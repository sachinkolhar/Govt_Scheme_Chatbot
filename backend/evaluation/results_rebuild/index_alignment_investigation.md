# FAISS Index Alignment Investigation

## Scope and Method

This investigation inspects the current repository code, documentation, model assets, and evaluation consumers. It does not rebuild the FAISS index, regenerate embeddings, modify any source/data/label/output file, or generate evaluation metrics.

The read-only helper `backend/evaluation/results_rebuild/inspect_index_alignment.py` can inspect current FAISS metadata and search source text for builder, ordering, embedding, mapping, and positional-lookup evidence. It does not query the index or write output files.

## 1. Current Artifact Facts

| Item                  | Finding                                                                    | Evidence                                                                                                                                                                                     | Status                          |
| --------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| Dataset               | `dataset/govt_schemes.csv` contains 3,400 rows                             | `backend/main.py:101` loads this CSV; current asset inspection and `input_manifest.csv` record 3,400 rows                                                                                    | Verified from current asset     |
| Index                 | `model/scheme_index.faiss` is loaded by the application and evaluators     | `backend/main.py:92`; `backend/evaluation/evaluation_pipeline.py:194-196`; `backend/evaluation/evaluation_pipeline_corrected.py:172`; `backend/evaluation/evaluation_score_diagnostic.py:95` | Verified from code              |
| Index type            | `IndexFlatL2`                                                              | Direct FAISS inspection recorded in `input_manifest.csv` and `BASELINE.md`                                                                                                                   | Verified from current artifact  |
| Distance metric       | `faiss.METRIC_L2`; FAISS output is squared L2 distance and lower is closer | `backend/evaluation/evaluation_score_diagnostic.py` documents and prints this interpretation; corrected pipeline requires L2                                                                 | Verified from code and artifact |
| Index dimension       | 384                                                                        | Direct FAISS inspection recorded in `input_manifest.csv` and `BASELINE.md`                                                                                                                   | Verified from current artifact  |
| Vector count          | 3,400                                                                      | Direct FAISS inspection recorded in `input_manifest.csv` and `BASELINE.md`                                                                                                                   | Verified from current artifact  |
| Encoder asset         | `model/semantic_encoder.pkl` is loaded with `joblib.load`                  | `backend/main.py:84`; `backend/evaluation/evaluation_pipeline.py:177-179`; `backend/evaluation/evaluation_pipeline_corrected.py:175`                                                         | Verified from code              |
| Encoder model/version | Not verified                                                               | No model manifest, constructor, training script, or authoritative version file was found                                                                                                     | Not verified                    |

The equal count of 3,400 dataset rows and 3,400 index vectors is recorded, but it is not treated as proof of row alignment.

## 2. Search for Index-Building and Embedding-Generation Code

### 2.1 Index-building code

A repository-wide search for `index.add`, `faiss.write_index`, `IndexIDMap`, and related index-construction operations found no index-building script. The available Python files contain consumers that call `faiss.read_index`, but no visible code that creates `scheme_index.faiss`.

Evidence from consumer files:

- `backend/main.py:92` calls `faiss.read_index(...)`.
- `backend/evaluation/evaluation_pipeline.py:194-196` calls `faiss.read_index(...)`.
- `backend/evaluation/evaluation_pipeline_corrected.py:172` calls `faiss.read_index(...)`.
- `backend/evaluation/evaluation_score_diagnostic.py:95` calls `faiss.read_index(...)`.

No matching builder call such as `index.add(...)` or `faiss.write_index(...)` was found in the project Python source. Therefore, the process that created the binary index is unavailable in this workspace.

**Conclusion:** The index-building process is missing from the available project files. **Status: Not verified.**

### 2.2 Embedding-generation code

The available code embeds query text at evaluation or runtime:

- `backend/search/semantic.py:63` calls `encoder.encode([cleaned], convert_to_numpy=True)` for a query.
- `backend/evaluation/evaluation_pipeline.py:242` calls `encoder.encode([query_clean], convert_to_numpy=True)`.
- `backend/evaluation/evaluation_pipeline_corrected.py:93` calls `encoder.encode([query.lower().strip()], convert_to_numpy=True)`.
- `backend/evaluation/evaluation_score_diagnostic.py:105-108` calls `encoder.encode(...)` for diagnostic queries.

These are query-encoding consumers, not corpus-embedding or index-construction code. No script was found that reads every dataset row, constructs the corpus text, calls `encode` over those rows, and writes the resulting vectors to `scheme_index.faiss`.

**Conclusion:** Corpus embedding generation and its ordering are not available. **Status: Not verified.**

## 3. Dataset Loading and Ordering

### 3.1 Runtime/evaluation loading order

The application loads the encoder, then the FAISS index, then the dataset:

- `backend/main.py:84` loads `semantic_encoder.pkl`.
- `backend/main.py:92` loads `scheme_index.faiss`.
- `backend/main.py:101` loads `govt_schemes.csv` with `pd.read_csv(...).fillna("")`.
- `backend/main.py:102` passes the three independently loaded objects to `semantic.configure_search_resources(...)`.

The evaluation consumers follow the same independent-loading pattern:

- `backend/evaluation/evaluation_pipeline.py:177-207` loads encoder, index, and CSV separately.
- `backend/evaluation/evaluation_pipeline_corrected.py:171-175` loads CSV, index, and encoder separately.
- `backend/evaluation/evaluation_score_diagnostic.py:94-99` loads CSV, index, and encoder separately.

The code shown does not sort, filter, shuffle, deduplicate, or reset the current dataset before these runtime/evaluation lookups. `fillna("")` changes missing-value representation, but it does not document or prove the historical order used during index construction.

**Status:** Current loading behavior is verified. Historical corpus preparation order is not verified.

### 3.2 Ordering operations found elsewhere

The repository contains `reset_index(drop=True)` in `backend/evaluation/create_manual_review_worksheet.py:56`, but that operation applies to a generated manual-review worksheet grouping, not to corpus embedding or FAISS index construction. It does not provide index alignment evidence.

No index-building-specific use of `sort_values`, `drop_duplicates`, `sample`, `shuffle`, or corpus `reset_index` was found. Absence of a visible operation is not proof that no such operation occurred before the binary artifacts were created.

**Conclusion:** No verified pre-index sorting, filtering, shuffling, deduplication, or index reset is available. The historical ordering pipeline remains **Not verified**.

## 4. FAISS ID to Dataset Record Mapping

### 4.1 Positional lookup in application code

The application uses FAISS result IDs as pandas positional indices:

- `backend/search/semantic.py:83` executes `df.iloc[idx]` after FAISS returns an index.
- `backend/search/routes.py:19` also maps candidate IDs with `df.iloc[idx]`.
- `backend/chat/processor.py:224` and `backend/chat/processor.py:291` use `get_dataframe().iloc[idx]` for retrieved schemes.
- `backend/eligibility/checker.py:370` uses `df.iloc[idx]` for recommendation candidates.

The legacy evaluator uses positional lookup too:

- `backend/evaluation/evaluation_pipeline.py:251` maps the FAISS index result with `df.iloc[int(idx)]`.

The corrected evaluator and diagnostic use positional lookup as well:

- `backend/evaluation/evaluation_pipeline_corrected.py:106` maps `matched_index` with `dataframe.iloc[matched_index]`.
- `backend/evaluation/evaluation_score_diagnostic.py:117` maps `top_index` with `dataframe.iloc[top_index]`.

This proves the runtime assumption: FAISS ID `i` is treated as dataset row position `i`. It does not prove that the assumption was true when the index was built.

### 4.2 Explicit mapping artifacts

No `IndexIDMap`, external FAISS-ID mapping table, dataset primary-key array, index manifest, or corpus-row-to-vector mapping file was found. The label-audit outputs contain dataset row indices for candidate records, but they are label-review artifacts and do not map every FAISS vector to a dataset record.

The candidate file `backend/evaluation/label_audit_reports/positive_candidate_records.csv` includes `dataset_row_index` and candidate slugs, but its `faiss_distance` values are recorded as unavailable. It is not an index-construction mapping artifact.

**Conclusion:** The application and evaluators use positional `dataframe.iloc` lookup, but no explicit FAISS-ID-to-dataset-record mapping is available. **Status: Verified consumer behavior; mapping validity Not verified.**

## 5. Dataset Row Alignment Evidence

### Verified from code

1. The current application loads the CSV and FAISS index as separate assets: `backend/main.py:84-102`.
2. The current application resolves FAISS IDs through positional dataframe lookup: `backend/search/semantic.py:63-83`.
3. The evaluation pipelines use the same positional lookup assumption: `backend/evaluation/evaluation_pipeline.py:242-251`, `backend/evaluation/evaluation_pipeline_corrected.py:93-106`, and `backend/evaluation/evaluation_score_diagnostic.py:105-117`.
4. Current dataset and index counts are both 3,400, and the index is 384-dimensional `IndexFlatL2`: `input_manifest.csv` and direct artifact inspection.

### Supported but incomplete

1. The runtime design is consistent with an index built in dataset row order, because returned IDs are consumed as `dataframe.iloc` positions.
2. The index vector count equals the dataset row count.
3. The evaluation README describes the FAISS index and dataset as paired resources, but it does not document the corpus embedding/build procedure or an explicit mapping.

These points support the possibility of row-order alignment but do not establish it.

### Not verified

1. The script or command that generated `scheme_index.faiss`.
2. The script or command that generated `semantic_encoder.pkl`.
3. The corpus text fields and preprocessing used to create index embeddings.
4. Whether corpus rows were sorted, filtered, shuffled, deduplicated, or reset before embedding.
5. Whether the CSV used during index construction was byte-for-byte or row-for-row the current `dataset/govt_schemes.csv`.
6. Whether index ID 0 corresponds to CSV row 0, index ID 1 to CSV row 1, and so on.
7. The encoder model name, version, weights, pooling, normalization, and embedding-generation settings used for the index.
8. Any external mapping file or build-time metadata not included in this workspace.

### Contradictory evidence

No direct contradictory index-builder evidence was found because the builder is absent. There is, however, a semantic configuration contradiction in consumers:

- `backend/config/settings.py:27` comments describe `IndexFlatIP` and cosine-like higher-is-better values.
- The actual current index is `IndexFlatL2`, and `backend/evaluation/evaluation_score_diagnostic.py` correctly treats values as squared L2 distances.
- `backend/search/semantic.py:77-78` and `backend/chat/processor.py` use higher-is-better threshold assumptions through `FAISS_MIN_SCORE` in the application path.

This contradiction concerns distance interpretation, not proof of row order. It further argues against treating existing application outputs as an alignment audit.

## 6. Encoder Identity and Version

The encoder is loaded from `model/semantic_encoder.pkl`:

- `backend/main.py:84` uses `joblib.load(...)`.
- `backend/evaluation/evaluation_pipeline.py:177-181` uses `joblib.load(...)` and describes the object as a SentenceTransformer-compatible encoder.
- `backend/evaluation/evaluation_pipeline_corrected.py:175` uses `joblib.load(...)`.
- `backend/evaluation/evaluation_score_diagnostic.py:99` uses `joblib.load(...)`.

Project documentation identifies the general technology as SentenceTransformers, and `EXPERIMENTATION_RESULTS.md:125` reports a SentenceTransformers version of 2.2.2. That documentation does not establish that the serialized encoder was created with that version, nor does it identify the exact model name or weights. No encoder-generation script, serialized metadata report, or hash-to-training configuration is available.

**Conclusion:** The encoder family is supported by code/documentation, but the exact encoder identity and version used to create the index are **Not verified**. The historical documentation is insufficient to establish reproducible index construction.

## 7. Alignment Conclusion

**Alignment conclusion: Not verified.**

The current project proves that the application and evaluation code assume FAISS IDs correspond directly to pandas dataset row positions. It does not prove that the existing FAISS index was built from the current CSV in that exact order. Equal dataset/index counts are insufficient, and no index-building script, corpus embedding script, explicit ID map, or build-time manifest is available.

## 8. Evidence Supporting the Conclusion

- `backend/main.py:84-102` loads encoder, index, and dataset independently.
- `backend/search/semantic.py:63-83` encodes queries, searches FAISS, and resolves returned IDs with `df.iloc[idx]`.
- `backend/evaluation/evaluation_pipeline.py:194-207, 242-251` loads current assets and uses positional lookup.
- `backend/evaluation/evaluation_pipeline_corrected.py:93-106, 171-175` uses the same positional assumption.
- `backend/evaluation/evaluation_score_diagnostic.py:94-117` uses the same positional assumption.
- Repository search found no visible `index.add`, `faiss.write_index`, `IndexIDMap`, corpus embedding-generation, or explicit vector-ID mapping implementation.
- `input_manifest.csv` records matching counts and current hashes, but no row-order evidence.

## 9. Missing Evidence

1. The original index-building script or notebook.
2. The original corpus embedding-generation script, including dataset columns and preprocessing.
3. The exact dataset snapshot used during index creation.
4. The exact encoder model name, version, weights, pooling, normalization, and runtime settings.
5. A build-time vector-ID-to-dataset-key mapping or index metadata manifest.
6. A reproducible row-order checksum linking each vector ID to a dataset record key.
7. Evidence of any filtering, sorting, deduplication, shuffling, or index reset before `index.add`.

## 10. Required Next Step Before Exact Identity Evaluation

A new index-building audit or explicit ID mapping is required before exact identity evaluation can be treated as fully valid. The preferred options are:

1. Recover and inspect the original index/embedding build process and the exact source dataset snapshot; or
2. Create a separately versioned, non-destructive rebuild that records the dataset key and row order for every vector, the encoder identity/version, preprocessing, and FAISS index metric; or
3. Attach an explicit FAISS-ID-to-dataset-key map generated at build time and verify it against the current dataset.

Until one of these evidence paths is completed, exact retrieval results should remain labelled `Not verified` for index-to-dataset identity alignment.
