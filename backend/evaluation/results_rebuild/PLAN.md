# Results Rebuild Workspace Plan

## Purpose

Rebuild the paper Results section from current, source-backed evaluation evidence without modifying existing source code, datasets, labels, papers, or previous experiment outputs.

## Immutable Inputs

The rebuild should read, but not overwrite:

- `dataset/govt_schemes.csv`
- `model/scheme_index.faiss`
- `model/semantic_encoder.pkl`
- `backend/evaluation/test_queries.json`
- `backend/evaluation/label_audit.csv`
- `backend/evaluation/label_audit_reports/`
- `backend/evaluation/results/`
- `backend/evaluation/score_diagnostic_results/`
- Project documentation containing historical claims, including `RESEARCH_PAPER.md`, `EXPERIMENTATION_RESULTS.md`, and `TECHNICAL_METRICS.md`

## Existing Evaluation Entry Points

- `evaluation_pipeline.py`: legacy threshold evaluation; currently assumes higher-is-better scores.
- `evaluation_pipeline_corrected.py`: non-destructive L2-aware evaluation; validates exact expected dataset identities before running.
- `evaluation_score_diagnostic.py`: L2 squared-distance binary-acceptance diagnostic.
- `audit_evaluation_labels.py`: source-label and dataset-identity audit.
- `report_label_audit.py`: label-audit reporting utility.
- `create_manual_review_worksheet.py`: manual-review worksheet generation.
- `run_evaluation.py`: legacy evaluation runner.
- `test_cpu_setup.py`: evaluation environment/resource check.

## Proposed Rebuild Stages

1. **Freeze inputs**
   - Record file paths, row counts, index metadata, and file hashes.
   - Record whether each artifact is current, historical, or generated.

2. **Validate retrieval semantics**
   - Confirm the FAISS metric from the index itself.
   - Treat `IndexFlatL2` outputs as squared L2 distances, where lower is closer.
   - Keep binary acceptance separate from exact retrieved-scheme identity.

3. **Adjudicate labels**
   - Review all unresolved positive mappings in `label_audit_reports/manual_review_worksheet.csv`.
   - Record approved dataset slug, reviewer decision, and source rationale.
   - Do not treat candidate traceability or string name similarity as semantic ground truth.

4. **Run corrected retrieval evaluation**
   - Use a documented validation/test split or prespecified threshold protocol.
   - Recalculate confusion-matrix metrics only after label policy is frozen.
   - Report threshold diagnostics separately from selected operating-point results.

5. **Reconstruct missing feature evaluations**
   - Speech: raw audio/reference transcripts, model/version, predictions, WER/CER/accuracy scripts.
   - Recommendation: profiles, eligibility/relevance labels, rankings, and metric scripts.
   - Conversation: rating records, rubric, evaluator metadata, and aggregation script.
   - Latency: request-level logs, load script, environment, timeout definition, and percentile calculation.

6. **Evaluate a comparable baseline**
   - Use the same dataset, query population, label policy, and metrics.
   - Do not use narrative comparison tables as baseline evidence.

7. **Draft results from an evidence ledger**
   - Every number must link to a file and calculation method.
   - Use `Verified`, `Provisional`, `Contradictory`, `Unsupported`, `Not reproducible`, or `Pending review`.
   - Use `Not verified` where the workspace lacks evidence.

8. **Quality checks**
   - Check all numerical claims against generated tables.
   - Confirm no candidate name-similarity field is called FAISS similarity.
   - Confirm no unverified label is called ground truth.
   - Confirm no threshold is called optimal without validation.
   - Confirm no baseline comparison is claimed without a comparable run.

## Planned New Outputs

This directory is reserved for rebuild artifacts and should not overwrite existing outputs:

- `BASELINE.md`: verified starting-state inventory and claim status.
- `PLAN.md`: this workflow and evidence policy.
- `input_manifest.csv`: planned file/hash/role manifest; Not verified until generated.
- `label_decisions.csv`: human adjudication output; Not verified until completed.
- `retrieval_metrics.csv`: corrected evaluation output; Not verified until rerun after label policy is frozen.
- `threshold_diagnostics.csv`: isolated threshold diagnostics; Not verified until generated in this workspace.
- `evidence_ledger.csv`: claim-to-source ledger for the rebuilt Results section.
- `results_section.md`: rebuilt Results prose; Not verified until the preceding artifacts exist.

## Non-Destructive Rule

Only files inside `backend/evaluation/results_rebuild/` may be created by the rebuild workflow. Existing project files and generated outputs remain read-only inputs unless a separate request explicitly authorizes changes.
