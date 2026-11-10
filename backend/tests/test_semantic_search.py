import numpy as np
import pandas as pd
import pytest

from backend.config.settings import resolve_faiss_max_distance
import backend.search.semantic as semantic


class StubEncoder:
    def encode(self, _queries, convert_to_numpy=True):
        return np.array([[1.0]], dtype=np.float32)


class StubIndex:
    def __init__(self, distances, indices):
        self.distances = np.array([distances], dtype=np.float32)
        self.indices = np.array([indices], dtype=np.int64)

    def search(self, _embedding, _top_k):
        return self.distances, self.indices


class DiagnosticEncoder:
    def get_sentence_embedding_dimension(self):
        return 2


class DiagnosticIndex:
    metric_type = semantic.FAISS_L2_METRIC
    d = 2
    ntotal = 2


def configure_stub(monkeypatch, distances, indices):
    monkeypatch.setattr(semantic, "encoder", StubEncoder())
    monkeypatch.setattr(semantic, "faiss_index", StubIndex(distances, indices))
    monkeypatch.setattr(semantic, "df", pd.DataFrame({"scheme_name": ["near", "far"]}))


def test_semantic_candidates_prefers_lower_l2_distance(monkeypatch):
    configure_stub(monkeypatch, [4.0, 1.0], [1, 0])
    monkeypatch.setattr(semantic, "FAISS_MAX_DISTANCE", None)

    assert semantic.semantic_candidates("query", 2) == [(0, 1.0), (1, 4.0)]


def test_distance_above_configured_maximum_is_filtered(monkeypatch):
    configure_stub(monkeypatch, [1.0, 3.0], [0, 1])
    monkeypatch.setattr(semantic, "FAISS_MAX_DISTANCE", 2.0)

    assert semantic.semantic_candidates("query", 2) == [(0, 1.0)]


def test_distance_below_configured_maximum_is_retained(monkeypatch):
    configure_stub(monkeypatch, [1.5], [0])
    monkeypatch.setattr(semantic, "FAISS_MAX_DISTANCE", 2.0)

    assert semantic.semantic_candidates("query", 1) == [(0, 1.5)]


def test_invalid_indexes_are_ignored(monkeypatch):
    configure_stub(monkeypatch, [0.5, 1.0, 2.0], [-1, 2, 0])
    monkeypatch.setattr(semantic, "FAISS_MAX_DISTANCE", None)

    assert semantic.semantic_candidates("query", 3) == [(0, 2.0)]


def test_duplicate_faiss_indexes_keep_best_distance(monkeypatch):
    configure_stub(monkeypatch, [3.0, 0.5, 1.0], [0, 0, 1])
    monkeypatch.setattr(semantic, "FAISS_MAX_DISTANCE", None)

    assert semantic.semantic_candidates("query", 3) == [(0, 0.5), (1, 1.0)]


def test_missing_or_disabled_threshold_keeps_candidates(monkeypatch):
    configure_stub(monkeypatch, [5.0], [0])
    monkeypatch.setattr(semantic, "FAISS_MAX_DISTANCE", None)

    assert semantic.semantic_candidates("query", 1) == [(0, 5.0)]
    assert semantic.is_faiss_distance_allowed(5.0)


def test_legacy_threshold_is_ignored_without_explicit_opt_in():
    with pytest.warns(DeprecationWarning, match="ignored"):
        assert resolve_faiss_max_distance({"FAISS_MIN_SCORE": "0.2"}) is None


def test_legacy_threshold_requires_explicit_opt_in():
    environment = {
        "FAISS_MIN_SCORE": "0.2",
        "FAISS_ENABLE_LEGACY_MIN_SCORE": "1",
    }
    with pytest.warns(DeprecationWarning, match="deprecated"):
        assert resolve_faiss_max_distance(environment) == 0.2


def test_current_distance_configuration_takes_precedence():
    environment = {
        "FAISS_MAX_DISTANCE": "2.5",
        "FAISS_MIN_SCORE": "0.2",
    }
    assert resolve_faiss_max_distance(environment) == 2.5


def test_validate_search_resources_reports_l2_dimensions_counts_and_alignment():
    report = semantic.validate_search_resources(
        DiagnosticEncoder(), DiagnosticIndex(), pd.DataFrame({"scheme_name": ["a", "b"]})
    )

    assert report["metric_is_l2"] is True
    assert report["dimension_matches"] is True
    assert report["counts_equal"] is True
    assert report["row_alignment_verified"] is False


def test_validate_search_resources_reports_mismatches():
    class InvalidIndex:
        metric_type = 999
        d = 3
        ntotal = -1

    report = semantic.validate_search_resources(
        DiagnosticEncoder(), InvalidIndex(), pd.DataFrame({"scheme_name": ["a"]})
    )

    assert report["metric_is_l2"] is False
    assert report["dimension_matches"] is False
    assert report["vector_count_nonnegative"] is False
    assert report["counts_equal"] is False


def test_hybrid_candidates_uses_bm25_reciprocal_rank_fusion(monkeypatch):
    frame = pd.DataFrame({
        "scheme_name": ["General Support", "PM Kisan"],
        "details": ["general public assistance", "farmer income support"],
        "tags": ["general", "farmer agriculture kisan"],
    })
    monkeypatch.setattr(semantic, "df", frame)
    monkeypatch.setattr(semantic, "encoder", StubEncoder())
    monkeypatch.setattr(semantic, "faiss_index", StubIndex([0.1, 0.2], [0, 1]))
    monkeypatch.setattr(semantic, "FAISS_MAX_DISTANCE", None)
    monkeypatch.setattr(semantic, "BM25_ENABLED", True)
    semantic._bm25_cache = None

    candidates = semantic.hybrid_candidates("farmer kisan", 2)

    assert [index for index, _ in candidates] == [1, 0]
    assert candidates[0][1] == pytest.approx(0.2)  # Preserves the actual FAISS L2 value.
