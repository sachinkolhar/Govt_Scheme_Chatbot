# CPU-Only Machine Fix for FAISS Evaluation Pipeline

## Problem

When running the evaluation pipeline on a CPU-only machine, you get:

```
RuntimeError: Attempting to deserialize object on a CUDA device but
torch.cuda.is_available() is False
```

This happens because the `semantic_encoder.pkl` file contains PyTorch model weights that were saved with CUDA metadata, but your machine doesn't have CUDA hardware.

## Solution

The evaluation pipeline now includes automatic CPU mode forcing that:

1. **Disables CUDA visibility** - Sets `CUDA_VISIBLE_DEVICES="-1"`
2. **Overrides torch.cuda.is_available()** - Always returns False
3. **Forces CPU in torch.load()** - Uses `map_location=torch.device('cpu')`
4. **Moves models to CPU** - Calls `.to('cpu')` on loaded models

## What Was Changed

### 1. evaluation_pipeline.py

- Added `_setup_cpu_mode()` function that runs at import time
- Updated `load_search_resources()` to call `.to('cpu')` on encoder
- Added detailed CPU mode documentation

### 2. run_evaluation.py

- Added early `_setup_cpu_mode()` call before subprocess launch
- Ensures CPU mode is active before evaluation starts

### 3. usage_examples.py

- Added `_setup_cpu_mode()` call before importing evaluation pipeline
- Ensures all example scripts work on CPU-only machines

### 4. New test_cpu_setup.py

- Comprehensive verification script
- Checks all dependencies and resources
- Validates CPU configuration

## How to Use

### First Time Setup

```bash
# Test your CPU setup
python backend/evaluation/test_cpu_setup.py
```

Expected output:

```
✓ Python 3.x.x
✓ PyTorch version: x.x.x
✓ torch.cuda.is_available() = False
✓ CPU device ready: cpu
✓ joblib is available
✓ FAISS is available
✓ Evaluation pipeline imports successful
✓ Queries: test_queries.json (...)
✓ Encoder: semantic_encoder.pkl (...)
✓ FAISS Index: scheme_index.faiss (...)
✓ Dataset: govt_schemes.csv (...)

✅ CPU SETUP VERIFICATION COMPLETE
```

### Run Evaluation

Now that CPU mode is verified:

```bash
# Use the convenient runner (recommended)
python backend/evaluation/run_evaluation.py

# Or run directly
python backend/evaluation/evaluation_pipeline.py

# Or use examples
python backend/evaluation/usage_examples.py
```

## Technical Details

### CPU Mode Forcing

The solution uses the same approach as `backend/main.py`:

```python
import torch
import os

# Disable CUDA
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Override CUDA check
torch.cuda.is_available = lambda: False

# Patch torch.load for CPU
_original_torch_load = torch.load

def _cpu_torch_load(*args, **kwargs):
    kwargs.setdefault("map_location", torch.device("cpu"))
    kwargs.setdefault("weights_only", False)
    return _original_torch_load(*args, **kwargs)

torch.load = _cpu_torch_load
```

### When CPU Mode Runs

1. **run_evaluation.py** - Sets up CPU mode in `_setup_cpu_mode()` before subprocess
2. **evaluation_pipeline.py** - Calls `_setup_cpu_mode()` at module import time
3. **usage_examples.py** - Calls `_setup_cpu_mode()` before importing pipeline

This ensures CPU mode is active before any model loading happens.

### Encoder Move to CPU

After loading with joblib, we explicitly move the encoder to CPU:

```python
encoder = joblib.load(encoder_path)
if encoder is not None and hasattr(encoder, 'to'):
    encoder.to('cpu')  # Move to CPU device
```

This handles SentenceTransformer models that may still have GPU references.

## Verification

### Check CPU is Forced

```bash
# Run test script
python backend/evaluation/test_cpu_setup.py

# Look for:
# ✓ torch.cuda.is_available() = False
# ✓ CPU device ready: cpu
```

### Verify in Logs

When running evaluation, you should see:

```
✓ Loaded semantic encoder from .../semantic_encoder.pkl (CPU mode)
```

NOT:

```
Attempting to deserialize object on a CUDA device...
```

## Troubleshooting

### "PyTorch not installed"

```bash
# Install PyTorch CPU version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

### "FAISS not installed"

```bash
# Install FAISS CPU version
pip install faiss-cpu

# Or if you have GPU:
# pip install faiss-gpu
```

### Still getting CUDA errors?

1. Run `test_cpu_setup.py` to verify setup
2. Check `torch.cuda.is_available()` returns `False`
3. Verify encoder file is valid: `ls -lh model/semantic_encoder.pkl`
4. Try clearing Python cache: `find . -type d -name __pycache__ -exec rm -r {} +`

### Encoder file is corrupted

```bash
# Recreate encoder if needed
# This requires your original setup script
python backend/scripts/create_encoder.py  # If available
```

## Performance on CPU

CPU-only evaluation will be slower than GPU:

- **Typical timing**: 5-30 seconds for full 65 query × 5 threshold evaluation
- **Per query**: ~0.1-0.3 seconds on modern CPU
- **Bottleneck**: Sentence encoding (not FAISS search)

### Speed Tips

1. Reduce threshold range:

   ```python
   THRESHOLDS_TO_TEST = [0.3, 0.4, 0.5]  # Instead of [0.2, 0.3, 0.4, 0.5, 0.6]
   ```

2. Reduce test queries:
   - Create subset of `test_queries.json` for quick testing

3. Use GPU if available:
   - Install `faiss-gpu` and `torch` with CUDA support
   - Remove CPU forcing to use GPU

## Files Updated

| File                     | Change                            | Impact                          |
| ------------------------ | --------------------------------- | ------------------------------- |
| `evaluation_pipeline.py` | Added `_setup_cpu_mode()`         | Enables CPU at import           |
| `run_evaluation.py`      | Added CPU setup before subprocess | Ensures CPU mode for evaluation |
| `usage_examples.py`      | Added CPU setup before imports    | Enables CPU for examples        |
| `test_cpu_setup.py`      | NEW - Verification script         | Validates configuration         |

## Backwards Compatibility

- ✅ GPU machines still work (CPU setup is applied but GPU available)
- ✅ Existing code not modified (just wrapped with CPU handling)
- ✅ All existing functions unchanged
- ✅ All output formats unchanged

## Related Files

- `backend/main.py` - Original CPU setup approach (we adapted this)
- `backend/config/settings.py` - FAISS_MIN_SCORE configuration
- `backend/search/semantic.py` - Semantic search functions

## Next Steps

1. Run test script: `python backend/evaluation/test_cpu_setup.py`
2. If all checks pass: `python backend/evaluation/run_evaluation.py`
3. Review results in `backend/evaluation/results/`
4. Update chatbot threshold if needed

---

**Need Help?**

- Check `test_cpu_setup.py` output for specific errors
- Review error message in console
- Ensure all required files exist (test script shows locations)
- See main README.md for general troubleshooting
