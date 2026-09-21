"""
FAISS Confidence Threshold Evaluation Pipeline
===============================================

This script evaluates and tunes the FAISS confidence threshold for optimal
chatbot performance by testing multiple thresholds against a labeled dataset.

Usage:
    python evaluation_pipeline.py

Output:
    - evaluation_results_detailed.csv (per-query results)
    - evaluation_summary.csv (per-threshold metrics)
    - ambiguous_matches.csv (queries with close top-2 scores)
    - threshold_comparison.png (visualization)
"""

import json
import os
import sys
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import joblib
import numpy as np
import pandas as pd

try:
    import torch
except ImportError:
    torch = None

try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    warnings.warn("matplotlib/seaborn not installed. Skipping visualizations.")

try:
    import faiss
except ImportError:
    faiss = None


# ============================================================================
# CPU Forcing (for CPU-only machines)
# ============================================================================

def _setup_cpu_mode() -> None:
    """
    Force PyTorch to use CPU mode, preventing CUDA deserialization errors.
    
    This is essential for CPU-only machines where torch models are saved with
    CUDA metadata but no CUDA hardware is available.
    
    This function:
    - Disables CUDA visibility
    - Overrides torch.cuda.is_available() to return False
    - Patches torch.load to use map_location='cpu'
    """
    if torch is None:
        return
    
    # Disable CUDA
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    
    # Override is_available check
    torch.cuda.is_available = lambda: False  # type: ignore
    
    # Patch torch.load to use CPU
    _original_torch_load = torch.load  # type: ignore
    
    def _cpu_torch_load(*args: Any, **kwargs: Any) -> Any:
        """Wrapper that forces CPU loading."""
        kwargs.setdefault("map_location", torch.device("cpu"))  # type: ignore
        kwargs.setdefault("weights_only", False)
        return _original_torch_load(*args, **kwargs)
    
    torch.load = _cpu_torch_load  # type: ignore


# Setup CPU mode before loading any models
_setup_cpu_mode()

# ============================================================================
# Data Classes & Configuration
# ============================================================================


@dataclass
class QueryResult:
    """Results for a single test query."""
    query: str
    expected_scheme: Optional[str]
    expected_match: bool
    matched_scheme: Optional[str]
    top_score: float
    second_score: float
    is_ambiguous: bool
    threshold: float
    is_accepted: bool
    is_correct: bool


@dataclass
class ThresholdMetrics:
    """Evaluation metrics for a single threshold."""
    threshold: float
    true_positives: int
    false_positives: int
    true_negatives: int
    false_negatives: int
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    total_ambiguous: int


# ============================================================================
# Core Functions
# ============================================================================


def load_queries(json_path: str) -> List[Dict[str, Any]]:
    """
    Load test queries from JSON file.
    
    Args:
        json_path: Path to test_queries.json
        
    Returns:
        List of query dictionaries with keys:
        - query (str): The test query
        - expected_scheme (str|null): Expected matched scheme name
        - expected_match (bool): Whether match is expected
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            queries = json.load(f)
        print(f"✓ Loaded {len(queries)} test queries from {json_path}")
        return queries
    except FileNotFoundError:
        print(f"✗ Error: Query file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"✗ Error: Invalid JSON in {json_path}")
        sys.exit(1)


def load_search_resources(
    model_dir: str,
    data_dir: str
) -> Tuple[Any, Any, pd.DataFrame]:
    """
    Load FAISS index, semantic encoder, and dataset.
    
    Encoder loading is automatically configured for CPU-only machines:
    - Disables CUDA
    - Forces map_location='cpu' in torch.load
    - Sets device='cpu' for SentenceTransformer
    
    Args:
        model_dir: Path to model directory (contains .pkl and .faiss files)
        data_dir: Path to data directory (contains CSV)
        
    Returns:
        Tuple of (encoder, faiss_index, dataframe)
    """
    print("\nLoading search resources...")
    
    # Load encoder with CPU mode
    encoder_path = os.path.join(model_dir, "semantic_encoder.pkl")
    try:
        encoder = joblib.load(encoder_path)
        
        # Ensure encoder is on CPU (for SentenceTransformer models)
        if encoder is not None and hasattr(encoder, 'to'):
            encoder.to('cpu')
        
        print(f"✓ Loaded semantic encoder from {encoder_path} (CPU mode)")
    except Exception as e:
        print(f"✗ Error loading encoder: {e}")
        print(f"  Make sure semantic_encoder.pkl exists and is valid")
        encoder = None
    
    # Load FAISS index
    faiss_index = None
    if faiss is not None:
        index_path = os.path.join(model_dir, "scheme_index.faiss")
        try:
            faiss_index = faiss.read_index(index_path)
            print(f"✓ Loaded FAISS index from {index_path}")
        except Exception as e:
            print(f"✗ Error loading FAISS index: {e}")
            print(f"  Make sure scheme_index.faiss exists")
    else:
        print("✗ faiss library not installed")
    
    # Load dataset
    csv_path = os.path.join(data_dir, "govt_schemes.csv")
    try:
        df = pd.read_csv(csv_path).fillna("")
        print(f"✓ Loaded dataset with {len(df)} schemes from {csv_path}")
    except Exception as e:
        print(f"✗ Error loading dataset: {e}")
        sys.exit(1)
    
    return encoder, faiss_index, df


def semantic_search(
    query: str,
    encoder: Any,
    faiss_index: Any,
    df: pd.DataFrame,
    top_k: int = 5
) -> List[Tuple[str, float]]:
    """
    Perform semantic search on query.
    
    Args:
        query: User query text
        encoder: Sentence transformer encoder
        faiss_index: FAISS index
        df: Schemes dataframe
        top_k: Number of top results to return
        
    Returns:
        List of (scheme_name, score) tuples
    """
    if encoder is None or faiss_index is None or df.empty:
        return []
    
    try:
        # Clean and encode query
        query_clean = query.lower().strip()
        embedding = encoder.encode([query_clean], convert_to_numpy=True).astype(np.float32)
        
        # Search FAISS
        distances, indices = faiss_index.search(embedding, min(top_k, 5))
        
        # Build results
        results = []
        for score, idx in zip(distances[0], indices[0]):
            if 0 <= idx < len(df):
                scheme_name = df.iloc[int(idx)].get("scheme_name", "Unknown")
                results.append((scheme_name, float(score)))
        
        return results
    except Exception as e:
        print(f"✗ Search error for query '{query}': {e}")
        return []


def evaluate_query(
    query_data: Dict[str, Any],
    results: List[Tuple[str, float]],
    threshold: float
) -> QueryResult:
    """
    Evaluate a single query against results and threshold.
    
    Args:
        query_data: Query record with expected_scheme and expected_match
        results: Top search results with scores
        threshold: Confidence threshold to test
        
    Returns:
        QueryResult with evaluation details
    """
    query = query_data["query"]
    expected_scheme = query_data.get("expected_scheme")
    expected_match = query_data.get("expected_match", False)
    
    # Extract top and second scores
    top_score = results[0][1] if results else 0.0
    second_score = results[1][1] if len(results) > 1 else 0.0
    matched_scheme = results[0][0] if results else None
    
    # Check if ambiguous (top two scores within 0.05)
    is_ambiguous = top_score - second_score < 0.05
    
    # Check if accepted by threshold
    is_accepted = top_score >= threshold if results else False
    
    # Determine if correct
    if expected_match:
        # Should match
        is_correct = is_accepted and (matched_scheme == expected_scheme)
    else:
        # Should not match
        is_correct = not is_accepted or (matched_scheme != expected_scheme)
    
    return QueryResult(
        query=query,
        expected_scheme=expected_scheme,
        expected_match=expected_match,
        matched_scheme=matched_scheme,
        top_score=top_score,
        second_score=second_score,
        is_ambiguous=is_ambiguous,
        threshold=threshold,
        is_accepted=is_accepted,
        is_correct=is_correct,
    )


def evaluate_threshold(
    queries: List[Dict[str, Any]],
    encoder: Any,
    faiss_index: Any,
    df: pd.DataFrame,
    threshold: float
) -> Tuple[List[QueryResult], List[Dict[str, Any]]]:
    """
    Evaluate all queries at a specific threshold.
    
    Args:
        queries: List of test queries
        encoder: Semantic encoder
        faiss_index: FAISS index
        df: Schemes dataframe
        threshold: Confidence threshold to test
        
    Returns:
        Tuple of (query_results, ambiguous_queries)
    """
    query_results = []
    ambiguous_queries = []
    
    print(f"\n  Evaluating {len(queries)} queries at threshold {threshold:.2f}...")
    
    for i, query_data in enumerate(queries):
        # Perform semantic search
        results = semantic_search(query_data["query"], encoder, faiss_index, df, top_k=5)
        
        # Evaluate against threshold
        result = evaluate_query(query_data, results, threshold)
        query_results.append(result)
        
        # Track ambiguous matches
        if result.is_ambiguous:
            ambiguous_queries.append({
                "query": query_data["query"],
                "expected_scheme": query_data.get("expected_scheme"),
                "matched_scheme": result.matched_scheme,
                "top_score": result.top_score,
                "second_score": result.second_score,
                "gap": result.top_score - result.second_score,
                "threshold": threshold,
            })
        
        # Progress indicator
        if (i + 1) % 10 == 0:
            print(f"    Processed {i + 1}/{len(queries)} queries")
    
    return query_results, ambiguous_queries


def calculate_metrics(
    query_results: List[QueryResult],
    threshold: float
) -> ThresholdMetrics:
    """
    Calculate evaluation metrics for a threshold.
    
    Metrics:
        - True Positive: Correct match expected, correctly found
        - False Positive: No match expected, but match found
        - True Negative: No match expected, correctly not found
        - False Negative: Match expected, but not found
    
    Args:
        query_results: List of evaluated query results
        threshold: The threshold being evaluated
        
    Returns:
        ThresholdMetrics with calculated metrics
    """
    tp = fp = tn = fn = 0
    
    for result in query_results:
        if result.expected_match:
            # Should have match
            if result.is_correct:
                tp += 1
            else:
                fn += 1
        else:
            # Should not have match
            if result.is_correct:
                tn += 1
            else:
                fp += 1
    
    # Calculate ratios
    total = len(query_results)
    accuracy = (tp + tn) / total if total > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    # Count ambiguous
    total_ambiguous = sum(1 for r in query_results if r.is_ambiguous)
    
    return ThresholdMetrics(
        threshold=threshold,
        true_positives=tp,
        false_positives=fp,
        true_negatives=tn,
        false_negatives=fn,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1_score=f1,
        total_ambiguous=total_ambiguous,
    )


def export_csv(
    all_results: List[QueryResult],
    metrics_list: List[ThresholdMetrics],
    ambiguous_list: List[Dict[str, Any]],
    output_dir: str
) -> None:
    """
    Export evaluation results to CSV files.
    
    Args:
        all_results: All query results across all thresholds
        metrics_list: Metrics for each threshold
        ambiguous_list: Ambiguous matches
        output_dir: Output directory for CSV files
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Detailed results per query
    detailed_df = pd.DataFrame([
        {
            "query": r.query,
            "expected_scheme": r.expected_scheme,
            "matched_scheme": r.matched_scheme,
            "top_score": f"{r.top_score:.4f}",
            "second_score": f"{r.second_score:.4f}",
            "threshold": r.threshold,
            "accepted": "Yes" if r.is_accepted else "No",
            "ambiguous": "Yes" if r.is_ambiguous else "No",
            "correct": "Yes" if r.is_correct else "No",
        }
        for r in all_results
    ])
    
    detailed_path = os.path.join(output_dir, "evaluation_results_detailed.csv")
    detailed_df.to_csv(detailed_path, index=False)
    print(f"✓ Exported detailed results to {detailed_path}")
    
    # Summary metrics per threshold
    summary_df = pd.DataFrame([
        {
            "threshold": f"{m.threshold:.2f}",
            "accuracy": f"{m.accuracy:.4f}",
            "precision": f"{m.precision:.4f}",
            "recall": f"{m.recall:.4f}",
            "f1_score": f"{m.f1_score:.4f}",
            "true_positives": m.true_positives,
            "false_positives": m.false_positives,
            "true_negatives": m.true_negatives,
            "false_negatives": m.false_negatives,
            "ambiguous_matches": m.total_ambiguous,
        }
        for m in metrics_list
    ])
    
    summary_path = os.path.join(output_dir, "evaluation_summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"✓ Exported summary metrics to {summary_path}")
    
    # Ambiguous matches
    if ambiguous_list:
        ambiguous_df = pd.DataFrame(ambiguous_list)
        ambiguous_path = os.path.join(output_dir, "ambiguous_matches.csv")
        ambiguous_df.to_csv(ambiguous_path, index=False)
        print(f"✓ Exported {len(ambiguous_list)} ambiguous matches to {ambiguous_path}")


def plot_results(
    metrics_list: List[ThresholdMetrics],
    output_dir: str
) -> None:
    """
    Generate visualization plots.
    
    Args:
        metrics_list: Metrics for each threshold
        output_dir: Output directory for plots
    """
    if not HAS_MATPLOTLIB:
        print("✗ matplotlib not installed; skipping visualizations")
        return
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Prepare data
    thresholds = [m.threshold for m in metrics_list]
    accuracies = [m.accuracy for m in metrics_list]
    precisions = [m.precision for m in metrics_list]
    recalls = [m.recall for m in metrics_list]
    f1_scores = [m.f1_score for m in metrics_list]
    false_positives = [m.false_positives for m in metrics_list]
    false_negatives = [m.false_negatives for m in metrics_list]
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (14, 10)
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('FAISS Threshold Evaluation Results', fontsize=16, fontweight='bold')
    
    # Plot 1: Accuracy vs Threshold
    axes[0, 0].plot(thresholds, accuracies, marker='o', linewidth=2, markersize=8, label='Accuracy')
    axes[0, 0].plot(thresholds, f1_scores, marker='s', linewidth=2, markersize=8, label='F1 Score')
    axes[0, 0].set_xlabel('Confidence Threshold', fontsize=11)
    axes[0, 0].set_ylabel('Score', fontsize=11)
    axes[0, 0].set_title('Accuracy & F1 Score vs Threshold', fontsize=12, fontweight='bold')
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)
    
    # Plot 2: Precision & Recall vs Threshold
    axes[0, 1].plot(thresholds, precisions, marker='o', linewidth=2, markersize=8, label='Precision')
    axes[0, 1].plot(thresholds, recalls, marker='s', linewidth=2, markersize=8, label='Recall')
    axes[0, 1].set_xlabel('Confidence Threshold', fontsize=11)
    axes[0, 1].set_ylabel('Score', fontsize=11)
    axes[0, 1].set_title('Precision & Recall vs Threshold', fontsize=12, fontweight='bold')
    axes[0, 1].legend()
    axes[0, 1].grid(True, alpha=0.3)
    
    # Plot 3: False Positives vs Threshold
    axes[1, 0].bar(thresholds, false_positives, color='#ff7f0e', alpha=0.7)
    axes[1, 0].set_xlabel('Confidence Threshold', fontsize=11)
    axes[1, 0].set_ylabel('Count', fontsize=11)
    axes[1, 0].set_title('False Positives vs Threshold', fontsize=12, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3, axis='y')
    
    # Plot 4: False Negatives vs Threshold
    axes[1, 1].bar(thresholds, false_negatives, color='#d62728', alpha=0.7)
    axes[1, 1].set_xlabel('Confidence Threshold', fontsize=11)
    axes[1, 1].set_ylabel('Count', fontsize=11)
    axes[1, 1].set_title('False Negatives vs Threshold', fontsize=12, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    output_path = os.path.join(output_dir, "threshold_comparison.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved visualization to {output_path}")
    plt.close()


def print_recommendations(metrics_list: List[ThresholdMetrics]) -> None:
    """
    Print evaluation summary and recommendations.
    
    Args:
        metrics_list: Metrics for each threshold
    """
    print("\n" + "=" * 80)
    print("EVALUATION SUMMARY & RECOMMENDATIONS")
    print("=" * 80)
    
    # Find best threshold by F1 score
    best_metrics = max(metrics_list, key=lambda m: m.f1_score)
    
    print(f"\n📊 BEST THRESHOLD: {best_metrics.threshold:.2f}")
    print(f"   F1 Score:        {best_metrics.f1_score:.4f}")
    print(f"   Accuracy:        {best_metrics.accuracy:.4f}")
    print(f"   Precision:       {best_metrics.precision:.4f}")
    print(f"   Recall:          {best_metrics.recall:.4f}")
    print(f"   False Positives: {best_metrics.false_positives}")
    print(f"   False Negatives: {best_metrics.false_negatives}")
    print(f"   Ambiguous:       {best_metrics.total_ambiguous}")
    
    # Show all thresholds comparison
    print(f"\n📈 THRESHOLD COMPARISON:")
    print(f"{'Threshold':<12} {'Accuracy':<12} {'Precision':<12} {'Recall':<12} {'F1':<12} {'FP':<6} {'FN':<6}")
    print("-" * 80)
    for m in sorted(metrics_list, key=lambda x: x.threshold):
        print(f"{m.threshold:<12.2f} {m.accuracy:<12.4f} {m.precision:<12.4f} {m.recall:<12.4f} {m.f1_score:<12.4f} {m.false_positives:<6} {m.false_negatives:<6}")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    print(f"   • Use threshold {best_metrics.threshold:.2f} for best overall performance")
    print(f"   • This threshold has {best_metrics.false_positives} false positives (type I error)")
    print(f"   • This threshold has {best_metrics.false_negatives} false negatives (type II error)")
    
    if best_metrics.false_positives > 10:
        print(f"   ⚠️  Consider raising threshold to reduce false positives")
    elif best_metrics.false_negatives > 10:
        print(f"   ⚠️  Consider lowering threshold to reduce false negatives")
    else:
        print(f"   ✓ Balanced false positive/negative ratio")
    
    # Ambiguous query warning
    total_ambiguous = sum(m.total_ambiguous for m in metrics_list)
    if total_ambiguous > 0:
        print(f"\n   📌 {total_ambiguous} ambiguous matches detected (gap < 0.05 between top 2 scores)")
        print(f"      Consider manual review for edge cases")
    
    print("\n" + "=" * 80)


# ============================================================================
# Main Execution
# ============================================================================


def main():
    """Main evaluation pipeline."""
    
    # Get base directories
    script_dir = Path(__file__).parent.absolute()
    backend_dir = script_dir.parent
    root_dir = backend_dir.parent
    
    model_dir = root_dir / "model"
    data_dir = root_dir / "dataset"
    output_dir = script_dir / "results"
    
    # Paths
    queries_path = str(script_dir / "test_queries.json")
    model_path = str(model_dir)
    data_path = str(data_dir)
    
    print("=" * 80)
    print("FAISS CONFIDENCE THRESHOLD EVALUATION PIPELINE")
    print("=" * 80)
    print(f"\n📁 Configuration:")
    print(f"   Test Queries: {queries_path}")
    print(f"   Model Dir:    {model_path}")
    print(f"   Data Dir:     {data_path}")
    print(f"   Output Dir:   {output_dir}")
    
    # Load data
    queries = load_queries(queries_path)
    encoder, faiss_index, df = load_search_resources(model_path, data_path)
    
    if encoder is None or faiss_index is None:
        print("\n✗ Error: Required resources not loaded")
        sys.exit(1)
    
    # Test thresholds
    thresholds_to_test = [0.2, 0.3, 0.4, 0.5, 0.6]
    all_results = []
    metrics_list = []
    all_ambiguous = []
    
    print(f"\n🔍 Testing {len(thresholds_to_test)} threshold values...")
    
    for threshold in thresholds_to_test:
        query_results, ambiguous_queries = evaluate_threshold(
            queries, encoder, faiss_index, df, threshold
        )
        metrics = calculate_metrics(query_results, threshold)
        
        all_results.extend(query_results)
        metrics_list.append(metrics)
        all_ambiguous.extend(ambiguous_queries)
        
        print(f"  ✓ Threshold {threshold:.2f}: F1={metrics.f1_score:.4f}, Acc={metrics.accuracy:.4f}")
    
    # Export results
    print(f"\n💾 Exporting results...")
    export_csv(all_results, metrics_list, all_ambiguous, str(output_dir))
    
    # Plot results
    plot_results(metrics_list, str(output_dir))
    
    # Print recommendations
    print_recommendations(metrics_list)


if __name__ == "__main__":
    main()
