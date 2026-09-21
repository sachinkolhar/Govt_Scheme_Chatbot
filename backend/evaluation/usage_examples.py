"""
Usage Examples for FAISS Evaluation Pipeline

This script demonstrates how to use the evaluation pipeline
in various scenarios.
"""

import os
import sys

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

from evaluation_pipeline import (
    calculate_metrics,
    evaluate_threshold,
    load_queries,
    load_search_resources,
    plot_results,
    print_recommendations,
    export_csv,
)
from pathlib import Path


def example_1_basic_usage():
    """Example 1: Basic single-threshold evaluation."""
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Single Threshold Evaluation")
    print("=" * 80)
    
    # Setup paths
    script_dir = Path(__file__).parent.absolute()
    root_dir = script_dir.parent.parent
    
    # Load resources
    queries = load_queries(str(script_dir / "test_queries.json"))
    encoder, faiss_index, df = load_search_resources(
        str(root_dir / "model"),
        str(root_dir / "dataset")
    )
    
    if encoder is None or faiss_index is None:
        print("✗ Resources not available")
        return
    
    # Evaluate at single threshold
    threshold = 0.35
    query_results, ambiguous = evaluate_threshold(
        queries, encoder, faiss_index, df, threshold
    )
    
    # Calculate metrics
    metrics = calculate_metrics(query_results, threshold)
    
    # Print results
    print(f"\n📊 Results at threshold {threshold}:")
    print(f"   Accuracy:  {metrics.accuracy:.4f}")
    print(f"   Precision: {metrics.precision:.4f}")
    print(f"   Recall:    {metrics.recall:.4f}")
    print(f"   F1 Score:  {metrics.f1_score:.4f}")
    print(f"   False Positives: {metrics.false_positives}")
    print(f"   False Negatives: {metrics.false_negatives}")


def example_2_custom_range():
    """Example 2: Test custom threshold range."""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Custom Threshold Range")
    print("=" * 80)
    
    # Setup paths
    script_dir = Path(__file__).parent.absolute()
    root_dir = script_dir.parent.parent
    
    # Load resources
    queries = load_queries(str(script_dir / "test_queries.json"))
    encoder, faiss_index, df = load_search_resources(
        str(root_dir / "model"),
        str(root_dir / "dataset")
    )
    
    if encoder is None or faiss_index is None:
        print("✗ Resources not available")
        return
    
    # Custom thresholds (more granular)
    thresholds = [0.25, 0.30, 0.35, 0.40, 0.45]
    metrics_list = []
    
    for threshold in thresholds:
        print(f"\nTesting threshold {threshold}...")
        query_results, _ = evaluate_threshold(
            queries, encoder, faiss_index, df, threshold
        )
        metrics = calculate_metrics(query_results, threshold)
        metrics_list.append(metrics)
        print(f"  F1: {metrics.f1_score:.4f}")
    
    # Find best
    best = max(metrics_list, key=lambda m: m.f1_score)
    print(f"\n✓ Best threshold: {best.threshold:.2f} (F1: {best.f1_score:.4f})")


def example_3_programmatic_integration():
    """Example 3: Use evaluation in your own code."""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Programmatic Integration")
    print("=" * 80)
    
    from evaluation_pipeline import semantic_search
    
    # Setup paths
    script_dir = Path(__file__).parent.absolute()
    root_dir = script_dir.parent.parent
    
    # Load resources
    encoder, faiss_index, df = load_search_resources(
        str(root_dir / "model"),
        str(root_dir / "dataset")
    )
    
    if encoder is None or faiss_index is None:
        print("✗ Resources not available")
        return
    
    # Test a single query
    test_query = "PM Kisan farmer support"
    results = semantic_search(test_query, encoder, faiss_index, df, top_k=5)
    
    print(f"\nSearch results for: '{test_query}'")
    print(f"{'Rank':<6} {'Scheme':<50} {'Score':<8}")
    print("-" * 80)
    for rank, (scheme, score) in enumerate(results, 1):
        print(f"{rank:<6} {scheme:<50} {score:<8.4f}")
    
    # Apply threshold logic
    threshold = 0.35
    if results[0][1] >= threshold:
        print(f"\n✓ Match accepted (score {results[0][1]:.4f} >= threshold {threshold})")
    else:
        print(f"\n✗ Match rejected (score {results[0][1]:.4f} < threshold {threshold})")


def example_4_batch_evaluation():
    """Example 4: Batch process multiple queries."""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Batch Evaluation")
    print("=" * 80)
    
    from evaluation_pipeline import semantic_search, evaluate_query
    
    # Setup paths
    script_dir = Path(__file__).parent.absolute()
    root_dir = script_dir.parent.parent
    
    # Load resources
    queries = load_queries(str(script_dir / "test_queries.json"))
    encoder, faiss_index, df = load_search_resources(
        str(root_dir / "model"),
        str(root_dir / "dataset")
    )
    
    if encoder is None or faiss_index is None:
        print("✗ Resources not available")
        return
    
    # Process first 10 queries
    threshold = 0.35
    print(f"\nEvaluating first 10 queries at threshold {threshold}:\n")
    print(f"{'Query':<40} {'Expected':<20} {'Matched':<20} {'✓/✗':<5}")
    print("-" * 85)
    
    correct = 0
    for query_data in queries[:10]:
        results = semantic_search(
            query_data["query"], encoder, faiss_index, df, top_k=5
        )
        result = evaluate_query(query_data, results, threshold)
        status = "✓" if result.is_correct else "✗"
        correct += 1 if result.is_correct else 0
        
        exp = query_data.get("expected_scheme") or "None"
        matched = result.matched_scheme or "None"
        
        print(f"{query_data['query']:<40} {exp:<20} {matched:<20} {status:<5}")
    
    print(f"\n✓ Accuracy on first 10: {correct}/10 ({correct*10}%)")


def example_5_export_and_plot():
    """Example 5: Export results and generate plots."""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Export & Visualization")
    print("=" * 80)
    
    # Setup paths
    script_dir = Path(__file__).parent.absolute()
    root_dir = script_dir.parent.parent
    
    # Load resources
    queries = load_queries(str(script_dir / "test_queries.json"))
    encoder, faiss_index, df = load_search_resources(
        str(root_dir / "model"),
        str(root_dir / "dataset")
    )
    
    if encoder is None or faiss_index is None:
        print("✗ Resources not available")
        return
    
    # Run full evaluation
    print("\nRunning full evaluation...")
    thresholds = [0.2, 0.3, 0.4, 0.5, 0.6]
    all_results = []
    metrics_list = []
    all_ambiguous = []
    
    for threshold in thresholds:
        query_results, ambiguous = evaluate_threshold(
            queries, encoder, faiss_index, df, threshold
        )
        metrics = calculate_metrics(query_results, threshold)
        
        all_results.extend(query_results)
        metrics_list.append(metrics)
        all_ambiguous.extend(ambiguous)
    
    # Export
    output_dir = script_dir / "results"
    print(f"\nExporting results to {output_dir}...")
    export_csv(all_results, metrics_list, all_ambiguous, str(output_dir))
    
    # Plot
    print("Generating visualizations...")
    plot_results(metrics_list, str(output_dir))
    
    # Show summary
    print_recommendations(metrics_list)


def example_6_custom_test_set():
    """Example 6: Create and evaluate custom test set."""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Custom Test Set")
    print("=" * 80)
    
    # Create custom test queries
    custom_queries = [
        {
            "query": "How to apply for PM Kisan scheme",
            "expected_scheme": "PM-KISAN",
            "expected_match": True
        },
        {
            "query": "What are benefits of Ayushman Bharat",
            "expected_scheme": "Pradhan Mantri Jan Arogya Yojana",
            "expected_match": True
        },
        {
            "query": "How to renew passport",
            "expected_scheme": None,
            "expected_match": False
        },
    ]
    
    # Setup paths
    script_dir = Path(__file__).parent.absolute()
    root_dir = script_dir.parent.parent
    
    # Load resources
    encoder, faiss_index, df = load_search_resources(
        str(root_dir / "model"),
        str(root_dir / "dataset")
    )
    
    if encoder is None or faiss_index is None:
        print("✗ Resources not available")
        return
    
    # Evaluate
    print(f"\nEvaluating {len(custom_queries)} custom queries:\n")
    
    threshold = 0.35
    query_results, _ = evaluate_threshold(
        custom_queries, encoder, faiss_index, df, threshold
    )
    metrics = calculate_metrics(query_results, threshold)
    
    print(f"Results at threshold {threshold}:")
    for result in query_results:
        status = "✓ CORRECT" if result.is_correct else "✗ WRONG"
        print(f"  {result.query}")
        print(f"    Expected: {result.expected_scheme}, Got: {result.matched_scheme} - {status}")
    
    print(f"\nMetrics:")
    print(f"  Accuracy:  {metrics.accuracy:.4f}")
    print(f"  F1 Score:  {metrics.f1_score:.4f}")


# ============================================================================
# Main
# ============================================================================


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  FAISS Evaluation Pipeline - Usage Examples".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    
    examples = [
        ("Single Threshold", example_1_basic_usage),
        ("Custom Range", example_2_custom_range),
        ("Programmatic Integration", example_3_programmatic_integration),
        ("Batch Evaluation", example_4_batch_evaluation),
        ("Export & Visualization", example_5_export_and_plot),
        ("Custom Test Set", example_6_custom_test_set),
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    try:
        choice = input("\nSelect example to run (1-6) or 'all': ").strip()
        
        if choice.lower() == 'all':
            for name, func in examples:
                try:
                    func()
                except Exception as e:
                    print(f"\n✗ Error in {name}: {e}")
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            name, func = examples[int(choice) - 1]
            try:
                func()
            except Exception as e:
                print(f"\n✗ Error: {e}")
        else:
            print("Invalid selection")
    except KeyboardInterrupt:
        print("\n\nAborted by user")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
