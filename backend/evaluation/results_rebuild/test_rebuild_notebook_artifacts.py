from __future__ import annotations

import hashlib
import importlib.util
from types import SimpleNamespace
from pathlib import Path

import pytest


SCRIPT_PATH = Path(__file__).with_name("rebuild_notebook_artifacts.py")
SPEC = importlib.util.spec_from_file_location("rebuild_notebook_artifacts", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


@pytest.mark.parametrize(
    ("raw_category", "expected"),
    [
        ("education & learning", "education"),
        ("banking,financial services and insurance", "other"),
        ("public safety,law & justice", "other"),
        ("agriculture,rural & environment", "other"),
    ],
)
def test_map_category_matches_notebook_comma_split(raw_category: str, expected: str) -> None:
    assert MODULE.map_category(raw_category) == expected


def test_category_summary_reports_other_without_reinterpreting_commas() -> None:
    summary = MODULE.category_mapping_summary(
        [
            "education & learning",
            "banking,financial services and insurance",
            "public safety,law & justice",
        ]
    )
    assert summary["input_count"] == 3
    assert summary["mapped_category_counts"] == {"education": 1, "other": 2}
    assert summary["other_count"] == 2


def test_existing_output_directory_is_rejected(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    output_dir = tmp_path / "rebuild_outputs"
    output_dir.mkdir()
    (output_dir / "existing.txt").write_text("protected", encoding="utf-8")
    monkeypatch.setattr(MODULE, "OUTPUT_DIR", output_dir)

    with pytest.raises(RuntimeError, match="non-empty output directory"):
        MODULE.create_staging_directory(False)


def test_alternate_output_directory_can_be_staged_without_touching_protected_output(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    protected_output = tmp_path / "rebuild_outputs"
    protected_output.mkdir()
    (protected_output / "existing.txt").write_text("protected", encoding="utf-8")
    alternate_output = tmp_path / "rebuild_outputs_second"
    monkeypatch.setattr(MODULE, "OUTPUT_DIR", alternate_output)

    staging = MODULE.create_staging_directory(False)

    try:
        assert staging.is_dir()
        assert (protected_output / "existing.txt").read_text(encoding="utf-8") == "protected"
        assert not alternate_output.exists()
    finally:
        MODULE.cleanup_staging_directory(staging)


def test_cli_output_dir_is_parsed_without_running_rebuild(tmp_path: Path) -> None:
    output_dir = tmp_path / "rebuild_outputs_second"

    args = MODULE.parse_args(["--output-dir", str(output_dir)])

    assert args.output_dir == output_dir


def test_cli_output_dir_refuses_existing_destination_without_running_rebuild(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output_dir = tmp_path / "rebuild_outputs_second"
    output_dir.mkdir()
    (output_dir / "existing.txt").write_text("protected", encoding="utf-8")
    args = MODULE.parse_args(["--output-dir", str(output_dir)])
    monkeypatch.setattr(MODULE, "OUTPUT_DIR", args.output_dir.resolve())

    with pytest.raises(RuntimeError, match="non-empty output directory"):
        MODULE.create_staging_directory(False)


def test_faiss_verification_checks_count_dimension_and_metric() -> None:
    faiss = pytest.importorskip("faiss")
    numpy = pytest.importorskip("numpy")
    index = faiss.IndexFlatL2(3)
    index.add(numpy.zeros((2, 3), dtype=numpy.float32))

    MODULE.verify_faiss_index(index, 2, 3, faiss)
    with pytest.raises(RuntimeError, match="FAISS verification failed"):
        MODULE.verify_faiss_index(index, 3, 3, faiss)
    with pytest.raises(RuntimeError, match="FAISS verification failed"):
        MODULE.verify_faiss_index(index, 2, 4, faiss)
    inner_product = faiss.IndexFlatIP(3)
    with pytest.raises(RuntimeError, match="FAISS verification failed"):
        MODULE.verify_faiss_index(inner_product, 0, 3, faiss)


def test_load_dependencies_distinguishes_transitive_import_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    real_import = MODULE.importlib.import_module

    def broken_import(name: str) -> object:
        if name == "sentence_transformers":
            raise ModuleNotFoundError(
                "No module named 'broken_transitive_dependency'",
                name="broken_transitive_dependency",
            )
        return real_import(name)

    monkeypatch.setattr(MODULE.importlib, "import_module", broken_import)
    dependencies = MODULE.load_dependencies()

    assert "sentence_transformers" not in dependencies["_missing"]
    assert dependencies["_import_errors"]["sentence_transformers"] == {
        "requested_module": "sentence_transformers",
        "missing_module": "broken_transitive_dependency",
        "message": "No module named 'broken_transitive_dependency'",
    }


def test_persisted_embedding_validation_rejects_dimension_and_count(
    tmp_path: Path,
) -> None:
    numpy = pytest.importorskip("numpy")
    expected = numpy.zeros((2, 3), dtype=numpy.float32)
    path = tmp_path / "embeddings.npy"

    numpy.save(path, numpy.zeros((2, 4), dtype=numpy.float32))
    with pytest.raises(RuntimeError, match="row count or dimension"):
        MODULE.validate_persisted_embeddings(path, expected, numpy, 2)

    numpy.save(path, numpy.zeros((1, 3), dtype=numpy.float32))
    with pytest.raises(RuntimeError, match="row count or dimension"):
        MODULE.validate_persisted_embeddings(path, expected, numpy, 2)


def test_persisted_processed_validation_preserves_empty_cleaned_text(
    tmp_path: Path,
) -> None:
    pandas = pytest.importorskip("pandas")
    expected = pandas.DataFrame(
        {
            "cleaned_text": ["", "normal scheme text"],
            "schemeCategory": ["other", "education"],
        }
    )
    path = tmp_path / "processed_schemes.csv"
    expected.to_csv(path, index=False)

    result = MODULE.validate_persisted_processed(path, expected, pandas)

    assert result["rows"] == 2
    assert result["columns"] == ["cleaned_text", "schemeCategory"]


def test_empty_scheme_category_is_not_allowed_by_current_mapping(
    tmp_path: Path,
) -> None:
    pandas = pytest.importorskip("pandas")
    expected = pandas.DataFrame(
        {"cleaned_text": ["normal scheme text"], "schemeCategory": ["other"]}
    )
    persisted = pandas.DataFrame(
        {"cleaned_text": ["normal scheme text"], "schemeCategory": [""]}
    )
    path = tmp_path / "processed_schemes.csv"
    persisted.to_csv(path, index=False)

    # Cell 20 maps an empty raw category to "other"; an empty persisted
    # schemeCategory must not be treated as equivalent.
    assert MODULE.map_category("") == "other"
    with pytest.raises(RuntimeError, match="rows or order differ"):
        MODULE.validate_persisted_processed(path, expected, pandas)


def test_persisted_processed_validation_accepts_normal_rows_and_rejects_changes(
    tmp_path: Path,
) -> None:
    pandas = pytest.importorskip("pandas")
    expected = pandas.DataFrame(
        {
            "cleaned_text": ["first scheme", "second scheme"],
            "schemeCategory": ["education", "health"],
        }
    )
    path = tmp_path / "processed_schemes.csv"
    expected.to_csv(path, index=False)
    MODULE.validate_persisted_processed(path, expected, pandas)

    changed = expected.copy()
    changed.loc[0, "cleaned_text"] = "changed scheme"
    changed.to_csv(path, index=False)
    with pytest.raises(RuntimeError, match="rows or order differ"):
        MODULE.validate_persisted_processed(path, expected, pandas)

    reordered = expected.iloc[::-1].reset_index(drop=True)
    reordered.to_csv(path, index=False)
    with pytest.raises(RuntimeError, match="rows or order differ"):
        MODULE.validate_persisted_processed(path, expected, pandas)


def test_downstream_reload_uses_notebook_default_na_semantics(
    tmp_path: Path,
) -> None:
    pandas = pytest.importorskip("pandas")
    persisted = pandas.DataFrame(
        {
            "cleaned_text": ["", "normal scheme text"],
            "schemeCategory": ["other", "education"],
        }
    )
    path = tmp_path / "processed_schemes.csv"
    persisted.to_csv(path, index=False)

    reloaded = MODULE.reload_processed_for_downstream(path, pandas)

    # The notebook uses read_csv() without keep_default_na=False. Preserve
    # that boundary: empty serialized fields become NaN downstream.
    assert pandas.isna(reloaded.loc[0, "cleaned_text"])
    assert reloaded.loc[1, "cleaned_text"] == "normal scheme text"
    assert reloaded.loc[0, "schemeCategory"] == "other"


def test_classifier_validation_rejects_dimension_mismatch(tmp_path: Path) -> None:
    classifier_path = tmp_path / "classifier.pkl"
    label_path = tmp_path / "labels.pkl"
    classifier = SimpleNamespace(n_features_in_=4)
    label_binarizer = SimpleNamespace(classes_=numpy_array(["education"]))

    class FakeJoblib:
        @staticmethod
        def load(path: Path) -> object:
            return classifier if path == classifier_path else label_binarizer

    with pytest.raises(RuntimeError, match="feature dimension"):
        MODULE.validate_persisted_models(
            classifier_path,
            label_path,
            3,
            numpy_array(["education"]),
            FakeJoblib,
        )


def test_publication_rejects_destination_created_after_staging(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    staging = tmp_path / ".rebuild_outputs.test"
    staging.mkdir()
    destination = tmp_path / "rebuild_outputs"
    destination.mkdir()
    monkeypatch.setattr(MODULE, "OUTPUT_DIR", destination)

    with pytest.raises(RuntimeError, match="output path now exists"):
        MODULE.publish_staging_directory(staging)


def test_artifact_status_for_manifest_marks_required_missing_as_partial() -> None:
    manifest = {
        "artifacts": {
            "processed_schemes.csv": {"status": "generated"},
            "scheme_embeddings.npy": {"status": "generated"},
            "semantic_encoder.pkl": {"status": "generated"},
            "scheme_index.faiss": {"status": "generated"},
            "scheme_classifier.pkl": {"status": "generated"},
            "label_binarizer.pkl": {"status": "unavailable", "reason": "missing"},
        }
    }

    assert MODULE.artifact_status_for_manifest(manifest["artifacts"]) == "partial"


def test_artifact_status_for_manifest_marks_all_required_generated_as_complete() -> None:
    manifest = {
        "artifacts": {
            "processed_schemes.csv": {"status": "generated"},
            "scheme_embeddings.npy": {"status": "generated"},
            "semantic_encoder.pkl": {"status": "generated"},
            "scheme_index.faiss": {"status": "generated"},
            "scheme_classifier.pkl": {"status": "generated"},
            "label_binarizer.pkl": {"status": "generated"},
        }
    }

    assert MODULE.artifact_status_for_manifest(manifest["artifacts"]) == "complete"


def test_manifest_artifact_metadata_matches_each_published_artifact_file(
    tmp_path: Path,
) -> None:
    artifact_names = [
        "processed_schemes.csv",
        "scheme_embeddings.npy",
        "semantic_encoder.pkl",
        "scheme_index.faiss",
        "scheme_classifier.pkl",
        "label_binarizer.pkl",
    ]
    manifest = {"artifacts": {}}
    artifact_paths = {}
    for index, name in enumerate(artifact_names):
        path = tmp_path / name
        payload = f"artifact-{index}\n".encode("ascii")
        path.write_bytes(payload)
        artifact_paths[name] = path
        manifest["artifacts"][name] = {
            "status": "generated",
            **MODULE.artifact_integrity_metadata(path),
        }

    for name, path in artifact_paths.items():
        entry = manifest["artifacts"][name]
        assert entry["size_bytes"] == path.stat().st_size
        assert entry["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
        assert "rebuild_manifest.json" not in manifest["artifacts"]


def test_manifest_publication_records_integrity_from_published_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    staging = tmp_path / "staging"
    destination = tmp_path / "published"
    staging.mkdir()
    monkeypatch.setattr(MODULE, "OUTPUT_DIR", destination)
    manifest = {"artifacts": {}}

    for index, name in enumerate(MODULE.REQUIRED_ARTIFACTS):
        payload = f"published-artifact-{index}\n".encode("ascii")
        (staging / name).write_bytes(payload)
        manifest["artifacts"][name] = {"status": "generated"}

    published_manifest = MODULE.write_manifest_and_publish(staging, manifest)
    persisted = __import__("json").loads(
        (destination / "rebuild_manifest.json").read_text(encoding="utf-8")
    )

    assert published_manifest["status"] == "complete"
    assert persisted["status"] == "complete"
    for name in MODULE.REQUIRED_ARTIFACTS:
        path = destination / name
        entry = persisted["artifacts"][name]
        assert entry["size_bytes"] == path.stat().st_size
        assert entry["sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert "rebuild_manifest.json" not in persisted["artifacts"]


def test_manifest_publication_marks_unavailable_required_artifact_partial(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    staging = tmp_path / "staging"
    destination = tmp_path / "published"
    staging.mkdir()
    monkeypatch.setattr(MODULE, "OUTPUT_DIR", destination)
    manifest = {
        "artifacts": {
            name: {"status": "generated"} for name in MODULE.REQUIRED_ARTIFACTS
        }
    }
    missing_name = "scheme_classifier.pkl"
    for name in MODULE.REQUIRED_ARTIFACTS:
        if name != missing_name:
            (staging / name).write_bytes(name.encode("ascii"))

    MODULE.write_manifest_and_publish(staging, manifest)
    persisted = __import__("json").loads(
        (destination / "rebuild_manifest.json").read_text(encoding="utf-8")
    )

    assert persisted["status"] == "partial"
    assert persisted["artifacts"][missing_name]["status"] == "unavailable"


def numpy_array(values: list[str]) -> object:
    numpy = pytest.importorskip("numpy")
    return numpy.array(values)
