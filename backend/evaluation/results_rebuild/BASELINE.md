# Evaluation Rebuild Baseline

**Baseline status:** Verified only for facts directly observable in the current workspace. Historical claims without raw supporting artifacts are marked `Provisional`, `Contradictory`, `Unsupported`, or `Not verified`.

## 1. Dataset and Retrieval Assets

| Item                        | Verified baseline fact                                                  | Source                                                               | Status                                               |
| --------------------------- | ----------------------------------------------------------------------- | -------------------------------------------------------------------- | ---------------------------------------------------- |
| Dataset location            | `dataset/govt_schemes.csv`                                              | Current workspace file                                               | Verified                                             |
| Dataset row count           | 3,400 rows                                                              | Direct CSV inspection                                                | Verified                                             |
| FAISS index location        | `model/scheme_index.faiss`                                              | Current workspace file                                               | Verified                                             |
| FAISS index type            | `IndexFlatL2`                                                           | Direct FAISS index inspection                                        | Verified                                             |
| FAISS metric                | `faiss.METRIC_L2` (`metric_type=1`)                                     | Direct FAISS index inspection; `evaluation_score_diagnostic.py`      | Verified                                             |
| Distance interpretation     | FAISS returns squared L2 distances; lower distance means a closer match | `evaluation_score_diagnostic.py`; `evaluation_pipeline_corrected.py` | Verified                                             |
| Embedding/index dimension   | 384                                                                     | Direct FAISS index inspection (`index.d`)                            | Verified                                             |
| Vectors in index            | 3,400                                                                   | Direct FAISS index inspection (`index.ntotal`)                       | Verified                                             |
| Dataset/index row alignment | Counts match: 3,400 CSV rows and 3,400 index vectors                    | Direct inspection                                                    | Verified for count; exact row alignment Not verified |
| Encoder file                | `model/semantic_encoder.pkl` exists                                     | Current workspace file check                                         | Verified                                             |
| Encoder model name/version  | Not verified                                                            | No authoritative model manifest identified                           | Not verified                                         |

## 2. Evaluation Query Population

| Item                         | Verified baseline fact                                       | Source                                                 | Status                                                            |
| ---------------------------- | ------------------------------------------------------------ | ------------------------------------------------------ | ----------------------------------------------------------------- |
| Evaluation query file        | `backend/evaluation/test_queries.json`                       | Current workspace file                                 | Verified                                                          |
| Query count                  | 64 records                                                   | Direct JSON count; `audit_evaluation_labels.py` output | Verified                                                          |
| Positive source labels       | 49 records with `expected_match=true`                        | Direct JSON count; `label_audit.csv`                   | Verified as source-label count                                    |
| Negative source labels       | 15 records with `expected_match=false`                       | Direct JSON count; `label_audit.csv`                   | Verified as source-label count                                    |
| Duplicate query count        | No duplicate query rows reported by the current audit output | `label_audit.csv`                                      | Verified from audit field; independent recomputation Not verified |
| Exact retrieval ground truth | Not verified for the full query set                          | Current label audit and manual review status           | Not verified                                                      |

## 3. Label-Audit Status

| Item                               | Verified baseline fact                                                                     | Source                                                           | Status                                                    |
| ---------------------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- | --------------------------------------------------------- |
| Exact positive mappings            | 9                                                                                          | `label_mapping_review.csv`; `mapping_category_summary.csv`       | Verified as exact name/slug traceability                  |
| Unresolved positive mappings       | 40                                                                                         | `label_mapping_review.csv`; `mapping_category_summary.csv`       | Verified; Pending review                                  |
| Candidates per positive query      | 3                                                                                          | `label_mapping_review.csv`; `manual_review_worksheet.csv`        | Verified for candidate generation                         |
| Candidate records                  | 147                                                                                        | `positive_candidate_records.csv`                                 | Verified as record count                                  |
| Untraceable candidates             | 0                                                                                          | `positive_candidate_records.csv`; `mapping_category_summary.csv` | Verified for traceability                                 |
| Automatic approvals                | 0                                                                                          | `label_mapping_review.csv`; `mapping_category_summary.csv`       | Verified                                                  |
| Completed reviewer decisions       | 0                                                                                          | `manual_review_worksheet.csv`                                    | Verified                                                  |
| Manual-review row status           | 40 rows marked `pending_review`                                                            | `manual_review_worksheet.csv`                                    | Verified                                                  |
| Candidate name scores              | `name_similarity_score`, `token_jaccard_similarity`, and `sequence_similarity` are present | `positive_candidate_records.csv`                                 | Verified as string/name comparison fields                 |
| Candidate FAISS distance           | Reported as `unavailable in label_audit.csv` in candidate records                          | `positive_candidate_records.csv`                                 | Verified absence of usable candidate-level FAISS distance |
| Semantic correctness of candidates | Not verified                                                                               | No completed reviewer decisions or source evidence               | Not verified                                              |
| Ground truth for all 49 positives  | Not verified                                                                               | 40 mappings remain unresolved                                    | Not verified                                              |

Candidate traceability must not be interpreted as semantic correctness. The candidate name-similarity fields must not be described as FAISS similarity.

## 4. Existing Evaluation Scripts

| Script                                                 | Observed role                                            | Important baseline status                                                                                         |
| ------------------------------------------------------ | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `backend/evaluation/evaluation_pipeline.py`            | Legacy FAISS threshold evaluation and CSV export         | Uses higher-is-better score logic; not authoritative for the current L2 index                                     |
| `backend/evaluation/evaluation_pipeline_corrected.py`  | Non-destructive exact-retrieval evaluation for L2 index  | Requires exact expected dataset identities; cannot establish results while 40 positive mappings remain unresolved |
| `backend/evaluation/evaluation_score_diagnostic.py`    | Current L2 squared-distance binary-acceptance diagnostic | Uses `top_distance <= threshold`; diagnostic only, not a validated operating-point evaluation                     |
| `backend/evaluation/audit_evaluation_labels.py`        | Audits source labels and dataset identity resolution     | Establishes traceability and review needs, not semantic correctness                                               |
| `backend/evaluation/report_label_audit.py`             | Produces label-audit reports                             | Existing reporting utility; output status is artifact-specific                                                    |
| `backend/evaluation/create_manual_review_worksheet.py` | Creates manual-review worksheet                          | Reviewer decisions are currently incomplete                                                                       |
| `backend/evaluation/run_evaluation.py`                 | Runs the legacy evaluation pipeline                      | Not authoritative for current L2 semantics                                                                        |
| `backend/evaluation/test_cpu_setup.py`                 | Checks dependencies and CPU/resource setup               | Environment check, not a model-quality evaluation                                                                 |

## 5. Existing Output Directories and Files

| Location                                                    | Current contents                                                                                                                                          | Status                                                                                                                     |
| ----------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `backend/evaluation/results/`                               | `evaluation_summary.csv`, `evaluation_results_detailed.csv`, `ambiguous_matches.csv`                                                                      | Existing legacy evaluation outputs; metric interpretation is affected by higher-is-better L2 mismatch                      |
| `backend/evaluation/score_diagnostic_results/`              | `score_distribution_by_query.csv`, `score_distribution_statistics.csv`, `threshold_comparison.csv`                                                        | Existing L2 diagnostic outputs; reproducible as binary acceptance against source labels, but labels are not fully verified |
| `backend/evaluation/label_audit_reports/`                   | `label_mapping_review.csv`, `manual_review_by_issue.csv`, `manual_review_worksheet.csv`, `mapping_category_summary.csv`, `positive_candidate_records.csv` | Existing label-audit and manual-review outputs; unresolved mappings remain pending                                         |
| `backend/evaluation/results_section_draft.md`               | Previous Results draft                                                                                                                                    | Existing prior draft; not modified by this rebuild setup                                                                   |
| `backend/evaluation/results_section_verification_report.md` | Prior verification report                                                                                                                                 | Existing prior audit; not modified by this rebuild setup                                                                   |

## 6. Existing Metric and Claim Status

| Claim or metric                                                                                                 | Current status                             | Verified source or reason                                                                                                                              |
| --------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Current dataset size is 3,400                                                                                   | Verified                                   | Direct CSV inspection                                                                                                                                  |
| Current index is 384-dimensional `IndexFlatL2`                                                                  | Verified                                   | Direct FAISS inspection                                                                                                                                |
| Current query population is 64: 49 positive and 15 negative source labels                                       | Verified as source-label counts            | `test_queries.json`, `label_audit.csv`                                                                                                                 |
| Nine exact positive mappings and 40 unresolved mappings                                                         | Verified                                   | Label-audit reports                                                                                                                                    |
| 147 candidate records, zero untraceable candidates, zero automatic approvals, zero completed reviewer decisions | Verified                                   | Label-audit reports                                                                                                                                    |
| Binary threshold diagnostics                                                                                    | Verified as diagnostic output only         | `score_diagnostic_results/threshold_comparison.csv`; uses squared L2 and source labels                                                                 |
| Earlier 50-query retrieval results: 82.0% accuracy, 86.5% precision, 88.9% recall, 87.7% F1                     | Not reproducible from current artifacts    | `RESEARCH_PAPER.md` and `TECHNICAL_METRICS.md` report them, but current population/index semantics differ                                              |
| Threshold 0.60 is optimal                                                                                       | Unsupported                                | No documented validation split or prespecified threshold-selection procedure                                                                           |
| Threshold 1.20 is optimal                                                                                       | Unsupported                                | It has the largest F1 among listed diagnostics, but labels are unresolved and no validation procedure exists                                           |
| Speech population and accuracy figures                                                                          | Provisional and contradictory              | Narrative documents report values, but raw audio, transcripts, and metric scripts are absent; model documentation differs                              |
| Recommendation cases and metrics                                                                                | Provisional, contradictory, or unsupported | Narrative documents report them, but raw profiles, relevance labels, rankings, and metric scripts are absent; documented F1 arithmetic is inconsistent |
| Conversation ratings and mean score                                                                             | Provisional or unsupported                 | Narrative documents report them, but rating-level records and aggregation script are absent                                                            |
| Latency population and percentiles                                                                              | Provisional and contradictory              | Narrative documents report them, but request logs and load-test outputs are absent; P95/P99 tables conflict                                            |
| Baseline comparison                                                                                             | Unsupported / Not verified                 | No comparable same-dataset, same-label, same-metric baseline output exists                                                                             |
| Statistical significance or confidence intervals                                                                | Not verified                               | No supporting raw observations or statistical analysis artifact identified                                                                             |

## 7. Baseline Constraints for the Rebuild

1. Treat `IndexFlatL2` output as squared L2 distance, not cosine similarity or inner-product similarity.
2. Keep binary acceptance metrics separate from exact scheme-identity metrics.
3. Use source labels only as provisional labels until manual review resolves canonical mappings.
4. Do not call any threshold optimal without a documented validation procedure.
5. Do not use candidate name-similarity scores as FAISS scores.
6. Do not claim speech, recommendation, conversational, or latency metrics as verified without raw observations and calculation scripts.
7. Do not include a baseline comparison until a comparable baseline is evaluated on the same population and metrics.
8. Use `Not verified` rather than infer missing model versions, hardware, sampling procedures, timeout rates, or row alignment.
9. Generate all rebuild outputs inside `backend/evaluation/results_rebuild/` without overwriting existing artifacts.
