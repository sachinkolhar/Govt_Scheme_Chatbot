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

| File                              | Purpose                 | How to Use                    |
| --------------------------------- | ----------------------- | ----------------------------- |
| `evaluation_summary.csv`          | Metrics per threshold   | Find **highest F1 score** row |
| `evaluation_results_detailed.csv` | Per-query results       | Debug wrong matches           |
| `ambiguous_matches.csv`           | Close calls (<0.05 gap) | Manual review edge cases      |
| `threshold_comparison.png`        | 4-panel visualization   | See trends visually           |

## 🎯 Quick Steps to Implement

1. **Run evaluation** → `python run_evaluation.py`
2. **Check results** → Open `evaluation_summary.csv`
3. **Find best threshold** → Row with max **F1 Score**
4. **Update chatbot** → Edit `backend/config/settings.py`
5. **Change this line:**
   ```python
   FAISS_MIN_SCORE = float(os.getenv("FAISS_MIN_SCORE", "0.35"))
   ```
6. **Restart backend** → `python backend/main.py`
7. **Test manually** → Use queries from `test_queries.json`

## 📈 Metrics Explained (Short Version)

- **Accuracy** = Overall correctness
- **Precision** = Accuracy of matches suggested (minimize false positives)
- **Recall** = Percentage of actual matches found (minimize false negatives)
- **F1 Score** = Balance between precision & recall ⭐ **USE THIS**

## 🎚️ Threshold Tuning

**Too many wrong suggestions?** → Raise threshold (0.35 → 0.45)

**Too many "not found"?** → Lower threshold (0.35 → 0.25)

**Not sure?** → Use highest F1 score threshold

## 🔧 Integrate into Your Code

```python
from evaluation_pipeline import semantic_search

# Search
results = semantic_search(query, encoder, faiss_index, df)

# Apply threshold
if results[0][1] >= 0.35:  # Your best threshold
    scheme = results[0][0]
else:
    scheme = None
```

## ✅ Verification Checklist

Before deploying new threshold:

- [ ] Evaluation completed without errors
- [ ] F1 score looks good (0.90+)
- [ ] False positives are reasonable (<3)
- [ ] False negatives are reasonable (<3)
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

## 🎓 Key Numbers for Your Chatbot

**Recommended thresholds:**

- Conservative (fewer wrong suggestions): **0.40-0.50**
- Balanced (good precision & recall): **0.30-0.40** ⭐
- Lenient (fewer "not found"): **0.20-0.30**

**Start with 0.35** and adjust based on results.

## 💾 Saving Your Work

```bash
# After evaluation
git add backend/evaluation/results/
git add backend/config/settings.py
git commit -m "Evaluation complete: Best threshold=0.35 (F1=0.92)"
```

---

**First time?** Run: `python backend/evaluation/run_evaluation.py`

**Questions?** See `README.md` or `INTEGRATION_GUIDE.md`

**Last Updated:** May 2026
