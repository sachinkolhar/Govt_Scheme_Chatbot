"""FAISS Threshold Evaluation Pipeline Package"""

__version__ = "1.0.0"
__author__ = "Govt Scheme Chatbot Team"

from evaluation_pipeline import (
    QueryResult,
    ThresholdMetrics,
    calculate_metrics,
    evaluate_query,
    evaluate_threshold,
    export_csv,
    load_queries,
    load_search_resources,
    plot_results,
    print_recommendations,
    semantic_search,
)

__all__ = [
    "QueryResult",
    "ThresholdMetrics",
    "calculate_metrics",
    "evaluate_query",
    "evaluate_threshold",
    "export_csv",
    "load_queries",
    "load_search_resources",
    "plot_results",
    "print_recommendations",
    "semantic_search",
]
