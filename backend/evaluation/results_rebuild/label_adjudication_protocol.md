# Label Adjudication Protocol

## Purpose and Scope

This protocol governs manual review of the 40 unresolved positive queries listed in `backend/evaluation/label_audit_reports/manual_review_worksheet.csv`. It is a review procedure, not an automatic relabeling rule. The existing `original_expected_scheme` value is a source label and must not be silently accepted as ground truth.

## Workflow Authority

`backend/evaluation/results_rebuild/label_decisions.csv` is the authoritative decision record for this adjudication workflow. Manual decisions, verified slugs, rationales, evidence references, reviewer identities, confidence values, and second-review outcomes must be entered in that CSV. The Markdown `reviewer_adjudication_report.md` is a read-only review aid generated from the worksheet, dataset, and template; editing the report does not record a decision.

Broad queries may legitimately receive `ambiguous`; reviewers must not force a single scheme merely to complete the table. An unverified source label is not ground truth. FAISS rank and FAISS distance are retrieval outputs, not semantic evidence, and cannot justify a decision by themselves.

The allowed `second_review_status` values are `pending`, `complete`, and `unresolved`. No other status is valid.

Status and decision consistency rules:

- A blank decision is an unreviewed row and must remain `pending`.
- A nonblank decision with `pending` status is incomplete and must not be treated as a completed label.
- `complete` requires an allowed decision plus rationale, evidence reference, reviewer ID, and confidence.
- `unresolved` requires an allowed decision plus rationale, evidence reference, reviewer ID, and confidence.
- These rules do not require every candidate row to be reviewed before the workflow can continue; partially reviewed queries must be reported.

## 1. Review Objective

For each query, determine whether the query refers to a specific government scheme and, only when the available evidence supports that conclusion, identify the correct current record in `dataset/govt_schemes.csv`.

The reviewer must distinguish:

- A query that identifies one current dataset scheme.
- A query that describes a policy area or broad need rather than one scheme.
- A query that can refer to multiple schemes.
- A query whose intended scheme is absent from the current dataset.
- A query requiring evidence outside the available project materials.

The objective is to establish a defensible canonical label, not to maximize the number of accepted matches.

## 2. Allowed Decisions

Use exactly one decision for each query-candidate review row:

| Decision                       | Definition                                                                                                                                                                                                                                                                         |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `verified_match`               | The query meaning identifies the candidate scheme specifically, and the required evidence supports that mapping. Record the candidate's current dataset slug in `verified_dataset_slug`. A match is not verified merely because the name is similar or the candidate is traceable. |
| `verified_no_match`            | The query is meaningful and reviewable, but the candidate does not represent the query's intended scheme. Use this only when the available evidence supports rejecting that candidate; it does not necessarily mean that the query has no valid scheme anywhere.                   |
| `ambiguous`                    | The query reasonably refers to two or more candidates, or its wording does not identify one scheme strongly enough to choose a single candidate. Do not select a canonical slug unless a second review resolves the ambiguity.                                                     |
| `dataset_missing`              | The query identifies a specific scheme or policy whose correct record cannot be found in the current dataset after reviewing the available candidate records. Record the evidence for absence and leave `verified_dataset_slug` blank.                                             |
| `needs_external_source_review` | The available project files are insufficient to decide. Use this when official-source evidence, a current scheme document, state/central scope information, or another authoritative source is required. This is not an approval and must remain unresolved until reviewed.        |

A query may produce multiple candidate rows in the template. Decisions are recorded at candidate level, while the canonical label is a query-level interpretation derived from the reviewed candidate rows. Candidate-level decisions should explain why each candidate was accepted, rejected, or left unresolved. At most one candidate may be assigned `verified_match` for a query; multiple verified matches are invalid until resolved. Multiple valid interpretations should normally result in `ambiguous` or a query-level decision that the wording is broad.

## 3. Required Evidence for `verified_match`

Before accepting a match, record evidence for all applicable elements below in `rationale` and `evidence_reference`:

1. **Query meaning:** Explain the concrete need, named scheme, beneficiary group, benefit, or policy described by the query.
2. **Candidate identity:** Cite the candidate dataset slug and scheme name, and explain why the candidate description matches the query rather than merely sharing words.
3. **Eligibility or benefits:** Cite relevant eligibility, benefit, or scope information from the current dataset record when it supports the interpretation.
4. **Official-source evidence already available:** Cite an official-source URL, document, or other authoritative evidence only when it already exists in the project files. Do not invent a URL, quotation, policy relationship, or synonym.

A reviewer must not approve a match when any required identity relationship is based only on a name-similarity score, token overlap, sequence similarity, candidate traceability, FAISS rank, or FAISS distance.

## 4. Language and Wording Policy

### Synonyms and spelling variations

Accept a synonym or spelling variation only when the candidate's description, eligibility, benefits, scope, or existing official-source evidence confirms the intended identity. Common wording alone is insufficient. Preserve the query text and candidate name as supplied; explain the normalization in the rationale.

### Abbreviations

Expand an abbreviation only when the project materials or an authoritative source already establishes that expansion. Do not infer that a shared acronym refers to one scheme when multiple expansions are possible.

### Translations and transliterations

Treat translated or transliterated wording as an interpretation to be evidenced. Confirm that the translated concept, beneficiary group, and benefit correspond to the candidate record. Do not treat language similarity or a translation guess as proof.

### Broad queries

Queries such as requests for help for a group, sector, or need may describe multiple schemes. If the wording does not identify one scheme, use `ambiguous`, `dataset_missing`, or `needs_external_source_review` as appropriate rather than forcing the source label onto one candidate.

## 5. Multiple Schemes and Missing Records

If a query refers to multiple schemes, record `ambiguous` and list the competing candidates and the reason one cannot be selected. If the query is broad but the evidence identifies a family of programs rather than a canonical record, do not convert the broad query into an exact identity match.

If the query clearly identifies a specific scheme but no current candidate or dataset record represents it, use `dataset_missing`. The reviewer must explain why the query identifies a specific scheme and cite evidence that the intended record is absent from the current dataset after reviewing the available candidates. Rejecting all three retrieved candidates is not, by itself, evidence that the dataset lacks the intended scheme. Do not treat the absence of a candidate name as proof that the scheme is absent from all official sources.

Use `needs_external_source_review` when deciding requires an official source that is not already available in the project. This outcome is preferable to speculation.

Presence of a rationale or evidence reference satisfies a recording requirement only; it does not prove that the evidence is sufficient. Reviewers remain responsible for assessing evidence quality under this protocol.

## 6. Rationale, Evidence, and Confidence

For every reviewed row:

- `rationale` must state the semantic reasoning and the decision-specific reason.
- `evidence_reference` is required for every nonblank decision, including `ambiguous` and `dataset_missing`. It must identify exact project-file paths, dataset fields, row indices, or already available official-source references. Use `Not verified` only when the protocol permits an unresolved evidence state; do not fill it automatically.
- `confidence` must be one of `low`, `medium`, or `high`, with a short explanation in `notes` when useful. Confidence describes the reviewer's certainty in the evidence assessment; it is not ground truth and must never override missing evidence.
- `reviewer_id` must identify the reviewer according to the study's privacy policy. Do not use confidence as a substitute for a second review.
- `second_review_status` must remain `pending` until an independent second review is completed or an explicit unresolved outcome is recorded.

No reviewer may infer a decision from the existing `expected_scheme`, `reviewer_decision`, candidate rank, or similarity score without documenting independent semantic evidence.

## 7. Similarity and Traceability Restrictions

Candidate string similarity fields (`name_similarity_score`, token Jaccard similarity, and sequence similarity) are retrieval aids for review only. Candidate traceability proves that a dataset row and slug can be located; it does not prove semantic correctness. Neither may be described as FAISS similarity, and neither is sufficient for `verified_match`.

FAISS distance or rank, when available, is also not a substitute for semantic adjudication. The current audit candidate artifact records FAISS distance as unavailable.

## 8. Index-Alignment Limitation

Manual label adjudication determines the relationship between query meaning and a dataset record. It does not prove that FAISS vector ID `i` was built from dataset row `i`. The separate index-alignment investigation concludes that dataset/index row alignment is `Not verified`; equal row/vector counts and positional `dataframe.iloc` lookups are not proof of build-time alignment.

Do not use a successful label decision as evidence that the FAISS index-to-dataset mapping is correct.

## 9. Disagreements and Second Review

A disagreement between reviewers requires one of the following before the label can be treated as resolved:

1. A second independent review that documents the evidence and selects one allowed decision; or
2. An explicit unresolved decision of `ambiguous` or `needs_external_source_review`, with the disagreement recorded in `notes` and `rationale`.

The original reviewer must not silently overwrite a disagreement. If reviewers disagree about a canonical slug, leave `verified_dataset_slug` blank until the disagreement is resolved by documented evidence.

## 10. No Silent Inference Rule

No decision should be silently inferred from the existing source label, expected scheme name, candidate ordering, similarity score, traceability flag, or prior evaluation result. Every nonblank decision must have a reviewer, rationale, evidence reference, and review status. Blank fields mean that review has not occurred; they do not mean approval or rejection.

## Review Completion Criteria

A query is ready for use as an exact-identity evaluation label only when:

- The decision is documented using one allowed value.
- The rationale and evidence reference are complete.
- Any selected slug is a current dataset slug and is supported by semantic evidence.
- Required second review is complete or the unresolved status is explicitly recorded.
- The decision is not based solely on string similarity, traceability, rank, or distance.
- Index-to-dataset alignment remains separately documented and is not assumed from this review.
