"""Rebuild artifacts from the verified portions of ``mini.ipynb``.

This script is intentionally non-destructive. It reads the root ``dataset.csv``
and writes only to the configured output directory. It does not run any
historical retrieval or recommendation evaluation.
"""

from __future__ import annotations

import argparse
import atexit
import hashlib
import importlib
import importlib.metadata
import json
import os
import platform
import shutil
import sys
import tempfile
from collections import Counter
from pathlib import Path
from numbers import Integral
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
INPUT_DATASET = PROJECT_ROOT / "dataset.csv"
OUTPUT_DIR = PROJECT_ROOT / "rebuild_outputs"
MODEL_NAME = "all-MiniLM-L6-v2"

CATEGORY_MAPPING = {
    "education & learning": "education",
    "skills & employment": "employment",
    "health & wellness": "health",
    "social welfare & empowerment": "social welfare",
    "business & entrepreneurship": "entrepreneurship",
    "banking,financial services and insurance": "finance",
    "women and child": "women",
    "housing & shelter": "housing",
    "utility & sanitation": "sanitation",
    "transport & infrastructure": "infrastructure",
    "science, it & communications": "technology",
    "sports & culture": "sports",
    "travel & tourism": "tourism",
    "public safety,law & justice": "public safety",
    "agriculture,rural & environment": "agriculture",
}

PACKAGE_NAMES = (
    "faiss-cpu",
    "joblib",
    "nltk",
    "numpy",
    "pandas",
    "scikit-learn",
    "sentence-transformers",
    "torch",
    "transformers",
)
REQUIRED_ARTIFACTS = (
    "processed_schemes.csv",
    "scheme_embeddings.npy",
    "semantic_encoder.pkl",
    "scheme_index.faiss",
    "scheme_classifier.pkl",
    "label_binarizer.pkl",
)


def map_category(raw_string: str) -> str:
    """Apply notebook cell 20 exactly, including its comma split behavior."""
    parts = [part.strip().lower() for part in raw_string.split(",")]
    mapped = set()
    for part in parts:
        for key in CATEGORY_MAPPING:
            if key in part:
                mapped.add(CATEGORY_MAPPING[key])
    return ", ".join(sorted(mapped)) if mapped else "other"


def category_mapping_summary(raw_categories: Any) -> dict[str, Any]:
    """Summarize the exact notebook mapping without changing its semantics."""
    mapped = [map_category(value) for value in raw_categories]
    counts = Counter(mapped)
    return {
        "input_count": len(mapped),
        "unique_output_count": len(counts),
        "mapped_category_counts": dict(sorted(counts.items())),
        "other_count": counts.get("other", 0),
    }


def clean_text(
    text: str,
    custom_stopwords: set[str],
    lemmatizer: Any,
) -> str:
    """Apply the cleaning sequence from notebook cell 16."""
    import re

    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in custom_stopwords]
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)


def package_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for package_name in PACKAGE_NAMES:
        try:
            versions[package_name] = importlib.metadata.version(package_name)
        except importlib.metadata.PackageNotFoundError:
            versions[package_name] = "unavailable"
    return versions


def model_revision(model: Any) -> str:
    """Return a revision only when the loaded model exposes one."""
    configs: list[Any] = []
    for module in getattr(model, "_modules", {}).values():
        auto_model = getattr(module, "auto_model", None)
        configs.append(getattr(auto_model, "config", None))
        configs.append(getattr(module, "config", None))
    configs.append(getattr(model, "config", None))
    for config in configs:
        revision = getattr(config, "_commit_hash", None)
        if revision:
            return str(revision)
    return "not exposed by loaded model"


def load_dependencies() -> dict[str, Any]:
    dependencies: dict[str, Any] = {}
    module_names = {
        "faiss": "faiss",
        "joblib": "joblib",
        "nltk": "nltk",
        "numpy": "numpy",
        "pandas": "pandas",
        "sklearn": "sklearn",
        "sentence_transformers": "sentence_transformers",
    }
    missing: dict[str, dict[str, str | None]] = {}
    import_errors: dict[str, dict[str, str | None]] = {}
    for key, module_name in module_names.items():
        try:
            dependencies[key] = importlib.import_module(module_name)
        except ModuleNotFoundError as exc:
            details = {
                "requested_module": module_name,
                "missing_module": exc.name,
                "message": str(exc),
            }
            if exc.name == module_name:
                missing[key] = details
            else:
                import_errors[key] = details
        except ImportError as exc:
            import_errors[key] = {
                "requested_module": module_name,
                "missing_module": None,
                "message": f"{type(exc).__name__}: {exc}",
            }
    dependencies["_missing"] = missing
    dependencies["_import_errors"] = import_errors
    return dependencies


def create_staging_directory(allow_existing: bool) -> Path:
    """Create an isolated staging directory before any artifact is written."""
    if OUTPUT_DIR.exists():
        if not OUTPUT_DIR.is_dir():
            raise RuntimeError(f"Output path is not a directory: {OUTPUT_DIR}")
        if any(OUTPUT_DIR.iterdir()):
            raise RuntimeError(
                f"Refusing to write to non-empty output directory {OUTPUT_DIR}."
            )
        raise RuntimeError(
            f"Refusing to publish into existing output directory {OUTPUT_DIR}; "
            "atomic directory publication cannot be guaranteed."
        )
    if allow_existing:
        raise RuntimeError(
            "--allow-existing-output cannot guarantee atomic publication and is "
            "intentionally unsupported."
        )
    return Path(tempfile.mkdtemp(prefix=".rebuild_outputs.", dir=PROJECT_ROOT))


def cleanup_staging_directory(staging_dir: Path) -> None:
    if staging_dir.exists():
        shutil.rmtree(staging_dir)


def publish_staging_directory(staging_dir: Path) -> None:
    """Atomically publish a complete staging directory without overwriting."""
    if OUTPUT_DIR.exists():
        raise RuntimeError(
            f"Refusing publication because output path now exists: {OUTPUT_DIR}"
        )
    os.replace(staging_dir, OUTPUT_DIR)


def verify_faiss_index(
    index: Any,
    expected_count: int,
    expected_dimension: int,
    faiss_module: Any,
) -> None:
    if (
        index.ntotal != expected_count
        or index.d != expected_dimension
        or index.metric_type != faiss_module.METRIC_L2
    ):
        raise RuntimeError(
            "FAISS verification failed: vector count, dimension, or metric type "
            "does not match the generated embeddings."
        )


def feature_dimension_from_classifier(classifier: Any) -> int | None:
    """Find a reliable fitted feature dimension across sklearn APIs."""
    dimensions: list[int] = []
    top_level = getattr(classifier, "n_features_in_", None)
    if isinstance(top_level, Integral):
        dimensions.append(int(top_level))
    for estimator in getattr(classifier, "estimators_", []):
        estimator_dimension = getattr(estimator, "n_features_in_", None)
        if isinstance(estimator_dimension, Integral):
            dimensions.append(int(estimator_dimension))
    if not dimensions or len(set(dimensions)) != 1:
        return None
    return dimensions[0]


def frame_digest(frame: Any, pandas_module: Any) -> str:
    """Digest persisted row content and order, not semantic dataset identity."""
    hashed = pandas_module.util.hash_pandas_object(frame, index=False).to_numpy()
    return hashlib.sha256(hashed.tobytes()).hexdigest()


def validate_persisted_processed(
    path: Path,
    expected_frame: Any,
    pandas_module: Any,
) -> dict[str, Any]:
    # Empty strings are valid cleaned text output, so preserve them through
    # the CSV round trip rather than converting them to NaN.
    reloaded = pandas_module.read_csv(path, keep_default_na=False)
    expected_columns = ["cleaned_text", "schemeCategory"]
    if list(reloaded.columns) != expected_columns:
        raise RuntimeError(
            f"Persisted processed columns differ: {list(reloaded.columns)!r}"
        )
    if len(reloaded) != len(expected_frame):
        raise RuntimeError("Persisted processed row count does not match in-memory data.")
    expected = expected_frame[expected_columns].reset_index(drop=True)
    if not reloaded.reset_index(drop=True).equals(expected):
        raise RuntimeError(
            "Persisted processed rows or order differ from the generated data. "
            "This validates persistence consistency, not historical row identity."
        )
    return {
        "rows": int(len(reloaded)),
        "columns": list(reloaded.columns),
        "row_order_digest": frame_digest(reloaded, pandas_module),
        "identity_claim": "not proven by row counts or digest alone",
    }


def reload_processed_for_downstream(path: Path, pandas_module: Any) -> Any:
    """Reload staged CSV using notebook cell 22/25 default read_csv semantics."""
    reloaded = pandas_module.read_csv(path)
    expected_columns = ["cleaned_text", "schemeCategory"]
    if list(reloaded.columns) != expected_columns:
        raise RuntimeError(
            f"Reloaded processed columns differ: {list(reloaded.columns)!r}"
        )
    return reloaded


def validate_persisted_embeddings(
    path: Path,
    expected_embeddings: Any,
    numpy_module: Any,
    expected_rows: int,
) -> dict[str, Any]:
    reloaded = numpy_module.load(path, allow_pickle=False)
    if reloaded.ndim != 2:
        raise RuntimeError("Persisted embeddings are not a 2-D array.")
    if reloaded.shape != expected_embeddings.shape:
        raise RuntimeError(
            "Persisted embedding row count or dimension differs from generated data."
        )
    if reloaded.shape[0] != expected_rows or not numpy_module.array_equal(
        reloaded, expected_embeddings
    ):
        raise RuntimeError(
            "Persisted embeddings are inconsistent with the source-order generated data."
        )
    return {"rows": int(reloaded.shape[0]), "dimension": int(reloaded.shape[1])}


def validate_persisted_models(
    classifier_path: Path | None,
    label_path: Path | None,
    expected_dimension: int,
    expected_classes: Any,
    joblib_module: Any,
) -> dict[str, Any]:
    result: dict[str, Any] = {}
    if classifier_path is not None:
        classifier = joblib_module.load(classifier_path)
        dimension = feature_dimension_from_classifier(classifier)
        if dimension is None:
            raise RuntimeError(
                "Could not establish a reliable classifier feature dimension."
            )
        if dimension != expected_dimension:
            raise RuntimeError(
                "Persisted classifier feature dimension differs from embeddings."
            )
        result["classifier_dimension"] = dimension
    if label_path is not None:
        label_binarizer = joblib_module.load(label_path)
        classes = getattr(label_binarizer, "classes_", None)
        if classes is None or classes.tolist() != expected_classes.tolist():
            raise RuntimeError("Persisted label-binarizer classes differ from fitted classes.")
        result["classes"] = classes.tolist()
    return result


def write_new(path: Path, writer: Any) -> None:
    if path.exists():
        raise RuntimeError(f"Refusing to overwrite existing file: {path}")
    writer(path)


def artifact_status_for_manifest(artifacts: dict[str, Any]) -> str:
    """Return overall manifest status based on required artifact availability."""
    required = {name: artifacts.get(name, {}) for name in REQUIRED_ARTIFACTS}
    if any(
        not isinstance(details, dict) or details.get("status") != "generated"
        for details in required.values()
    ):
        return "partial"
    return "complete"


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def file_size_bytes(path: Path) -> int:
    return path.stat().st_size


def artifact_integrity_metadata(path: Path) -> dict[str, int | str]:
    return {
        "size_bytes": file_size_bytes(path),
        "sha256": file_sha256(path),
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help="Destination directory to publish without overwriting an existing path.",
    )
    return parser.parse_args(argv)


def write_manifest_and_publish(
    staging_dir: Path, manifest: dict[str, Any]
) -> dict[str, Any]:
    """Finalize metadata from staged bytes, write the manifest, and publish."""
    for artifact_name in REQUIRED_ARTIFACTS:
        details = manifest["artifacts"].get(artifact_name)
        artifact_path = staging_dir / artifact_name
        if not isinstance(details, dict):
            continue
        if details.get("status") == "generated" and not artifact_path.is_file():
            details["status"] = "unavailable"
            details["reason"] = "Generated artifact file is missing from staging."
        if details.get("status") == "generated":
            details.update(artifact_integrity_metadata(artifact_path))

    manifest["status"] = artifact_status_for_manifest(manifest["artifacts"])
    manifest["output_directory"] = str(OUTPUT_DIR)
    manifest_path = staging_dir / "rebuild_manifest.json"
    write_new(
        manifest_path,
        lambda path: path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8"
        ),
    )
    publish_staging_directory(staging_dir)
    return manifest


def main() -> int:
    global OUTPUT_DIR
    args = parse_args()
    OUTPUT_DIR = args.output_dir.resolve()

    if not INPUT_DATASET.is_file():
        raise FileNotFoundError(f"Required input dataset was not found: {INPUT_DATASET}")
    staging_dir = create_staging_directory(False)
    atexit.register(cleanup_staging_directory, staging_dir)

    dependencies = load_dependencies()
    missing = dependencies.pop("_missing")
    import_errors = dependencies.pop("_import_errors")
    manifest: dict[str, Any] = {
        "status": "partial",
        "input_dataset": str(INPUT_DATASET),
        "output_directory": str(OUTPUT_DIR),
        "model_name": MODEL_NAME,
        "historical_evaluation": {
            "retrieval_50_query": "not run and not implemented",
            "recommendation_52_case": "not run and not implemented",
        },
        "python": sys.version,
        "platform": platform.platform(),
        "package_versions": package_versions(),
        "missing_dependencies": missing,
        "dependency_import_errors": import_errors,
        "artifacts": {},
        "notes": [
            "The input dataset is read-only.",
            "The notebook did not record the original Sentence Transformers revision.",
            "Generated artifacts are new outputs and are not historical evidence.",
        ],
    }

    pandas = dependencies.get("pandas")
    numpy = dependencies.get("numpy")
    joblib = dependencies.get("joblib")
    sklearn = dependencies.get("sklearn")

    if pandas is None or numpy is None or dependencies.get("nltk") is None:
        missing_core = [
            name
            for name in ("pandas", "numpy", "nltk")
            if name not in dependencies
        ]
        manifest["artifacts"]["processed_schemes.csv"] = {
            "status": "unavailable",
            "reason": f"Missing required dependencies: {', '.join(missing_core)}",
        }
    else:
        from nltk.corpus import stopwords
        from nltk.stem import WordNetLemmatizer

        df = pandas.read_csv(INPUT_DATASET)
        source_row_count = len(df)
        manifest["input_dataset_rows"] = source_row_count
        if "Unnamed: 9" not in df.columns:
            raise ValueError("Notebook cell 8 expects an 'Unnamed: 9' column.")
        df.drop(columns=["Unnamed: 9"], inplace=True)
        for column in ("application", "documents", "tags"):
            if column not in df.columns:
                raise ValueError(f"Notebook cell 9 expects column {column!r}.")
            df[column] = df[column].fillna("")
        required_text = ("scheme_name", "details", "benefits", "eligibility", "tags")
        missing_text = [column for column in required_text if column not in df.columns]
        if missing_text:
            raise ValueError(f"Notebook cell 11 requires columns: {missing_text}")
        df["combined_text"] = (
            df["scheme_name"]
            + " "
            + df["details"]
            + " "
            + df["benefits"]
            + " "
            + df["eligibility"]
            + " "
            + df["tags"]
        )

        important_keywords = {
            "benefit",
            "loan",
            "assistance",
            "support",
            "eligible",
            "scheme",
            "financial",
            "application",
        }
        try:
            default_stopwords = set(stopwords.words("english"))
            lemmatizer = WordNetLemmatizer()
            lemmatizer.lemmatize("scheme")
        except LookupError as exc:
            manifest["artifacts"]["processed_schemes.csv"] = {
                "status": "unavailable",
                "reason": f"Missing NLTK resource: {exc}",
            }
            df = None
        else:
            custom_stopwords = default_stopwords - important_keywords
            df["cleaned_text"] = df["combined_text"].apply(
                lambda value: clean_text(value, custom_stopwords, lemmatizer)
            )
            if "schemeCategory" not in df.columns:
                raise ValueError("Notebook cell 20 requires column 'schemeCategory'.")
            df["normalized_category"] = df["schemeCategory"].apply(map_category)
            processed_df = df[["cleaned_text", "normalized_category"]].rename(
                columns={"normalized_category": "schemeCategory"}
            )
            processed_path = staging_dir / "processed_schemes.csv"
            write_new(processed_path, lambda path: processed_df.to_csv(path, index=False))
            manifest["artifacts"]["processed_schemes.csv"] = {
                "status": "generated",
                "rows": int(len(processed_df)),
                "columns": list(processed_df.columns),
                "row_order": "preserved; no row-reordering operation is used",
            }
            if processed_path.exists():
                manifest["artifacts"]["processed_schemes.csv"].update(
                    artifact_integrity_metadata(processed_path)
                )
            manifest["category_mapping"] = category_mapping_summary(
                df["schemeCategory"].tolist()
            )
            if len(processed_df) != source_row_count:
                raise RuntimeError("Processed row count does not match input row count.")
            manifest["artifacts"]["processed_schemes.csv"].update(
                validate_persisted_processed(processed_path, processed_df, pandas)
            )
            # Notebook cells 22 and 25 reload this CSV with pandas defaults
            # before encoding labels and generating embeddings.
            df = reload_processed_for_downstream(processed_path, pandas)

    labels = None
    if "df" not in locals() or df is None:
        manifest["artifacts"]["remaining"] = {
            "status": "unavailable",
            "reason": "Preprocessing did not produce a dataframe.",
        }
    else:
        sentence_transformers = dependencies.get("sentence_transformers")
        if joblib is None or sklearn is None:
            manifest["artifacts"]["label_binarizer.pkl"] = {
                "status": "unavailable",
                "reason": "joblib and scikit-learn are required.",
            }
        else:
            from sklearn.preprocessing import MultiLabelBinarizer

            label_list = df["schemeCategory"].apply(
                lambda value: [category.strip() for category in value.split(",")]
            )
            mlb = MultiLabelBinarizer()
            labels = mlb.fit_transform(label_list)
            label_path = staging_dir / "label_binarizer.pkl"
            write_new(label_path, lambda path: joblib.dump(mlb, path))
            manifest["artifacts"]["label_binarizer.pkl"] = {
                "status": "generated",
                "classes": mlb.classes_.tolist(),
            }
            if label_path.exists():
                manifest["artifacts"]["label_binarizer.pkl"].update(
                    artifact_integrity_metadata(label_path)
                )
            manifest["artifacts"]["label_binarizer.pkl"].update(
                validate_persisted_models(
                    None,
                    label_path,
                    0,
                    mlb.classes_,
                    joblib,
                )
            )

        if sentence_transformers is None:
            manifest["artifacts"]["embeddings_and_models"] = {
                "status": "unavailable",
                "reason": (
                    "sentence-transformers is not installed."
                    if "sentence_transformers" in missing
                    else "sentence-transformers import failed."
                ),
            }
        else:
            from sentence_transformers import SentenceTransformer

            sbert_model = SentenceTransformer(MODEL_NAME)
            embeddings = sbert_model.encode(
                df["cleaned_text"].tolist(), convert_to_numpy=True
            )
            manifest["model_revision"] = model_revision(sbert_model)
            if embeddings.ndim != 2:
                raise ValueError(f"Expected 2-D embeddings, got shape {embeddings.shape}.")
            if embeddings.shape[0] != source_row_count:
                raise RuntimeError(
                    "Embedding row count does not match the original dataset row count."
                )

            embeddings_path = staging_dir / "scheme_embeddings.npy"
            write_new(embeddings_path, lambda path: numpy.save(path, embeddings))
            manifest["artifacts"]["scheme_embeddings.npy"] = {
                "status": "generated",
                "rows": int(embeddings.shape[0]),
                "dimension": int(embeddings.shape[1]),
                "dtype": str(embeddings.dtype),
            }
            if embeddings_path.exists():
                manifest["artifacts"]["scheme_embeddings.npy"].update(
                    artifact_integrity_metadata(embeddings_path)
                )
            manifest["artifacts"]["scheme_embeddings.npy"].update(
                validate_persisted_embeddings(
                    embeddings_path, embeddings, numpy, source_row_count
                )
            )
            if joblib is None:
                manifest["artifacts"]["semantic_encoder.pkl"] = {
                    "status": "unavailable",
                    "reason": "joblib is not installed.",
                }
            else:
                encoder_path = staging_dir / "semantic_encoder.pkl"
                write_new(encoder_path, lambda path: joblib.dump(sbert_model, path))
                manifest["artifacts"]["semantic_encoder.pkl"] = {
                    "status": "generated",
                    "model_name": MODEL_NAME,
                    "revision": manifest["model_revision"],
                }
                if encoder_path.exists():
                    manifest["artifacts"]["semantic_encoder.pkl"].update(
                        artifact_integrity_metadata(encoder_path)
                    )

            if labels is not None and joblib is not None and sklearn is not None:
                from sklearn.linear_model import LogisticRegression
                from sklearn.model_selection import train_test_split
                from sklearn.multiclass import OneVsRestClassifier

                x_train, _, y_train, _ = train_test_split(
                    embeddings, labels, test_size=0.2, random_state=42
                )
                classifier = OneVsRestClassifier(
                    LogisticRegression(max_iter=1000, class_weight="balanced")
                )
                classifier.fit(x_train, y_train)
                classifier_dimension = feature_dimension_from_classifier(classifier)
                if classifier_dimension != embeddings.shape[1]:
                    raise RuntimeError(
                        "Classifier input dimension is unavailable or does not "
                        "match embedding dimension."
                    )
                classifier_path = staging_dir / "scheme_classifier.pkl"
                write_new(classifier_path, lambda path: joblib.dump(classifier, path))
                manifest["artifacts"]["scheme_classifier.pkl"] = {
                    "status": "generated",
                    "model": "OneVsRestClassifier(LogisticRegression(...))",
                    "notebook_cell": 40,
                }
                if classifier_path.exists():
                    manifest["artifacts"]["scheme_classifier.pkl"].update(
                        artifact_integrity_metadata(classifier_path)
                    )
                manifest["artifacts"]["scheme_classifier.pkl"].update(
                    validate_persisted_models(
                        classifier_path,
                        None,
                        embeddings.shape[1],
                        mlb.classes_,
                        joblib,
                    )
                )
            elif labels is not None:
                manifest["artifacts"]["scheme_classifier.pkl"] = {
                    "status": "unavailable",
                    "reason": (
                        "joblib and scikit-learn are required."
                        if joblib is None or sklearn is None
                        else "Classifier dependencies are unavailable."
                    ),
                }

            if dependencies.get("faiss") is None:
                manifest["artifacts"]["scheme_index.faiss"] = {
                    "status": "unavailable",
                    "reason": "faiss is not installed.",
                }
            else:
                faiss = dependencies["faiss"]
                if embeddings.dtype != numpy.float32:
                    raise ValueError(
                        "Notebook embeddings are not float32; refusing implicit conversion."
                    )
                index = faiss.IndexFlatL2(int(embeddings.shape[1]))
                index.add(embeddings)
                verify_faiss_index(
                    index, embeddings.shape[0], embeddings.shape[1], faiss
                )
                index_path = staging_dir / "scheme_index.faiss"
                write_new(index_path, lambda path: faiss.write_index(index, str(path)))
                verified_index = faiss.read_index(str(index_path))
                verify_faiss_index(
                    verified_index, embeddings.shape[0], embeddings.shape[1], faiss
                )
                manifest["artifacts"]["scheme_index.faiss"] = {
                    "status": "generated",
                    "ntotal": int(verified_index.ntotal),
                    "dimension": int(verified_index.d),
                    "metric_type": "METRIC_L2",
                    "distance_semantics": "squared L2; lower is closer",
                }
                if index_path.exists():
                    manifest["artifacts"]["scheme_index.faiss"].update(
                        artifact_integrity_metadata(index_path)
                    )

    write_manifest_and_publish(staging_dir, manifest)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
