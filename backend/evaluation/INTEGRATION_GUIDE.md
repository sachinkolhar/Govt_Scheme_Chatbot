# FAISS Evaluation Pipeline - Integration Guide

## 📋 What's Included

Your evaluation package includes:

```
backend/evaluation/
├── evaluation_pipeline.py          # Main evaluation script
├── run_evaluation.py               # Convenient runner with setup checks
├── usage_examples.py               # 6 practical usage examples
├── test_queries.json               # 64 current source-labeled queries
├── __init__.py                     # Package initialization
├── README.md                       # Detailed documentation
├── evaluation_requirements.txt     # Dependencies
└── results/                        # Output directory (auto-created)
    ├── evaluation_results_detailed.csv
    ├── evaluation_summary.csv
    ├── ambiguous_matches.csv
    └── threshold_comparison.png
```

## 🚀 Quick Start (5 minutes)

### Step 1: Install Dependencies

```bash
cd backend/evaluation
pip install -r evaluation_requirements.txt
```

### Step 2: Run Evaluation

```bash
python run_evaluation.py
```

This will:

- ✓ Check all dependencies
- ✓ Verify required files (encoder, FAISS index, dataset)
- ✓ Run the legacy evaluator across historical diagnostic values
- ✓ Generate CSV results and visualization
- ✓ Print provisional diagnostic summaries

### Step 3: Review Results

```bash
# View summary metrics
cat results/evaluation_summary.csv

# View detailed per-query results
cat results/evaluation_results_detailed.csv

# View problematic queries
cat results/ambiguous_matches.csv

# View visualization
open results/threshold_comparison.png
```

## 📊 Understanding the Output

### evaluation_summary.csv

Shows legacy diagnostic output. These values are not current calibration evidence:

```
threshold,accuracy,precision,recall,f1_score,true_positives,...
0.20,...
0.30,...
0.35,...
```

Do not select a cutoff from this output. The legacy evaluator uses
higher-is-better score logic and is not a current `IndexFlatL2` calibration.

### evaluation_results_detailed.csv

Per-query evaluation results:

```
query,expected_scheme,matched_scheme,top_score,accepted,correct
"PM Kisan benefits","PM-KISAN","PM-KISAN","<raw squared L2 distance>","Yes","Yes"
"driving license","null","PM-KISAN","<raw squared L2 distance>","Yes","No"
```

**Use to:**

- Find false positives (wrong matches)
- Find false negatives (missed matches)
- Improve test coverage

### ambiguous_matches.csv

Queries where top-2 scores are very close (<0.05 gap):

```
query,expected_scheme,matched_scheme,top_score,second_score,gap,threshold
"elderly pension","IGN Old Age","IGN Widow","<distance>","<distance>","<distance gap>",<legacy diagnostic value>
```

**These need manual review** - threshold change might flip their classification

### threshold_comparison.png

4-panel visualization:

1. **Accuracy & F1** - Overall performance trend
2. **Precision & Recall** - Quality vs Coverage tradeoff
3. **False Positives** - Wrong suggestions trend
4. **False Negatives** - Missed opportunities trend

## 🎯 Implementation Steps

### Step 1: Understand the Current Runtime Semantics

`IndexFlatL2` returns raw squared L2 distances. Lower distance means closer;
the value is not confidence or similarity. A maximum-distance cutoff, when
configured, is applied as:

```python
accepted = distance <= FAISS_MAX_DISTANCE
```

`FAISS_MAX_DISTANCE` is optional and currently uncalibrated. A cutoff must not
be selected from historical examples. Calibration requires reviewed labels and
a documented validation procedure. Semantic relevance is separate from the
numeric distance cutoff.

The current query file contains 64 queries. FAISS index-to-dataset row
alignment remains unverified: equal vector and dataset counts do not prove
row-order alignment.

### Step 2: Review Legacy Evaluation Only

The historical evaluation output is provisional. It does not establish a
production cutoff for the current squared-L2 index. Do not copy its numeric
threshold into runtime settings without new calibration and label review.

Historical threshold and metric values may appear in generated legacy output;
they are provisional, not current calibration, and not suitable for production
configuration.

### Step 3: Set Only a Validated Maximum Distance

Edit `backend/config/settings.py`:

```python
# Optional; leave unset until a squared-L2 cutoff is validated.
raw_distance = os.getenv("FAISS_MAX_DISTANCE")
FAISS_MAX_DISTANCE = float(raw_distance) if raw_distance else None
```

### Step 4: Test in Chatbot

Restart the backend:

```bash
cd backend
python main.py
```

Test with queries from `test_queries.json` to verify behavior matches expectations.

### Step 5: Monitor in Production

Track metrics:

- False positives: Users complaining about wrong suggestions
- False negatives: Users saying "scheme not found" for valid schemes
- Ambiguous matches: Borderline cases from evaluation

## 💡 Tuning Guide

### Problem: Too Many False Positives

Users get wrong scheme suggestions

**Solution:** Recalibrate the optional maximum squared-L2 distance using
reviewed labels and the documented validation procedure. Do not infer a cutoff
from historical values.

**Steps:**

1. Re-run evaluation with new threshold
2. Check false positives decrease on validation data
3. Confirm semantic relevance separately from the numeric cutoff
4. Update settings.py only after validation

### Problem: Too Many False Negatives

Users get "scheme not found" for valid schemes

**Solution:** Recalibrate the optional maximum squared-L2 distance using
reviewed labels and the documented validation procedure. Do not infer a cutoff
from historical values.

**Steps:**

1. Re-run evaluation with new threshold
2. Check false negatives decrease on validation data
3. Confirm semantic relevance separately from the numeric cutoff
4. Update settings.py only after validation

### Problem: Can't Decide Between Cutoffs

Do not choose from historical output. Define a reviewed-label validation split,
document the selection rule, and report the held-out result separately.

## 🔍 Advanced: Custom Test Sets

### Adding More Queries

Edit `test_queries.json`:

```json
[
  {
    "query": "your test query",
    "expected_scheme": "Exact Scheme Name from CSV",
    "expected_match": true
  },
  {
    "query": "non-matching query",
    "expected_scheme": null,
    "expected_match": false
  }
]
```

**Important:**

- `expected_scheme` must match **exactly** as in CSV (case-sensitive!)
- Set to `null` if scheme doesn't exist in dataset
- `expected_match` boolean indicates if we expect a match

### Finding Exact Scheme Names

```bash
# From dataset/govt_schemes.csv header
# First column is "scheme_name"

# Search for specific scheme
grep -i "kisan" dataset/govt_schemes.csv | head -1

# Output: "PM-KISAN"
# Use exactly this string as expected_scheme
```

## 📈 Programmatic Usage

### Example 1: Single Query Evaluation

```python
from evaluation_pipeline import semantic_search

results = semantic_search(
    query="PM Kisan benefits",
    encoder=encoder,
    faiss_index=faiss_index,
    df=schemes_df,
    top_k=5
)

# Results: [("PM-KISAN", 0.82), ("Farmer Scheme", 0.65), ...]

threshold = 0.35
if results[0][1] >= threshold:
    selected_scheme = results[0][0]
```

### Example 2: Batch Evaluation

```python
from evaluation_pipeline import evaluate_threshold, calculate_metrics

query_results, ambiguous = evaluate_threshold(
    queries=test_queries,
    encoder=encoder,
    faiss_index=faiss_index,
    df=schemes_df,
    threshold=0.35
)

metrics = calculate_metrics(query_results, 0.35)
print(f"F1 Score: {metrics.f1_score}")
```

### Example 3: Full Pipeline

```python
from evaluation_pipeline import (
    load_queries, load_search_resources,
    evaluate_threshold, calculate_metrics,
    export_csv, plot_results
)

# Load
queries = load_queries("test_queries.json")
encoder, index, df = load_search_resources("model", "dataset")

# Evaluate thresholds
metrics_list = []
for threshold in [0.2, 0.3, 0.4, 0.5, 0.6]:
    results, _ = evaluate_threshold(queries, encoder, index, df, threshold)
    metrics = calculate_metrics(results, threshold)
    metrics_list.append(metrics)

# Export & visualize
export_csv(all_results, metrics_list, ambiguous, "output")
plot_results(metrics_list, "output")
```

See `usage_examples.py` for 6 complete working examples.

## 🧪 Testing Your Updates

After changing a validated `FAISS_MAX_DISTANCE` value:

### Test 1: Manual Testing

```python
# Start backend
python backend/main.py

# Test queries from evaluation
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "PM Kisan benefits", "conversation_id": "test"}'

# Should include PM-KISAN in response
```

### Test 2: Automated Testing

```bash
# Create test script with evaluation queries
python usage_examples.py
# Select "Single Threshold" example

# Verify matches align with expectations
```

### Test 3: Regression Testing

```bash
# Keep evaluation results as baseline
# After any changes, re-run:
python run_evaluation.py

# Compare old vs new results
# F1 score should stay same or improve
```

## 📝 Maintenance

### When to Re-evaluate

1. **After adding new schemes** to dataset
   - New schemes might change search rankings
   - Existing threshold might need adjustment

2. **After updating encoder** model
   - Different encoder = different embeddings
   - Must re-evaluate threshold

3. **If user feedback indicates issues**
   - Add problematic queries to test_queries.json
   - Re-run evaluation
   - Adjust threshold if needed

4. **Quarterly reviews** (recommended)
   - Monitor real-world performance
   - Compare with evaluation metrics
   - Adjust if drift detected

### Version Control

Track your evaluation work:

```bash
# Save evaluation results
git add backend/evaluation/results/
git add backend/evaluation/test_queries.json
git commit -m "Record provisional FAISS L2 evaluation diagnostics"

# Track settings changes
git diff backend/config/settings.py
git add backend/config/settings.py
git commit -m "Update validated FAISS_MAX_DISTANCE"
```

## 🐛 Troubleshooting

### Issue: "encoder is None"

```
Cause: semantic_encoder.pkl not found or corrupted
Fix: Ensure model/semantic_encoder.pkl exists
     Verify it was created correctly during setup
```

### Issue: "FAISS index unavailable"

```
Cause: scheme_index.faiss not found
Fix: Install faiss: pip install faiss-cpu
     Verify model/scheme_index.faiss exists
```

### Issue: "matplotlib not installed"

```
Cause: Optional dependency missing
Fix: pip install matplotlib seaborn
     Or just use CSV results without plots
```

### Issue: Results seem wrong

```
Debug steps:
1. Check test_queries.json has valid JSON syntax
2. Verify expected_scheme matches CSV exactly
3. Check for encoding issues (use UTF-8)
4. Run on small subset first
5. Compare with manual search results
```

## 📚 Further Reading

- `README.md` - Detailed technical documentation
- `usage_examples.py` - 6 practical code examples
- `evaluation_pipeline.py` - Inline code documentation

## ✅ Checklist: Before Going to Production

- [ ] Run `python run_evaluation.py` successfully
- [ ] Review `evaluation_summary.csv` as provisional diagnostics only
- [ ] Check `threshold_comparison.png` - trends look reasonable
- [ ] Review `ambiguous_matches.csv` - understand edge cases
- [ ] Update `backend/config/settings.py` only with a validated `FAISS_MAX_DISTANCE`
- [ ] Restart backend and test manually
- [ ] Add 5-10 real-world test cases to `test_queries.json`
- [ ] Document the reviewed-label validation procedure in the change record
- [ ] Set up monitoring for false positives/negatives
- [ ] Plan quarterly re-evaluation

## 🎓 Key Takeaways

1. **F1 Score** is your best metric (balances precision & recall)
2. **Test threshold 0.35** as starting point (good for many datasets)
3. **Monitor real-world usage** - evaluation is offline baseline
4. **Document your choice** - explain why you picked that threshold
5. **Re-evaluate quarterly** - performance can drift over time

---

**Questions?** Check README.md or review usage_examples.py

**Ready to evaluate?** Run: `python run_evaluation.py`
