"""Create a non-destructive manifest of Results-rebuild input artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parents[2]
MANIFEST_PATH = SCRIPT_DIR / "input_manifest.csv"

INPUTS = [
    ("dataset/govt_schemes.csv", "dataset"),
    ("model/scheme_index.faiss", "FAISS retrieval index"),
    ("model/semantic_encoder.pkl", "embedding encoder"),
    ("backend/evaluation/test_queries.json", "evaluation queries"),
    ("backend/evaluation/label_audit.csv", "label audit"),
    (
        "backend/evaluation/label_audit_reports/label_mapping_review.csv",
        "label mapping review",
    ),
    (
        "backend/evaluation/label_audit_reports/manual_review_worksheet.csv",
        "manual label review worksheet",
    ),
    (
        "backend/evaluation/label_audit_reports/positive_candidate_records.csv",
        "positive candidate records",
    ),
    ("backend/evaluation/results", "legacy evaluation output directory"),
    (
        "backend/evaluation/score_diagnostic_results",
        "L2 diagnostic output directory",
    ),
]

FIELDNAMES = [
    "relative_path",
    "file_role",
    "item_type",
    "exists",
    "size_bytes",
    "sha256",
    "row_count",
    "query_count",
    "positive_label_count",
    "negative_label_count",
    "faiss_index_type",
    "faiss_metric_type",
    "embedding_dimension",
    "vector_count",
    "alignment_status",
    "status",
    "notes",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative_path(path: Path) -> str:
    return path.relative_to(ROOT_DIR).as_posix()


def csv_data_row_count(path: Path) -> int | None:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.reader(handle)
            next(reader, None)
            return sum(1 for _ in reader)
    except (OSError, UnicodeError, csv.Error):
        return None


def query_metadata(path: Path) -> dict[str, int | None]:
    try:
        records = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(records, list):
            return {"query_count": None, "positive_label_count": None, "negative_label_count": None}
        return {
            "query_count": len(records),
            "positive_label_count": sum(record.get("expected_match") is True for record in records),
            "negative_label_count": sum(record.get("expected_match") is False for record in records),
        }
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {"query_count": None, "positive_label_count": None, "negative_label_count": None}


def faiss_metadata(path: Path) -> dict[str, Any]:
    metadata: dict[str, Any] = {
        "faiss_index_type": "Not verified",
        "faiss_metric_type": "Not verified",
        "embedding_dimension": "Not verified",
        "vector_count": "Not verified",
    }
    try:
        import faiss

        index = faiss.read_index(str(path))
        metric_names = {
            faiss.METRIC_INNER_PRODUCT: "METRIC_INNER_PRODUCT",
            faiss.METRIC_L2: "METRIC_L2 (squared L2 distance)",
        }
        metadata.update(
            {
                "faiss_index_type": type(index).__name__,
                "faiss_metric_type": metric_names.get(index.metric_type, str(index.metric_type)),
                "embedding_dimension": index.d,
                "vector_count": index.ntotal,
            }
        )
    except (ImportError, OSError, RuntimeError, AttributeError):
        pass
    return metadata


def metadata_for_file(path: Path) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    if path.suffix.lower() == ".csv":
        metadata["row_count"] = csv_data_row_count(path)
    if path.name == "test_queries.json":
        metadata.update(query_metadata(path))
    if path.name == "scheme_index.faiss":
        metadata.update(faiss_metadata(path))
    return metadata


def status_for(relative: str) -> str:
    if relative in {"dataset/govt_schemes.csv", "model/scheme_index.faiss", "model/semantic_encoder.pkl", "backend/evaluation/test_queries.json"}:
        return "current"
    if relative.startswith("backend/evaluation/results/") or relative.startswith(
        "backend/evaluation/score_diagnostic_results/"
    ) or relative.startswith("backend/evaluation/label_audit_reports/") or relative == "backend/evaluation/label_audit.csv":
        return "generated"
    return "not verified"


def notes_for(relative: str, item_type: str) -> str:
    if item_type == "directory":
        return "Directory entry; child files are listed separately and hashed individually."
    if relative == "dataset/govt_schemes.csv":
        return "Current scheme dataset. Row count agrees with the index vector count, but exact index-to-row order is Not verified."
    if relative == "model/scheme_index.faiss":
        return "Current FAISS asset. Index IDs are consumed positionally by dataframe.iloc in application/evaluation code; build-time row-order evidence is Not verified."
    if relative == "model/semantic_encoder.pkl":
        return "Current encoder asset; encoder model/version metadata is Not verified by the available manifest inputs."
    if relative == "backend/evaluation/test_queries.json":
        return "Current source query labels; label semantic validity is not established for all positive records."
    if relative.endswith("positive_candidate_records.csv"):
        return "Generated audit records. Name-similarity fields are not FAISS similarity; candidate FAISS distance is recorded as unavailable."
    if relative.endswith("manual_review_worksheet.csv"):
        return "Generated review input; reviewer decisions remain pending in the current artifact."
    if relative.startswith("backend/evaluation/results/"):
        return "Generated legacy evaluation output; interpretation is affected by higher-is-better logic applied to the L2 index."
    if relative.startswith("backend/evaluation/score_diagnostic_results/"):
        return "Generated L2 diagnostic output; metrics use source labels and are not fully ground-truth validated."
    if relative.endswith("label_audit.csv") or relative.endswith("label_mapping_review.csv"):
        return "Generated label-audit output; traceability does not establish semantic correctness."
    return "Metadata not verified beyond file existence and hash."


def make_record(path: Path, role: str) -> dict[str, Any]:
    rel = relative_path(path)
    item_type = "directory" if path.is_dir() else "file"
    record: dict[str, Any] = {
        "relative_path": rel,
        "file_role": role,
        "item_type": item_type,
        "exists": path.exists(),
        "size_bytes": path.stat().st_size if path.is_file() else "",
        "sha256": sha256_file(path) if path.is_file() else "",
        "row_count": "",
        "query_count": "",
        "positive_label_count": "",
        "negative_label_count": "",
        "faiss_index_type": "",
        "faiss_metric_type": "",
        "embedding_dimension": "",
        "vector_count": "",
        "alignment_status": "Not verified",
        "status": status_for(rel),
        "notes": notes_for(rel, item_type),
    }
    if path.is_file():
        record.update(metadata_for_file(path))
    if rel in {"dataset/govt_schemes.csv", "model/scheme_index.faiss"}:
        record["alignment_status"] = "Not verified: matching counts do not prove row-order alignment."
    return record


def collect_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for relative, role in INPUTS:
        path = ROOT_DIR / relative
        if not path.exists():
            missing = make_record(path, role)
            missing["status"] = "not verified"
            missing["notes"] = "Input is missing; no metadata or hash can be produced."
            records.append(missing)
            continue
        records.append(make_record(path, role))
        if path.is_dir():
            for child in sorted(path.rglob("*")):
                if child.is_file():
                    records.append(make_record(child, role))
    return records


def validate(records: list[dict[str, Any]]) -> None:
    errors: list[str] = []
    for record in records:
        if not record["relative_path"] or not record["file_role"] or not record["status"]:
            errors.append(f"missing required field: {record}")
        if record["item_type"] == "file" and record["exists"] and not record["sha256"]:
            errors.append(f"missing SHA-256 for file: {record['relative_path']}")
    if errors:
        raise ValueError("Manifest validation failed:\n" + "\n".join(errors))


def write_manifest(records: list[dict[str, Any]]) -> None:
    with MANIFEST_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(records)


def main() -> int:
    records = collect_records()
    validate(records)
    write_manifest(records)
    file_records = [record for record in records if record["item_type"] == "file"]
    missing = [record["relative_path"] for record in records if not record["exists"]]
    alignment = "Not verified: no build-time row-order evidence found; code uses positional dataframe.iloc mapping."
    print(f"Processed {len(records)} manifest entries ({len(file_records)} files).")
    print(f"Missing inputs: {len(missing)}" + (f" ({', '.join(missing)})" if missing else "."))
    print(f"Alignment evidence: {alignment}")
    print(f"Wrote {MANIFEST_PATH.relative_to(ROOT_DIR).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
