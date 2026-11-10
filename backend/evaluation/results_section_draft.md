# A. Evidence Audit Table

The following audit separates values that are directly calculated from the current workspace from values that appear only in narrative documentation. `Verified` means that the value is directly supported by a current artifact or a deterministic calculation from one. `Provisional` means that the value is reported in project documentation but the underlying observations, script, or raw output are absent or internally inconsistent. `Pending Review` applies to labels whose candidate records are traceable but whose canonical equivalence has not been approved. `Not Reproducible` means that the current artifacts do not support the reported value as stated.

| Metric or claim                       |                                                         Numerical value | Source file or script                                                                 | Calculation method                                         | Verification status                                             | Notes or limitations                                                                                                                     |
| ------------------------------------- | ----------------------------------------------------------------------: | ------------------------------------------------------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| Dataset rows                          |                                                                   3,400 | `dataset/govt_schemes.csv`; direct asset inspection                                   | Number of CSV data rows                                    | Verified                                                        | The current dataset contains 3,400 rows, not 3,487 as stated in older documents.                                                         |
| FAISS index size                      |                                                           3,400 vectors | `model/scheme_index.faiss`; direct asset inspection                                   | `index.ntotal`                                             | Verified                                                        | Matches the current dataset row count.                                                                                                   |
| FAISS index implementation            |                                            `IndexFlatL2`, dimension 384 | `model/scheme_index.faiss`; direct asset inspection                                   | FAISS index metadata                                       | Verified                                                        | `metric_type=1`, which is `faiss.METRIC_L2`.                                                                                             |
| Query records                         |                                                                      64 | `backend/evaluation/test_queries.json`; `audit_evaluation_labels.py` output           | JSON record count                                          | Verified                                                        | The evaluation README and older documents say 65 or 50 in different places.                                                              |
| Positive query labels                 |                                                                      49 | `test_queries.json`; `label_audit.csv`                                                | Count of `expected_match=true`                             | Verified as source-label count                                  | Semantic correctness is not established for all positive labels.                                                                         |
| Negative query labels                 |                                                                      15 | `test_queries.json`; `label_audit.csv`                                                | Count of `expected_match=false`                            | Verified as source-label count                                  | Negative-label validity has not been independently adjudicated.                                                                          |
| Exact positive mappings               |                                                                       9 | `label_mapping_review.csv`; `mapping_category_summary.csv`                            | Count of `mapping_category=exact_mapping`                  | Verified                                                        | Exact name/slug traceability does not prove that the query's intended scheme is correct.                                                 |
| Unresolved positive mappings          |                                                                      40 | `label_audit.csv`; `label_mapping_review.csv`                                         | Count of positive labels absent as exact dataset name/slug | Verified                                                        | All 40 require manual canonical mapping or removal.                                                                                      |
| Candidates per positive label         |                                                                       3 | `label_mapping_review.csv`; `manual_review_worksheet.csv`                             | Candidate count per positive row                           | Verified                                                        | Candidate generation is traceability evidence, not semantic validation.                                                                  |
| Positive candidate records            |                                                                     147 | `positive_candidate_records.csv`                                                      | 49 positive rows x 3 candidates                            | Verified                                                        | All records have traceable dataset row indices and slugs.                                                                                |
| Untraceable candidates                |                                                                       0 | `mapping_category_summary.csv`; candidate records                                     | Count of missing/untraceable candidate records             | Verified                                                        | Traceability must not be interpreted as correctness.                                                                                     |
| Automatic approvals                   |                                                                       0 | `label_mapping_review.csv`                                                            | Count of `automatic_approval=true`                         | Verified                                                        | No label was automatically accepted.                                                                                                     |
| Completed reviewer decisions          |                                                                       0 | `manual_review_worksheet.csv`                                                         | Count of non-empty reviewer decisions                      | Verified                                                        | All 40 worksheet rows remain `pending_review`.                                                                                           |
| Diagnostic threshold values           |                        0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.5 | `evaluation_score_diagnostic.py`; `score_diagnostic_results/threshold_comparison.csv` | Threshold sweep over top squared L2 distance               | Verified as diagnostic output                                   | No threshold-selection validation protocol is documented.                                                                                |
| Binary threshold metrics              |                                                             See Table 2 | `score_diagnostic_results/threshold_comparison.csv`                                   | Acceptance rule `top_distance <= threshold`                | Verified computationally; provisional for performance claims    | The labels are not fully validated and the metric is binary acceptance, not exact retrieval identity.                                    |
| Previously reported retrieval metrics |                 82.0% accuracy, 86.5% precision, 88.9% recall, 87.7% F1 | `RESEARCH_PAPER.md`; `TECHNICAL_METRICS.md`                                           | Earlier confusion matrix, stated as 32/9/5/4 over 50       | Not Reproducible                                                | Current query population is 64, current index is L2, and current stored pipeline uses the wrong distance direction.                      |
| Speech utterances                     |                                                            488 reported | `RESEARCH_PAPER.md`; `EXPERIMENTATION_RESULTS.md`                                     | Narrative count; detailed language counts sum to 488       | Provisional                                                     | No raw utterance, transcript, or evaluation output files are present; another document states 488/528, which is internally inconsistent. |
| Speech languages                      |                                           English, Hindi, Telugu, Tamil | `RESEARCH_PAPER.md`; `backend/voice/whisper.py`; `backend/main.py`                    | Documented language set and implementation mapping         | Provisional for experiment; Verified for implementation support | The implementation supports the four languages, but the evaluated sample provenance is missing.                                          |
| Speech model                          | Whisper `small` in current startup code; `base` in experiment narrative | `backend/main.py`; `EXPERIMENTATION_RESULTS.md`                                       | Source-code configuration versus narrative report          | Contradictory                                                   | The model used for the reported speech numbers cannot be established.                                                                    |
| Speech accuracy and WER/CER           |          Multiple reported values, including 97.9%, 91.5%, 90.8%, 89.9% | `RESEARCH_PAPER.md`; `EXPERIMENTATION_RESULTS.md`; `TECHNICAL_METRICS.md`             | Narrative tables                                           | Not Reproducible                                                | No raw references or scripts calculate these metrics in the workspace; do not treat them as confirmed.                                   |
| Recommendation cases                  |                                                             52 reported | `RESEARCH_PAPER.md`; `EXPERIMENTATION_RESULTS.md`                                     | Narrative test-case count                                  | Provisional                                                     | No recommendation-evaluation output or raw relevance labels were found.                                                                  |
| Recommendation F1                     |                                                          90.3% reported | `RESEARCH_PAPER.md`; `TECHNICAL_METRICS.md`                                           | Narrative confusion-matrix calculation                     | Not Reproducible                                                | The current source code implements recommendations but does not provide the reported evaluation calculation.                             |
| Recommendation NDCG@5                 |                                                          0.876 reported | `EXPERIMENTATION_RESULTS.md`                                                          | Narrative ranking metric                                   | Not Reproducible                                                | No ranked relevance judgments or calculation output found.                                                                               |
| Conversation ratings                  |                 155 reported: 45 English, 40 Hindi, 35 Telugu, 35 Tamil | `RESEARCH_PAPER.md`; `EXPERIMENTATION_RESULTS.md`                                     | Narrative language-level counts                            | Provisional                                                     | No rating-level data, evaluator records, or scoring script found.                                                                        |
| Mean conversational score             |                                                          88.3% reported | `RESEARCH_PAPER.md`; `TECHNICAL_METRICS.md`                                           | Narrative mean of relevance/correctness/helpfulness        | Not Reproducible                                                | Reported value is retained only as a prior claim.                                                                                        |
| Latency requests                      |                                                         10,000 reported | `RESEARCH_PAPER.md`; `TECHNICAL_METRICS.md`                                           | Narrative synthetic-load description                       | Provisional                                                     | No latency log, load-test script, or request-level output found.                                                                         |
| Latency summary                       |                     P50 742 ms, mean 794 ms, P95 1,073 ms, P99 1,392 ms | `TECHNICAL_METRICS.md`                                                                | Narrative percentile table                                 | Not Reproducible                                                | Another component table reports total P95 1,230 ms and P99 1,593 ms. P90 and timeout rate are not reported.                              |
| Baseline comparison                   |                                                                    None | Evaluation directory and project search                                               | No same-dataset baseline artifact found                    | Not Available                                                   | No valid baseline can be included.                                                                                                       |

# B. Section 4: Results

## 4. Results

### 4.1 Experimental Evaluation Overview

The current workspace contains a 3,400-row government-scheme dataset and a FAISS index containing 3,400 vectors. The active retrieval asset is an `IndexFlatL2` index with vector dimension 384. The evaluation query file contains 64 records: 49 labeled positive and 15 labeled negative. These counts are directly reproducible from `backend/evaluation/test_queries.json` and its label audit.

The available evaluation evidence is uneven across system components. Semantic retrieval has query-level CSV outputs and a separate label audit. By contrast, the project contains narrative reports for speech recognition, scheme recommendation, multilingual conversation, and latency, but no corresponding raw observations or executable metric-generation artifacts. Accordingly, the results below distinguish verified artifact-derived results from provisional or pending-review reports.

The implementation supports English, Hindi, Telugu, and Tamil. The backend loads a SentenceTransformer encoder and FAISS index for retrieval, uses rule-based eligibility checks with semantic ranking for recommendations, and exposes Whisper-based speech transcription. The current startup code loads Whisper's `small` model on CPU. The experiment narrative refers to Whisper `base`, so the model associated with the historical speech figures is not established.

### 4.2 Semantic Retrieval Performance

The retrieval pipeline encodes a normalized query and searches the FAISS index for nearest scheme vectors. The current index is `IndexFlatL2` with `faiss.METRIC_L2`. FAISS therefore returns squared L2 distances: a smaller value denotes a closer match. These values are not cosine similarities or inner-product scores. The corrected diagnostic script applies the binary acceptance rule

`accepted = (top_squared_L2_distance <= threshold)`.

The production helper and the original evaluation pipeline still use a higher-is-better comparison (`score >= threshold`) and contain comments describing an inner-product index. Their stored results therefore cannot be used as current L2 retrieval performance without correction. The corrected diagnostic output is used below for binary acceptance only.

The exact-retrieval evaluator in `evaluation_pipeline_corrected.py` additionally requires the top retrieved dataset row to equal the expected dataset row. It cannot validate the current positive labels as an exact-identity population because 40 of 49 positive labels do not resolve to an exact dataset name or slug. Thus, binary acceptance and exact scheme retrieval must be reported separately.

#### 4.2.1 Confusion Matrix and Classification Metrics

At threshold 0.60, the current diagnostic output gives the following binary acceptance counts over all 64 source-labeled queries:

|                         | Predicted accepted | Predicted rejected | Total |
| ----------------------- | -----------------: | -----------------: | ----: |
| Source-labeled positive |             3 (TP) |            46 (FN) |    49 |
| Source-labeled negative |             0 (FP) |            15 (TN) |    15 |
| Total                   |                  3 |                 61 |    64 |

The corresponding metrics are accuracy 0.28125 (28.125%), precision 1.0 (100%), recall 0.061224 (6.122%), and F1-score 0.115385 (11.538%). These values are verified as calculations reproduced in `score_diagnostic_results/threshold_comparison.csv`, but they are provisional as model-performance claims because the positive labels are not fully validated. They also describe acceptance of a candidate, not whether the top candidate is the intended scheme.

| Metric          | Result at threshold 0.60 | Verification status                     |
| --------------- | -----------------------: | --------------------------------------- |
| True positives  |                        3 | Verified diagnostic; provisional labels |
| True negatives  |                       15 | Verified diagnostic; provisional labels |
| False positives |                        0 | Verified diagnostic; provisional labels |
| False negatives |                       46 | Verified diagnostic; provisional labels |
| Accuracy        |                  28.125% | Verified diagnostic; provisional labels |
| Precision       |                 100.000% | Verified diagnostic; provisional labels |
| Recall          |                   6.122% | Verified diagnostic; provisional labels |
| F1-score        |                  11.538% | Verified diagnostic; provisional labels |

The previously reported 50-query confusion matrix of TP=32, TN=9, FP=5, and FN=4, together with 82.0% accuracy, 86.5% precision, 88.9% recall, and 87.7% F1-score, is not reproducible from the current artifacts. It uses a different population size, conflicts with the current 64-row query file, and appears to use the opposite distance interpretation. It is therefore not reported as a current result.

#### 4.2.2 Retrieval Threshold Analysis

The corrected diagnostic sweep evaluated ten thresholds. The output is reproduced below without selecting an optimal threshold.

| Threshold | Accuracy | Precision |   Recall | F1-score |  TP |  TN |  FP |  FN |
| --------: | -------: | --------: | -------: | -------: | --: | --: | --: | --: |
|      0.20 | 23.4375% |    0.0000 |   0.0000 |   0.0000 |   0 |  15 |   0 |  49 |
|      0.30 | 23.4375% |    0.0000 |   0.0000 |   0.0000 |   0 |  15 |   0 |  49 |
|      0.40 | 23.4375% |    0.0000 |   0.0000 |   0.0000 |   0 |  15 |   0 |  49 |
|      0.50 | 23.4375% |    0.0000 |   0.0000 |   0.0000 |   0 |  15 |   0 |  49 |
|      0.60 | 28.1250% |    1.0000 | 0.061224 | 0.115385 |   3 |  15 |   0 |  46 |
|      0.70 | 40.6250% |    1.0000 | 0.224490 | 0.366667 |  11 |  15 |   0 |  38 |
|      0.80 | 65.6250% |  0.965517 | 0.571429 | 0.717949 |  28 |  14 |   1 |  21 |
|      1.00 | 90.6250% |  0.957447 | 0.918367 | 0.937500 |  45 |  13 |   2 |   4 |
|      1.20 | 90.6250% |  0.890909 | 1.000000 | 0.942308 |  49 |   9 |   6 |   0 |
|      1.50 | 78.1250% |  0.777778 | 1.000000 | 0.875000 |  49 |   1 |  14 |   0 |

These thresholds are diagnostic values, not validated operating points. No held-out validation set, preregistered selection rule, or independent threshold-selection procedure is present. The apparent maximum diagnostic F1-score at 1.20 must not be called optimal because it is based on provisional labels and binary acceptance rather than verified exact retrieval.

#### 4.2.3 Ground-Truth Label Validation

The label audit contains 49 positive records. Nine expected schemes resolve exactly to a current dataset name or slug. The remaining 40 positive records do not resolve exactly and were assigned three traceable dataset candidates each, producing 147 candidate records. Candidate traceability is complete in the audit: zero candidates are untraceable. However, traceability only establishes that a candidate row exists; it does not establish semantic equivalence between the query intent and that row.

No candidate was automatically approved, and the 40-row manual-review worksheet contains zero completed reviewer decisions. All unresolved mappings therefore remain pending review. The correct interpretation is that the current evaluation population is a source-labeled diagnostic set with partially validated identity, not a fully verified exact-retrieval benchmark.

### 4.3 Multilingual Speech Recognition Performance

The implementation provides speech transcription for English, Hindi, Telugu, and Tamil through a Whisper endpoint. The backend startup path loads Whisper `small` on CPU, while the experimentation document reports Whisper `base`; the experiment configuration is consequently unresolved.

Project documents report 488 speech utterances across the four languages and clean-condition language-level values of 97.9% for English, 91.5% for Hindi, 90.8% for Telugu, and 89.9% for Tamil. These values are not independently reproducible from the current workspace: no utterance files, reference transcripts, transcription outputs, WER/CER calculation script, or per-condition result files were found. Another document reports 488/528 for the overall average, which conflicts with the stated 488-utterance population. The reported speech values are therefore provisional historical claims and are not treated as confirmed Results.

The available project text uses accuracy, WER, and CER terminology, but the underlying calculations are absent. No aggregate or per-language speech metric is confirmed for publication from the current artifacts.

### 4.4 Government Scheme Recommendation Performance

The recommendation implementation constructs a profile query from age, gender, state, occupation, category, income, student or farmer status, and disability status. It then applies state compatibility and rule-based checks to semantically retrieved candidates before ranking the results. This implementation behavior is verified from the current source code.

Project documents report 52 profile-based recommendation cases, an F1-score of 90.3%, an NDCG@5 of 0.876, an MRR of 0.912, and a MAP of 0.898. The workspace contains no recommendation case file, relevance judgments, eligibility ground-truth table, or script that calculates these values. The definition of a relevant recommendation is therefore not verifiable, and the reported metrics cannot be presented as confirmed results. In particular, the label audit for semantic retrieval does not validate recommendation relevance labels.

| Evaluation item         | Result | Verification status                     |
| ----------------------- | -----: | --------------------------------------- |
| Recommendation cases    |     52 | Provisional historical report           |
| Recommendation F1-score |  90.3% | Not reproducible from current artifacts |
| NDCG@5                  |  0.876 | Not reproducible from current artifacts |
| MRR                     |  0.912 | Not reproducible from current artifacts |
| MAP                     |  0.898 | Not reproducible from current artifacts |

### 4.5 Multilingual Conversational Evaluation

The implementation supports language selection for English, Hindi, Telugu, and Tamil and includes retrieval-grounded chat, section-specific answers, web fallback, and conversation state for yes/no follow-up behavior. These capabilities are verified in the source code and tests, but functional support is not a quality score.

The project documentation reports 155 language-level ratings: 45 English, 40 Hindi, 35 Telugu, and 35 Tamil. It also reports a mean score of 88.3%, with relevance, correctness, and helpfulness as evaluation criteria. The evaluator type is described in the documentation as native-speaker evaluation in one report, but the rating-level records, evaluator assignments, rating scale, scoring rubric, and calculation script are absent. The 155-rating and 88.3% values are consequently retained as previously reported, not independently reproduced results. The mean represents the reported aggregate of the stated conversational criteria; its exact weighting cannot be verified.

### 4.6 System Latency and Computational Performance

The project documentation reports a synthetic benchmark of 10,000 requests and gives a full-chat mean of 794 ms, P50 of 742 ms, P95 of 1,073 ms, and P99 of 1,392 ms. It also reports a search-only P99 of 189 ms. These values refer to different scopes: full-chat latency includes the LLM path, whereas search-only latency excludes generation. P90 and timeout rate are not reported.

The latency values remain provisional because no request-level log, load-test script, hardware capture, or percentile calculation output is present. There is also an internal contradiction: a component breakdown in the same project documentation reports total P95 of 1,230 ms and total P99 of 1,593 ms, rather than 1,073 ms and 1,392 ms. The reported 10,000-request P95 should therefore not be stated as a verified performance result.

| Latency scope                    |    Sample size |            P50 |           Mean |            P90 |            P95 |      P99 |   Timeout rate | Verification status                     |
| -------------------------------- | -------------: | -------------: | -------------: | -------------: | -------------: | -------: | -------------: | --------------------------------------- |
| Full chat, previously reported   |         10,000 |         742 ms |         794 ms | [NOT REPORTED] |       1,073 ms | 1,392 ms | [NOT REPORTED] | Provisional and internally contradicted |
| Search-only, previously reported | [NOT REPORTED] | [NOT REPORTED] | [NOT REPORTED] | [NOT REPORTED] | [NOT REPORTED] |   189 ms | [NOT REPORTED] | Provisional                             |

### 4.7 Error Analysis

The current artifacts support the following error and data-quality observations. At the diagnostic threshold of 0.60, the binary acceptance output contains 46 false negatives, zero false positives, three true positives, and 15 true negatives under the source labels. These are not exact retrieval error counts because the positive labels are only partially validated.

The label audit identifies 40 positive-label identity issues. The unresolved cases include near-duplicate or related scheme names, such as state-specific old-age pension records, multiple housing records, similarly named employment and training schemes, maternity-benefit variants, and several education or scholarship records. The manual worksheet shows three candidates per unresolved positive query, but all reviewer decisions remain pending. These cases provide direct evidence of possible label ambiguity and similar-name effects; they do not establish model error by themselves.

The current retrieval outputs also show that many top candidates are semantically related but not identical to the expected label. Examples include state-specific pension or health schemes, related housing schemes, and alternative training or welfare schemes. Since the source evaluation defines a positive query by an expected identity that is absent for 40 records, it is not valid to convert these cases into false positives or false negatives without completed canonical review.

The project documents additionally report counts for speech failures, hallucinations, database misses, and ambiguous queries, but those counts are not supported by current raw logs. They are therefore omitted from confirmed error totals.

### 4.8 Baseline Comparison

No valid baseline was evaluated on the same current dataset, query population, labels, and metrics. The narrative comparison tables for BM25, hosted vector databases, speech APIs, and alternative language models do not include reproducible same-dataset experiment artifacts. A comparative performance claim is therefore not included.

### 4.9 Summary of Results

| Evaluation area             |                      Evaluation size | Metric                                                  |                                     Result | Verification status                                  |
| --------------------------- | -----------------------------------: | ------------------------------------------------------- | -----------------------------------------: | ---------------------------------------------------- |
| Dataset and index           |         3,400 schemes; 3,400 vectors | Index type and distance                                 | `IndexFlatL2`; squared L2; lower is closer | Verified                                             |
| Semantic retrieval labels   | 64 queries: 49 positive, 15 negative | Label population                                        |                   49 positive, 15 negative | Verified as source labels; semantic validity pending |
| Binary retrieval acceptance |                           64 queries | Accuracy at threshold 0.60                              |                                    28.125% | Verified diagnostic; provisional labels              |
| Binary retrieval acceptance |                           64 queries | Precision / recall / F1 at threshold 0.60               |                100.000% / 6.122% / 11.538% | Verified diagnostic; provisional labels              |
| Label validation            |                  49 positive queries | Exact mappings / unresolved mappings                    |                                     9 / 40 | Verified; 40 pending review                          |
| Candidate traceability      |                          147 records | Untraceable / automatic approvals / completed decisions |                                  0 / 0 / 0 | Verified                                             |
| Speech recognition          |              488 reported utterances | Per-language accuracy                                   |        97.9%, 91.5%, 90.8%, 89.9% reported | Provisional; not independently reproduced            |
| Recommendation              |                    52 reported cases | F1 / NDCG@5                                             |                     90.3% / 0.876 reported | Not reproducible                                     |
| Multilingual conversation   |                 155 reported ratings | Mean score                                              |                             88.3% reported | Provisional; not independently reproduced            |
| Full-chat latency           |             10,000 reported requests | Mean / P95 / P99                                        |      794 ms / 1,073 ms / 1,392 ms reported | Provisional and internally contradicted              |
| Baseline comparison         |                        Not available | Same-dataset comparison                                 |                              Not performed | Not available                                        |

Overall, the current artifacts verify the system configuration, the query and label populations, the L2 distance interpretation, the diagnostic threshold outputs, and the label-audit state. They do not support a publication claim of 82.0% retrieval accuracy, 90.3% recommendation F1, 88.3% conversational mean score, or 1,073 ms verified P95 latency. Those values require reconstruction from raw observations under a corrected and documented evaluation protocol.

# C. Contradictions Between `RESEARCH_PAPER.md` and Current Artifacts

1. `RESEARCH_PAPER.md` describes 50 labeled retrieval queries, while the current `test_queries.json` and audit contain 64 queries: 49 positive and 15 negative.
2. `RESEARCH_PAPER.md` reports 82.0% accuracy, 86.5% precision, 88.9% recall, and 87.7% F1 from a 50-query confusion matrix. The current L2 diagnostic output uses 64 queries and does not reproduce those values.
3. The paper calls the retrieval output a similarity score and describes a threshold of 0.60, while the current FAISS asset is `IndexFlatL2`, where lower squared L2 distance is better.
4. `backend/config/settings.py` documents `IndexFlatIP` and a higher-is-better threshold, while the actual index is `IndexFlatL2`; `backend/search/semantic.py` and `backend/chat/processor.py` also use higher-is-better comparisons.
5. The original stored evaluation summary contains 64-query counts (49 positive, 15 negative) but was generated by the original higher-is-better pipeline and reports zero true positives at thresholds 0.20-0.60. It is not equivalent to the corrected L2 diagnostic.
6. The paper states 3,400-plus schemes in some places and 3,487 schemes in its experimental descriptions. The current CSV and index each contain 3,400.
7. The paper presents the speech figures as reported clean-condition results, while the source documents disagree on speech populations and one document reports an impossible-looking 488/528 overall denominator. No raw speech artifacts resolve this.
8. The current implementation loads Whisper `small`, while the experimentation document describes Whisper `base`. The model used for the reported speech metrics is not established.
9. The paper presents recommendation F1=90.3% and NDCG@5=0.876, but no current recommendation labels or metric outputs exist.
10. The paper presents 155 ratings and an 88.3% mean as evaluation results, but no rating-level evidence or scoring script exists.
11. The paper reports 10,000 latency queries with P95=1,073 ms and P99=1,392 ms. Another project table reports total P95=1,230 ms and P99=1,593 ms; no raw latency log is available.
12. The paper implies a valid retrieval result and baseline-like performance claims, but no same-dataset baseline execution is present.
13. The paper reports threshold testing in different ranges across documents: 0.50-0.80, 0.50-0.80 in increments of 0.05, and 0.20-0.60. The current diagnostic output uses 0.20-0.80 plus 1.0, 1.2, and 1.5.

# D. Missing Experiments or Files Required Before Publication

1. A corrected exact-retrieval evaluation using the current `IndexFlatL2` index, squared-distance acceptance, and a fully adjudicated expected scheme identity for every query.
2. A documented validation split or prespecified threshold-selection protocol; the current threshold sweep is diagnostic only.
3. A canonical label file recording reviewer decisions for all 40 unresolved positive queries, including rationale and approved dataset slug.
4. Raw speech audio or a reproducible manifest, reference transcripts, Whisper model/version, decoding settings, predicted transcripts, and scripts for WER, CER, and the project's accuracy definition.
5. A recommendation evaluation file containing all 52 profiles, eligibility/relevance ground truth, returned rankings, and scripts for precision, recall, F1, NDCG@5, MRR, and MAP.
6. Conversation rating records with evaluator identifiers or anonymized evaluator groups, rating scale, rubric, language, query, response, and aggregation code for the 155-rating claim.
7. Request-level latency logs and the exact load-generation script, including hardware, concurrency, network conditions, timeout definition, successful-request count, and percentile calculation. The log must resolve the conflicting P95/P99 tables.
8. A same-dataset baseline implementation and output, such as BM25 or another explicitly selected comparator, using the same query set, label policy, and evaluation metrics.
9. A definitive dataset and index manifest recording row count, index row alignment, embedding model/version, preprocessing, and index metric.
10. Reproduction instructions that work from a clean environment and preserve the corrected L2 semantics.
11. If confidence intervals or significance claims are retained, raw observations and a prespecified statistical analysis plan are required. No such analysis is confirmed by the current artifacts.

# E. Recommended Next-Step Checklist

- [ ] Freeze the current dataset, index, encoder, and query-file versions with hashes.
- [ ] Correct the application and evaluation threshold semantics for squared L2 distance, or explicitly convert distances to a documented similarity measure.
- [ ] Complete manual review of all 40 unresolved positive labels; approve, remap, or remove each record.
- [ ] Re-run exact retrieval and binary acceptance metrics after label adjudication.
- [ ] Select a threshold only on documented validation data, then evaluate once on a held-out test set.
- [ ] Reconstruct speech evaluation with fixed Whisper model/version, raw references, and WER/CER scripts.
- [ ] Reconstruct the 52-case recommendation evaluation with explicit eligibility and relevance definitions.
- [ ] Reconstruct the 155-rating conversational evaluation with a fixed rubric and aggregation method.
- [ ] Re-run the 10,000-request latency benchmark and publish request-level logs plus P50, mean, P90, P95, P99, and timeout rate.
- [ ] Evaluate at least one baseline on the same data and metrics before making comparative claims.
- [ ] Update the paper only after each numerical claim has a source artifact and a reproducible calculation path.
