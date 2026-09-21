# FAISS Evaluation Pipeline - Integration Guide

## 📋 What's Included

Your evaluation package includes:

```
backend/evaluation/
├── evaluation_pipeline.py          # Main evaluation script
├── run_evaluation.py               # Convenient runner with setup checks
├── usage_examples.py               # 6 practical usage examples
├── test_queries.json               # 65 labeled test queries
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
- ✓ Run full evaluation across 5 thresholds
- ✓ Generate CSV results and visualization
- ✓ Print recommendations

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

Shows performance at each threshold:

```
threshold,accuracy,precision,recall,f1_score,true_positives,...
0.20,0.8231,0.8571,0.9286,0.8913,13,2,48,1,3
0.30,0.8462,0.9091,0.9286,0.9189,13,1,49,1,2
0.35,0.8615,0.9286,0.9286,0.9286,13,1,50,1,1
```

**Select threshold with highest F1 score** (0.35 in this example)

### evaluation_results_detailed.csv

Per-query evaluation results:

```
query,expected_scheme,matched_scheme,top_score,accepted,correct
"PM Kisan benefits","PM-KISAN","PM-KISAN","0.8234","Yes","Yes"
"driving license","null","PM-KISAN","0.3145","Yes","No"
```

**Use to:**

- Find false positives (wrong matches)
- Find false negatives (missed matches)
- Improve test coverage

### ambiguous_matches.csv

Queries where top-2 scores are very close (<0.05 gap):

```
query,expected_scheme,matched_scheme,top_score,second_score,gap,threshold
"elderly pension","IGN Old Age","IGN Widow","0.7234","0.6823","0.0411",0.30
```

**These need manual review** - threshold change might flip their classification

### threshold_comparison.png

4-panel visualization:

1. **Accuracy & F1** - Overall performance trend
2. **Precision & Recall** - Quality vs Coverage tradeoff
3. **False Positives** - Wrong suggestions trend
4. **False Negatives** - Missed opportunities trend

## 🎯 Implementation Steps

### Step 1: Identify Best Threshold

From `evaluation_summary.csv`, find row with highest **F1 Score**:

```
threshold: 0.35
f1_score:  0.9189
```

### Step 2: Update Settings

Edit `backend/config/settings.py`:

```python
# Before
FAISS_MIN_SCORE = float(os.getenv("FAISS_MIN_SCORE", "0.2"))

# After
FAISS_MIN_SCORE = float(os.getenv("FAISS_MIN_SCORE", "0.35"))
```

### Step 3: Test in Chatbot

Restart the backend:

```bash
cd backend
python main.py
```

Test with queries from `test_queries.json` to verify behavior matches expectations.

### Step 4: Monitor in Production

Track metrics:

- False positives: Users complaining about wrong suggestions
- False negatives: Users saying "scheme not found" for valid schemes
- Ambiguous matches: Borderline cases from evaluation

## 💡 Tuning Guide

### Problem: Too Many False Positives

Users get wrong scheme suggestions

**Solution:** Increase threshold

```
Current: 0.35 → Try: 0.40 or 0.45
```

**Steps:**

1. Re-run evaluation with new threshold
2. Check false positives decrease
3. Accept slight increase in false negatives
4. Update settings.py

### Problem: Too Many False Negatives

Users get "scheme not found" for valid schemes

**Solution:** Decrease threshold

```
Current: 0.35 → Try: 0.30 or 0.25
```

**Steps:**

1. Re-run evaluation with new threshold
2. Check false negatives decrease
3. Accept slight increase in false positives
4. Update settings.py

### Problem: Can't Decide Between Thresholds

Use F1 score as tiebreaker

**Why F1 Score?**

- Balances precision and recall
- Single number for easy comparison
- Standard in ML evaluation
- Recommended for this use case

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

After changing `FAISS_MIN_SCORE`:

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
git commit -m "Evaluation: Best threshold=0.35 (F1=0.92)"

# Track settings changes
git diff backend/config/settings.py
git add backend/config/settings.py
git commit -m "Update FAISS_MIN_SCORE to 0.35"
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
- [ ] Review `evaluation_summary.csv` - best threshold identified
- [ ] Check `threshold_comparison.png` - trends look reasonable
- [ ] Review `ambiguous_matches.csv` - understand edge cases
- [ ] Update `backend/config/settings.py` with new threshold
- [ ] Restart backend and test manually
- [ ] Add 5-10 real-world test cases to `test_queries.json`
- [ ] Document threshold choice in commit message
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
