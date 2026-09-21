"""
CPU-Only Machine Setup for FAISS Evaluation Pipeline

This script verifies that CPU mode is properly configured and tests
the setup before running the full evaluation.

Run this first if you experience CUDA-related errors.
"""

import os
import sys


def test_cpu_setup():
    """Test CPU mode configuration."""
    print("=" * 80)
    print("FAISS EVALUATION PIPELINE - CPU MODE TEST")
    print("=" * 80)
    
    # Test 1: Check Python
    print(f"\n✓ Python {sys.version}")
    
    # Test 2: Check torch
    print("\n[1/5] Testing PyTorch setup...")
    try:
        import torch
        print(f"✓ PyTorch version: {torch.__version__}")
        
        # Test CUDA check
        is_cuda = torch.cuda.is_available()
        print(f"✓ torch.cuda.is_available() = {is_cuda}")
        
        if is_cuda:
            print("  ⚠️  Warning: CUDA is available but we'll force CPU")
        
        # Test device
        device = torch.device("cpu")
        print(f"✓ CPU device ready: {device}")
        
    except ImportError:
        print("⚠️  PyTorch not installed (optional)")
    except Exception as e:
        print(f"✗ PyTorch error: {e}")
    
    # Test 3: Check joblib
    print("\n[2/5] Testing joblib setup...")
    try:
        import joblib
        print(f"✓ joblib is available")
    except ImportError:
        print("✗ joblib not installed (required)")
        return False
    
    # Test 4: Check FAISS
    print("\n[3/5] Testing FAISS setup...")
    try:
        import faiss
        print(f"✓ FAISS is available")
    except ImportError:
        print("⚠️  FAISS not installed (required)")
        return False
    
    # Test 5: Check evaluation pipeline imports
    print("\n[4/5] Testing evaluation pipeline imports...")
    try:
        from evaluation_pipeline import (
            load_queries,
            load_search_resources,
            semantic_search,
        )
        print("✓ Evaluation pipeline imports successful")
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    
    # Test 6: Check required files
    print("\n[5/5] Checking required resource files...")
    from pathlib import Path
    
    script_dir = Path(__file__).parent.absolute()
    root_dir = script_dir.parent.parent
    
    required_files = {
        "Queries": script_dir / "test_queries.json",
        "Encoder": root_dir / "model" / "semantic_encoder.pkl",
        "FAISS Index": root_dir / "model" / "scheme_index.faiss",
        "Dataset": root_dir / "dataset" / "govt_schemes.csv",
    }
    
    all_exist = True
    for name, path in required_files.items():
        if path.exists():
            size_mb = path.stat().st_size / (1024 * 1024)
            print(f"✓ {name}: {path.name} ({size_mb:.1f} MB)")
        else:
            print(f"✗ {name}: NOT FOUND at {path}")
            all_exist = False
    
    if not all_exist:
        return False
    
    # Final summary
    print("\n" + "=" * 80)
    print("✅ CPU SETUP VERIFICATION COMPLETE")
    print("=" * 80)
    print("\nYou can now run the evaluation pipeline:")
    print("  python run_evaluation.py")
    print("\nOr the direct script:")
    print("  python evaluation_pipeline.py")
    
    return True


if __name__ == "__main__":
    success = test_cpu_setup()
    sys.exit(0 if success else 1)
