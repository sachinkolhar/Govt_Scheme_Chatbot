"""
Evaluation Configuration File

Customize the evaluation pipeline without modifying the main script.
"""

# ============================================================================
# Thresholds to Test
# ============================================================================

# List of FAISS confidence thresholds to evaluate
# Default: [0.2, 0.3, 0.4, 0.5, 0.6]
# Modify for more granular testing or different ranges
THRESHOLDS_TO_TEST = [0.2, 0.3, 0.4, 0.5, 0.6]

# For more granular testing (finer steps):
# THRESHOLDS_TO_TEST = [0.25, 0.30, 0.35, 0.40, 0.45]

# For broader range testing:
# THRESHOLDS_TO_TEST = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]

# ============================================================================
# Ambiguity Detection
# ============================================================================

# Score gap threshold for marking as ambiguous
# If top_score - second_score < this value, mark as ambiguous
# Ambiguous matches need manual review
AMBIGUITY_THRESHOLD = 0.05

# For stricter ambiguity detection (fewer false ambiguities):
# AMBIGUITY_THRESHOLD = 0.10

# For more lenient detection (catch more edge cases):
# AMBIGUITY_THRESHOLD = 0.03

# ============================================================================
# Search Parameters
# ============================================================================

# Number of top candidates to retrieve from FAISS
# More candidates = slower search but more robust evaluation
TOP_K_RESULTS = 5

# ============================================================================
# Output Configuration
# ============================================================================

# Results directory (relative to evaluation script directory)
RESULTS_DIR = "results"

# CSV filenames
DETAILED_RESULTS_FILE = "evaluation_results_detailed.csv"
SUMMARY_METRICS_FILE = "evaluation_summary.csv"
AMBIGUOUS_MATCHES_FILE = "ambiguous_matches.csv"

# Visualization
VISUALIZATION_FILE = "threshold_comparison.png"
VISUALIZATION_DPI = 300
VISUALIZATION_FIGSIZE = (14, 10)

# ============================================================================
# Visualization Configuration
# ============================================================================

# Color scheme
COLORS = {
    "accuracy": "#1f77b4",
    "precision": "#ff7f0e",
    "recall": "#2ca02c",
    "f1_score": "#d62728",
    "false_positives": "#ff7f0e",
    "false_negatives": "#d62728",
}

# Plot style
PLOT_STYLE = "whitegrid"  # Options: darkgrid, whitegrid, dark, white, ticks
PLOT_MARKER_SIZE = 8
PLOT_LINE_WIDTH = 2

# ============================================================================
# Metrics Configuration
# ============================================================================

# Metric thresholds for warnings/recommendations
# If any metric falls below these, generate warning
MIN_ACCEPTABLE_METRICS = {
    "accuracy": 0.75,
    "precision": 0.80,
    "recall": 0.85,
    "f1_score": 0.80,
}

# Threshold for considering false positives/negatives as "high"
HIGH_ERROR_THRESHOLD = 10  # Warn if more than 10

# ============================================================================
# Logging & Output
# ============================================================================

# Verbosity levels: 0=silent, 1=normal, 2=verbose
VERBOSITY = 1

# Progress update frequency (every N queries)
PROGRESS_INTERVAL = 10

# Print detailed metrics summary
PRINT_SUMMARY = True

# ============================================================================
# Resource Paths (Auto-detected, but can override)
# ============================================================================

# If your resources are in non-standard locations, override here:
# (Leave as None to use auto-detection)

MODEL_DIR = None  # Default: {root}/model
DATA_DIR = None   # Default: {root}/dataset
QUERIES_FILE = None  # Default: {current_dir}/test_queries.json

# Example overrides:
# MODEL_DIR = "/path/to/custom/model"
# DATA_DIR = "/path/to/custom/data"
# QUERIES_FILE = "/path/to/custom/queries.json"

# ============================================================================
# Encoder Configuration
# ============================================================================

# Sentence transformer encoder settings
ENCODER_BATCH_SIZE = 32
ENCODER_CONVERT_TO_NUMPY = True

# ============================================================================
# Advanced: Metric Calculations
# ============================================================================

# Calculate additional metrics beyond standard ones
# Requires more computation but provides more insights
CALCULATE_ADVANCED_METRICS = False

# Advanced metrics include:
# - Specificity (TN / (TN + FP))
# - Sensitivity (TP / (TP + FN))
# - False positive rate
# - False negative rate
# - Matthews correlation coefficient

# ============================================================================
# Export Configuration
# ============================================================================

# CSV export settings
CSV_ENCODING = "utf-8"
CSV_FLOAT_FORMAT = "%.4f"  # Decimal places for float values
CSV_INDEX = False  # Include row indices

# Include timestamp in filenames
TIMESTAMP_OUTPUT = False

# Example: evaluation_results_detailed_2024_05_20_143022.csv
# Instead of: evaluation_results_detailed.csv

# ============================================================================
# Performance Optimization
# ============================================================================

# Parallel processing (if supported in future)
USE_MULTIPROCESSING = False
NUM_WORKERS = 4

# Cache search results (speeds up re-runs)
CACHE_SEARCH_RESULTS = True

# ============================================================================
# Quality Checks
# ============================================================================

# Minimum required test queries for reliable evaluation
MIN_TEST_QUERIES = 30

# Maximum queries to process (for testing)
# Set to None for no limit
MAX_TEST_QUERIES = None

# ============================================================================
# Recommendation Engine
# ============================================================================

# Criteria for recommended threshold
# "f1_score": Use F1 score (recommended)
# "precision": Prioritize precision (fewer false positives)
# "recall": Prioritize recall (fewer false negatives)
RECOMMENDATION_METRIC = "f1_score"

# If tie in metric score, use this as tiebreaker
# Options: "accuracy", "precision", "recall", "f1_score"
RECOMMENDATION_TIEBREAKER = "accuracy"

# ============================================================================
# Notifications & Alerts
# ============================================================================

# Alert thresholds
ALERT_THRESHOLDS = {
    "high_fp": 10,  # Alert if FP > this
    "high_fn": 10,  # Alert if FN > this
    "low_f1": 0.80,  # Alert if F1 < this
    "high_ambiguous": 5,  # Alert if ambiguous > this
}

# ============================================================================
# Custom Hooks (Advanced)
# ============================================================================

# Functions to call at various pipeline stages
# Leave as None to skip

def on_evaluation_start():
    """Called when evaluation starts."""
    pass

def on_threshold_evaluated(threshold, metrics):
    """Called after each threshold evaluation."""
    pass

def on_evaluation_complete(all_metrics):
    """Called when evaluation completes."""
    pass

# ============================================================================
# Documentation
# ============================================================================

"""
Quick Configuration Guide:

1. MOST IMPORTANT: Modify THRESHOLDS_TO_TEST if testing custom range
2. USUALLY: Leave other settings as defaults
3. CUSTOMIZE: Adjust ambiguity, output, visualization if needed
4. ADVANCED: Only modify after understanding implications

Default recommended settings are optimized for:
- Government schemes chatbot use case
- Balanced precision/recall
- Production-grade evaluation

For help, see README.md or INTEGRATION_GUIDE.md
"""

# ============================================================================
# Load Configuration
# ============================================================================

def get_config():
    """Get configuration as dictionary."""
    return {
        "thresholds": THRESHOLDS_TO_TEST,
        "ambiguity_threshold": AMBIGUITY_THRESHOLD,
        "top_k": TOP_K_RESULTS,
        "results_dir": RESULTS_DIR,
        "verbosity": VERBOSITY,
    }

if __name__ == "__main__":
    print("Configuration loaded successfully")
    print(f"Thresholds to test: {THRESHOLDS_TO_TEST}")
    print(f"Ambiguity threshold: {AMBIGUITY_THRESHOLD}")
    print(f"Results directory: {RESULTS_DIR}")
