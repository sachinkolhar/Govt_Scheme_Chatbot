# FAISS Evaluation Pipeline - Quick Reference

## 📂 File Structure

```
backend/evaluation/
├── evaluation_pipeline.py       Main script (production-quality)
├── run_evaluation.py            Convenient runner with checks
├── usage_examples.py            6 practical examples
├── test_queries.json            65 test queries
├── __init__.py                  Package init
├── README.md                    Full documentation
├── INTEGRATION_GUIDE.md         Integration steps
├── evaluation_requirements.txt  Dependencies
└── QUICK_REFERENCE.md           This file
```

## 🚀 One-Line Commands

```bash
# Install dependencies
pip install -r backend/evaluation/evaluation_requirements.txt

# Run evaluation (recommended)
python backend/evaluation/run_evaluation.py

# Run evaluation directly
python backend/evaluation/evaluation_pipeline.py

# Try examples
python backend/evaluation/usage_examples.py

# View results
cat backend/evaluation/results/evaluation_summary.csv
```

## 📊 Key Outputs

| File                              | Purpose                   | How to Use                           |
| --------------------------------- | ------------------------- | ------------------------------------ |
| `evaluation_summary.csv`          | Legacy diagnostic metrics | Review only; not current calibration |
| `evaluation_results_detailed.csv` | Per-query results         | Debug wrong matches                  |
| `ambiguous_matches.csv`           | Close calls (<0.05 gap)   | Manual review edge cases             |
| `threshold_comparison.png`        | 4-panel visualization     | See trends visually                  |

## 🎯 Quick Steps to Implement

1. **Run evaluation** → `python run_evaluation.py`
2. **Check results** → Open `evaluation_summary.csv`
3. **Review the provisional legacy metrics** → Do not treat them as calibration
4. **Set a validated maximum distance** → Edit `backend/config/settings.py`
5. **Use this optional setting:**
   ```python
    raw_distance = os.getenv("FAISS_MAX_DISTANCE")
    FAISS_MAX_DISTANCE = float(raw_distance) if raw_distance else None
   ```
6. **Restart backend** → `python backend/main.py`
7. **Test manually** → Use queries from `test_queries.json`

## 📈 Metrics Explained (Short Version)

- **Accuracy** = Overall correctness
- **Precision** = Accuracy of matches suggested (minimize false positives)
- **Recall** = Percentage of actual matches found (minimize false negatives)
- **F1 Score** = Balance between precision & recall; legacy output is provisional

## 🎚️ Threshold Tuning

**Too many wrong suggestions?** → Recalibrate the squared-L2 cutoff against reviewed labels

**Too many "not found"?** → Recalibrate the squared-L2 cutoff against reviewed labels

**Not sure?** → Do not choose from historical output. Use reviewed labels and a
documented validation procedure.

## 🔧 Integrate into Your Code

```python
from evaluation_pipeline import semantic_search

# Search
results = semantic_search(query, encoder, faiss_index, df)

# Apply the optional maximum squared-L2 distance cutoff.
# IndexFlatL2 returns raw squared L2 distances; lower is closer.
FAISS_MAX_DISTANCE = None  # Uncalibrated until validated.
if FAISS_MAX_DISTANCE is None or results[0][1] <= FAISS_MAX_DISTANCE:
    scheme = results[0][0]
else:
    scheme = None
```

## ✅ Verification Checklist

Before deploying a new optional maximum-distance cutoff:

- [ ] Evaluation completed without errors
- [ ] Reviewed labels are complete for the intended evaluation population
- [ ] Validation procedure and selection rule are documented
- [ ] Ambiguous matches understood
- [ ] settings.py updated
- [ ] Backend restarted
- [ ] Manual testing passed
- [ ] Threshold documented in commit

## 📞 Quick Troubleshooting

| Problem              | Solution                                  |
| -------------------- | ----------------------------------------- |
| "encoder is None"    | Check `model/semantic_encoder.pkl` exists |
| "FAISS unavailable"  | Install: `pip install faiss-cpu`          |
| "No results plotted" | Install: `pip install matplotlib seaborn` |
| "Invalid JSON"       | Validate `test_queries.json` syntax       |
| Slow evaluation      | Normal - ~5-30 sec for full run           |

## 📚 Documentation

- **Full Details** → `README.md`
- **Integration Steps** → `INTEGRATION_GUIDE.md`
- **Code Examples** → `usage_examples.py`
- **Source Code** → `evaluation_pipeline.py` (well-commented)

## 🎓 Current Runtime Notes

- `FAISS_MAX_DISTANCE` is optional and currently uncalibrated.
- A cutoff must not be selected from historical examples or fixed metric targets.
- Semantic relevance is separate from the numeric distance cutoff.
- FAISS index-to-dataset row alignment remains unverified; equal counts do not
  prove row-order alignment.
- The current query file contains 64 queries.

## 💾 Saving Your Work

```bash
# After evaluation
git add backend/evaluation/results/
git add backend/config/settings.py
git commit -m "Record provisional FAISS L2 evaluation diagnostics"
```

---

**First time?** Run: `python backend/evaluation/run_evaluation.py`

**Questions?** See `README.md` or `INTEGRATION_GUIDE.md`

**Last Updated:** May 2026
