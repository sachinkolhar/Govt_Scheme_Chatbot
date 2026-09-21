#!/usr/bin/env python
"""
Quick runner for FAISS evaluation pipeline with environment setup.
Usage: python run_evaluation.py
"""

import os
import subprocess
import sys
from pathlib import Path


# ============================================================================
# CPU Forcing (for CPU-only machines)
# ============================================================================

def _setup_cpu_mode() -> None:
    """Force PyTorch to use CPU mode before importing evaluation pipeline."""
    try:
        import torch
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        torch.cuda.is_available = lambda: False  # type: ignore
    except ImportError:
        pass  # torch not installed, skip


# Setup CPU mode early
_setup_cpu_mode()


def main():
    """Run evaluation pipeline with proper setup."""
    
    # Get paths
    current_dir = Path(__file__).parent.absolute()
    evaluation_script = current_dir / "evaluation_pipeline.py"
    
    print("=" * 80)
    print("FAISS THRESHOLD EVALUATION - SETUP & RUN")
    print("=" * 80)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print(f"✗ Python 3.8+ required (you have {sys.version})")
        sys.exit(1)
    
    print(f"\n✓ Python version: {sys.version}")
    
    # Check required modules
    print("\n📦 Checking dependencies...")
    required_packages = {
        'pandas': 'Data processing',
        'numpy': 'Numerical computing',
        'matplotlib': 'Visualization',
        'seaborn': 'Statistical visualization',
    }
    
    optional_packages = {
        'faiss': 'Vector search (usually loaded via backend)',
        'joblib': 'Model serialization (usually loaded via backend)',
    }
    
    missing_packages = []
    
    for package, desc in required_packages.items():
        try:
            __import__(package)
            print(f"  ✓ {package:<15} - {desc}")
        except ImportError:
            print(f"  ✗ {package:<15} - {desc} (MISSING)")
            missing_packages.append(package)
    
    for package, desc in optional_packages.items():
        try:
            __import__(package)
            print(f"  ✓ {package:<15} - {desc}")
        except ImportError:
            print(f"  ⚠ {package:<15} - {desc} (optional, may fail if not in backend)")
    
    if missing_packages:
        print(f"\n⚠️  Missing required packages: {', '.join(missing_packages)}")
        print("\nTo install, run:")
        print(f"  pip install {' '.join(missing_packages)}")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Check required files
    print("\n📁 Checking resources...")
    resources = {
        current_dir / "test_queries.json": "Test queries dataset",
        current_dir.parent.parent / "model" / "semantic_encoder.pkl": "Semantic encoder",
        current_dir.parent.parent / "model" / "scheme_index.faiss": "FAISS index",
        current_dir.parent.parent / "dataset" / "govt_schemes.csv": "Scheme dataset",
    }
    
    missing_resources = []
    for resource_path, desc in resources.items():
        if resource_path.exists():
            size_mb = resource_path.stat().st_size / (1024 * 1024)
            print(f"  ✓ {desc:<30} ({size_mb:.1f} MB)")
        else:
            print(f"  ✗ {desc:<30} (NOT FOUND at {resource_path})")
            missing_resources.append(str(resource_path))
    
    if missing_resources:
        print(f"\n✗ Missing required resources:")
        for resource in missing_resources:
            print(f"  - {resource}")
        print("\nPlease ensure your chatbot is set up correctly.")
        sys.exit(1)
    
    # Create output directory
    output_dir = current_dir / "results"
    output_dir.mkdir(exist_ok=True)
    print(f"\n✓ Output directory: {output_dir}")
    
    # Run evaluation
    print("\n" + "=" * 80)
    print("STARTING EVALUATION PIPELINE...")
    print("=" * 80 + "\n")
    
    try:
        result = subprocess.run(
            [sys.executable, str(evaluation_script)],
            cwd=str(current_dir),
            check=False
        )
        
        if result.returncode == 0:
            print("\n" + "=" * 80)
            print("✅ EVALUATION COMPLETED SUCCESSFULLY")
            print("=" * 80)
            print(f"\n📊 Results saved to: {output_dir}")
            print("\nGenerated files:")
            for csv_file in sorted(output_dir.glob("*.csv")):
                print(f"  - {csv_file.name}")
            for png_file in sorted(output_dir.glob("*.png")):
                print(f"  - {png_file.name}")
            print("\nNext steps:")
            print("  1. Review evaluation_summary.csv for best threshold")
            print("  2. Check evaluation_results_detailed.csv for failures")
            print("  3. View threshold_comparison.png for visualization")
            print("  4. Update FAISS_MIN_SCORE in backend/config/settings.py")
        else:
            print("\n" + "=" * 80)
            print("❌ EVALUATION FAILED")
            print("=" * 80)
            sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Evaluation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
