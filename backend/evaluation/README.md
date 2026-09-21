# FAISS Threshold Evaluation Pipeline

A comprehensive evaluation framework for tuning the FAISS confidence threshold in the Government Schemes Chatbot.

## Overview

This pipeline helps you find the optimal confidence threshold for your semantic search-based chatbot by:

- Testing multiple thresholds (0.2 to 0.6)
- Calculating precision, recall, accuracy, and F1 scores
- Identifying ambiguous matches (close top-2 scores)
- Generating visualizations
- Recommending the best threshold

## Files

- **`evaluation_pipeline.py`** - Main evaluation script
- **`test_queries.json`** - 65 labeled test queries (government schemes dataset)
- **`results/`** - Output directory for CSV files and visualizations

## Quick Start

### 1. Install Dependencies

```bash
pip install pandas numpy matplotlib seaborn scikit-learn
```

(Optional: If using GPU)

```bash
pip install faiss-gpu
```

### 2. Verify Resources

Make sure your chatbot has these files:

```
project_root/
├── backend/
│   ├── evaluation/
│   │   ├── evaluation_pipeline.py
│   │   └── test_queries.json
│   └── ...
├── model/
│   ├── semantic_encoder.pkl (SentenceTransformer encoder)
│   └── scheme_index.faiss (FAISS index)
├── dataset/
│   └── govt_schemes.csv (Scheme metadata)
└── ...
```

### 3. Run Evaluation

```bash
cd backend/evaluation
python evaluation_pipeline.py
```

This will:

- Load 65 test queries
- Test 5 thresholds: 0.2, 0.3, 0.4, 0.5, 0.6
- Calculate metrics for each threshold
- Generate visualization plots
- Print recommendations

## Output Files

### CSV Files

#### `evaluation_results_detailed.csv`

Per-query results:

| query             | expected_scheme | matched_scheme | top_score | second_score | threshold | accepted | ambiguous | correct |
| ----------------- | --------------- | -------------- | --------- | ------------ | --------- | -------- | --------- | ------- |
| PM Kisan benefits | PM-KISAN        | PM-KISAN       | 0.8234    | 0.6123       | 0.2       | Yes      | No        | Yes     |
| driving license   | null            | PM-KISAN       | 0.3145    | 0.2987       | 0.2       | Yes      | No        | No      |

**Use this to:**

- Understand which queries fail
- Review false positives
- Analyze edge cases

#### `evaluation_summary.csv`

Per-threshold metrics:

| threshold | accuracy | precision | recall | f1_score | true_positives | false_positives | true_negatives | false_negatives | ambiguous_matches |
| --------- | -------- | --------- | ------ | -------- | -------------- | --------------- | -------------- | --------------- | ----------------- |
| 0.2       | 0.8231   | 0.8571    | 0.9286 | 0.8913   | 13             | 2               | 48             | 1               | 3                 |
| 0.3       | 0.8462   | 0.9091    | 0.9286 | 0.9189   | 13             | 1               | 49             | 1               | 2                 |

**Use this to:**

- Compare threshold performance
- Select best F1 score
- Balance precision vs recall

#### `ambiguous_matches.csv`

Queries where top-2 scores are within 0.05:

| query           | expected_scheme | matched_scheme | top_score | second_score | gap    | threshold |
| --------------- | --------------- | -------------- | --------- | ------------ | ------ | --------- |
| elderly pension | IGN Old Age     | IGN Widow      | 0.7234    | 0.6823       | 0.0411 | 0.3       |

**Use this to:**

- Identify edge cases
- Review for manual correction
- Consider secondary disambiguation

### Visualization

#### `threshold_comparison.png`

4-panel plot showing:

1. **Accuracy & F1 Score vs Threshold** - Overall performance
2. **Precision & Recall vs Threshold** - Tradeoff analysis
3. **False Positives vs Threshold** - Type I errors
4. **False Negatives vs Threshold** - Type II errors

## Metrics Explained

### Classification Metrics

- **True Positive (TP)**: Expected match found correctly
- **False Positive (FP)**: No match expected, but match found (Type I error)
- **True Negative (TN)**: No match expected, correctly not found
- **False Negative (FN)**: Expected match not found (Type II error)

### Performance Metrics

- **Accuracy** = (TP + TN) / Total
  - Overall correctness
  - Balanced for this use case

- **Precision** = TP / (TP + FP)
  - When we say match found, how often correct?
  - Lower FP = higher precision
  - Goal: ~0.90+

- **Recall** = TP / (TP + FN)
  - How many actual matches did we find?
  - Higher recall = fewer missed matches
  - Goal: ~0.95+

- **F1 Score** = 2 _ (Precision _ Recall) / (Precision + Recall)
  - Harmonic mean of precision & recall
  - Best overall metric for this task
  - Higher is better

## Interpreting Results

### Example Output

```
📊 BEST THRESHOLD: 0.35
   F1 Score:        0.9128
   Accuracy:        0.8462
   Precision:       0.9286
   Recall:          0.9000
   False Positives: 1
   False Negatives: 1
   Ambiguous:       2
```

### What This Means

- **Threshold 0.35** balances precision and recall best
- **F1 of 0.91** indicates excellent performance
- **1 false positive** = 1 wrong scheme suggested when it shouldn't
- **1 false negative** = 1 missed scheme that should have matched
- **2 ambiguous** = 2 queries with close-call scores (manual review needed)

## Adding More Test Queries

Edit `test_queries.json` to add queries:

```json
[
  {
    "query": "your query here",
    "expected_scheme": "Exact Scheme Name or null",
    "expected_match": true or false
  }
]
```

**Rules:**

- `expected_scheme` must match exactly as in CSV (case-sensitive)
- Set to `null` if expecting no match
- `expected_match` should be `true` only if scheme exists in dataset

## Tuning Strategy

### Scenario 1: Too Many False Positives (wrong schemes suggested)

- **Problem**: User gets incorrect suggestions
- **Solution**: Raise threshold (0.5 → 0.6)
- **Tradeoff**: May miss some valid schemes (higher false negatives)

### Scenario 2: Too Many False Negatives (missing schemes)

- **Problem**: "Sorry, I don't have that scheme" even when it exists
- **Solution**: Lower threshold (0.3 → 0.2)
- **Tradeoff**: May suggest irrelevant schemes (higher false positives)

### Scenario 3: Balanced Approach

- Use the threshold with highest F1 score
- Typically 0.3-0.4 for good precision (90%+) and recall (90%+)
- Monitor in production for user feedback

## Integration

### Update Settings

Once you've identified the best threshold:

1. Update `backend/config/settings.py`:

```python
# Before
FAISS_MIN_SCORE = float(os.getenv("FAISS_MIN_SCORE", "0.2"))

# After
FAISS_MIN_SCORE = float(os.getenv("FAISS_MIN_SCORE", "0.35"))  # Your best threshold
```

2. Or set environment variable:

```bash
export FAISS_MIN_SCORE=0.35
python backend/main.py
```

## Troubleshooting

### "encoder is None"

- Verify `model/semantic_encoder.pkl` exists
- Check file is valid and readable
- Ensure CUDA/torch is properly installed if expected

### "FAISS index unavailable"

- Verify `model/scheme_index.faiss` exists
- Ensure faiss is installed: `pip install faiss-cpu`
- Check FAISS library build is compatible with CPU/GPU

### "No results plotted"

- Verify matplotlib is installed: `pip install matplotlib seaborn`
- Check output directory has write permissions

### Test queries load error

- Verify `test_queries.json` is valid JSON
- Check no trailing commas
- Ensure all required fields present

## Performance Considerations

- **Speed**: Full evaluation (65 queries × 5 thresholds) ~5-30 seconds
- **Memory**: Encoder + FAISS index typically 500MB-2GB
- **CPU Usage**: Semantic encoding can be slow on CPU-only systems

### Speed Optimization

For faster evaluation on CPU:

```bash
# Use smaller batch size
python evaluation_pipeline.py --batch_size 1
```

## Advanced Usage

### Custom Threshold Range

Edit `main()` function:

```python
thresholds_to_test = [0.15, 0.25, 0.35, 0.45, 0.55]  # Custom range
```

### Add More Metrics

Extend `ThresholdMetrics` dataclass:

```python
@dataclass
class ThresholdMetrics:
    # ... existing fields ...
    specificity: float  # TN / (TN + FP)
    sensitivity: float  # TP / (TP + FN)
```

### Custom Scoring Logic

Modify `evaluate_query()` for domain-specific logic:

```python
# Example: Partial matches count as correct
if expected_scheme.lower() in matched_scheme.lower():
    is_correct = True
```

## Contact & Support

For issues or questions:

1. Check Troubleshooting section
2. Review generated CSV files for details
3. Check console output for error messages
4. Verify all resource files exist and are readable

## License

Part of Government Schemes Chatbot project.

---

**Last Updated**: May 2026
