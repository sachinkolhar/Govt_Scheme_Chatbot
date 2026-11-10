
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
ARTIFACTS = ROOT / "colab_retrieval_artifacts"

required_files = [
    "scheme_chunks.csv",
    "scheme_chunks_enriched.csv",
    "scheme_embeddings.npy",
    "scheme_encoder_name.txt",
]

print("=== Colab Artifact Validation ===")

missing = [name for name in required_files if not (ARTIFACTS / name).is_file()]

if missing:
    print("ERROR: Missing files:")
    for name in missing:
        print(f"  - {name}")
    raise SystemExit(1)

chunks = pd.read_csv(ARTIFACTS / "scheme_chunks.csv").fillna("")
enriched = pd.read_csv(
    ARTIFACTS / "scheme_chunks_enriched.csv"
).fillna("")
embeddings = np.load(
    ARTIFACTS / "scheme_embeddings.npy",
    allow_pickle=False,
)

encoder_name = (
    ARTIFACTS / "scheme_encoder_name.txt"
).read_text(encoding="utf-8").strip()

print(f"Original chunks: {len(chunks):,}")
print(f"Enriched chunks: {len(enriched):,}")
print(f"Embedding shape: {embeddings.shape}")
print(f"Embedding dtype: {embeddings.dtype}")
print(f"Encoder: {encoder_name}")

if embeddings.ndim != 2:
    raise SystemExit("FAIL: Embeddings must be a 2D matrix.")

if len(chunks) != len(enriched) or len(chunks) != len(embeddings):
    raise SystemExit("FAIL: Row counts do not match.")

if not np.isfinite(embeddings).all():
    raise SystemExit("FAIL: Embeddings contain NaN or infinity.")

if embeddings.dtype != np.float32:
    print("WARNING: Embeddings are not float32.")

if embeddings.shape[0] == 0 or embeddings.shape[1] == 0:
    raise SystemExit("FAIL: Embeddings are empty.")

# Check row identity where shared columns exist.
identity_columns = [
    col for col in ["chunk_id", "scheme_id", "chunk_type", "chunk_number"]
    if col in chunks.columns and col in enriched.columns
]

if not identity_columns:
    print("WARNING: No shared identity columns found.")
else:
    aligned = chunks[identity_columns].astype(str).equals(
        enriched[identity_columns].astype(str)
    )
    print(f"Shared identity columns: {identity_columns}")
    print(f"CSV row identity aligned: {aligned}")

    if not aligned:
        raise SystemExit("FAIL: CSV rows are not aligned.")

norms = np.linalg.norm(embeddings, axis=1)
print(f"Vector norm range: {norms.min():.5f} to {norms.max():.5f}")

print("\nPASS: Basic artifact integrity checks completed.")
print("Note: This does not yet verify the local FAISS index mapping.")
