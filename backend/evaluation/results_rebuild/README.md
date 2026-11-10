# Notebook artifact rebuild

`rebuild_notebook_artifacts.py` is a non-destructive implementation of the
verified preprocessing, embedding, FAISS, and Logistic Regression save logic
from `mini.ipynb`.

## Run

From the project root:

```powershell
.\venv\Scripts\python.exe backend\evaluation\results_rebuild\rebuild_notebook_artifacts.py
```

The script reads the existing root `dataset.csv` and first writes to a unique
hidden staging directory under the project root. It validates the staged
artifacts, then atomically publishes the complete directory as
`rebuild_outputs\`. It refuses to run if `rebuild_outputs\` already exists;
this conservative rule is required to guarantee that no target file is
overwritten and that a failed run cannot leave a partially published result.
For a controlled rerun, use an explicitly separate destination:

```powershell
.\venv\Scripts\python.exe backend\evaluation\results_rebuild\rebuild_notebook_artifacts.py `
  --output-dir rebuild_outputs_second
```

The destination must not already exist. The default remains
`rebuild_outputs\`, and no output directory is overwritten.

Required components are used independently where possible. Missing top-level
packages and broken imports caused by transitive dependencies are recorded
separately in `rebuild_manifest.json`; unexpected runtime exceptions are not
converted into "missing package" statuses.

## Manifest status semantics

The top-level `status` field is explicit and derived from the required artifact
set, not merely from whether the script reached the end of execution. The
required artifacts are the six published rebuild outputs:

- `processed_schemes.csv`
- `scheme_embeddings.npy`
- `semantic_encoder.pkl`
- `scheme_index.faiss`
- `scheme_classifier.pkl`
- `label_binarizer.pkl`

A manifest is `complete` only when every required artifact is present and marked
`generated`. If any required artifact is unavailable, missing, or otherwise not
`generated`, the manifest is `partial`.

Per-artifact `status` values remain available for debugging and auditing, while
`status` at the root provides the single completion signal for the output set.

## Artifact integrity metadata

For each successfully generated artifact, the manifest records:

- `size_bytes`: the exact file size in bytes
- `sha256`: the lowercase SHA-256 digest of the file contents

These values are computed from the generated artifact file itself. The manifest
itself is intentionally excluded from its own hash and size metadata. To validate
an artifact externally, calculate the hash and size from the published file on
disk, then compare them to the manifest values. For example:

```powershell
Get-FileHash .\rebuild_outputs\scheme_embeddings.npy -Algorithm SHA256
Get-Item .\rebuild_outputs\scheme_embeddings.npy | Select-Object -Expand Length
```

This verifies file identity for the published output set; it does not verify
historical dataset/index alignment or historical evaluation metrics.

## Output-set validation

To validate the published artifact set, compare each generated file's measured
size and SHA-256 against the manifest entries, then confirm the required artifact
set is present and the root `status` is `complete`.

## Generated artifacts

- `processed_schemes.csv`: notebook-cleaned text and normalized categories.
- `scheme_embeddings.npy`: `all-MiniLM-L6-v2` embeddings in original row order.
- `semantic_encoder.pkl`: the loaded Sentence Transformers encoder.
- `scheme_index.faiss`: a verified `IndexFlatL2` index over those embeddings.
- `scheme_classifier.pkl`: the notebook cell 40 Logistic Regression
  `OneVsRestClassifier`.
- `label_binarizer.pkl`: the fitted `MultiLabelBinarizer`.
- `rebuild_manifest.json`: input/output paths, package versions, model revision
  when exposed by the runtime, artifact status, and FAISS verification details.

Before publication, the script reloads and validates the staged CSV, NumPy
embeddings, classifier, label binarizer, and FAISS index. These checks prove
that the persisted files agree with the current in-memory rebuild and preserve
the processed row order. They do not prove historical dataset identity,
semantic label correctness, or FAISS alignment with an external dataset.

After validating `processed_schemes.csv`, the script reloads it with the
notebook's default `pandas.read_csv()` behavior before label encoding,
classifier training, and embedding generation. This intentionally preserves
the notebook's CSV round-trip semantics: serialized empty fields become
`NaN` under pandas defaults. The validation step separately uses
`keep_default_na=False` so it can compare the persisted text exactly and does
not silently reinterpret empty fields.

The manifest also records the exact notebook category-mapping behavior,
including counts mapped to `"other"`. In particular, the notebook splits raw
categories on commas before matching; keys such as
`"banking,financial services and insurance"` therefore do not match as a
whole and remain `"other"`. This behavior is preserved rather than silently
reinterpreted.

The notebook's later Random Forest/TF-IDF and `lr_model` save cells are
ambiguous alternatives and are intentionally excluded. These outputs are new
artifacts based on the currently available dataset; they do not reproduce or
validate the historical 50-query retrieval or 52-case recommendation results.
