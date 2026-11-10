import faiss
import numpy as np
import pandas as pd
import pytest

from backend.search.chunk_retrieval import ChunkRetriever


class StubEncoder:
    def get_sentence_embedding_dimension(self):
        return 2

    def encode(self, _queries, convert_to_numpy=True, normalize_embeddings=True):
        return np.array([[1.0, 0.0]], dtype=np.float32)


def make_retriever():
    chunks = pd.DataFrame([
        {
            "chunk_id": 0, "scheme_id": "A", "scheme_name": "Scheme A",
            "field_type": "benefits", "chunk_text": "A benefits",
            "level": "State", "normalized_categories": "agriculture",
        },
        {
            "chunk_id": 1, "scheme_id": "A", "scheme_name": "Scheme A",
            "field_type": "eligibility", "chunk_text": "A eligibility",
            "level": "State", "normalized_categories": "agriculture",
        },
        {
            "chunk_id": 2, "scheme_id": "B", "scheme_name": "Scheme B",
            "field_type": "benefits", "chunk_text": "B benefits",
            "level": "Central", "normalized_categories": "education",
        },
    ])
    vectors = np.array([
        [0.8, 0.6],
        [1.0, 0.0],
        [0.0, 1.0],
    ], dtype=np.float32)
    index = faiss.IndexFlatIP(2)
    index.add(vectors)
    return ChunkRetriever(chunks, index, StubEncoder())


def test_retrieve_groups_chunks_by_scheme_and_keeps_best_match():
    retriever = make_retriever()

    results = retriever.retrieve("test query", top_k_chunks=3, top_k_schemes=5)

    assert [item["scheme_id"] for item in results] == ["A", "B"]
    assert results[0]["chunk_id"] == 1
    assert results[0]["similarity"] == pytest.approx(1.0)
    assert results[1]["similarity"] == pytest.approx(0.0)


def test_level_filter_is_case_insensitive():
    results = make_retriever().retrieve("test", top_k_chunks=3, level="state")

    assert results
    assert all(item["level"] == "State" for item in results)
    assert all(item["scheme_id"] == "A" for item in results)


def test_field_type_filter():
    results = make_retriever().retrieve(
        "test", top_k_chunks=3, field_type="eligibility"
    )

    assert len(results) == 1
    assert results[0]["chunk_id"] == 1


def test_category_filter():
    results = make_retriever().retrieve(
        "test", top_k_chunks=3, category="education"
    )

    assert len(results) == 1
    assert results[0]["scheme_id"] == "B"


def test_empty_query_returns_no_results():
    assert make_retriever().retrieve("   ") == []


def test_invalid_faiss_indices_are_ignored(monkeypatch):
    retriever = make_retriever()

    class InvalidIndex:
        ntotal = 3
        d = 2
        metric_type = faiss.METRIC_INNER_PRODUCT

        def search(self, _query, _top_k):
            return (
                np.array([[0.9, 0.8, 0.7]], dtype=np.float32),
                np.array([[0, -1, 99]], dtype=np.int64),
            )

    retriever.index = InvalidIndex()
    results = retriever.retrieve("test", top_k_chunks=3)

    assert [item["chunk_id"] for item in results] == [0]


def test_mismatched_index_count_is_rejected():
    chunks = pd.DataFrame([
        {
            "chunk_id": 0, "scheme_id": "A", "scheme_name": "Scheme A",
            "field_type": "benefits", "chunk_text": "text", "level": "State",
        }
    ])
    index = faiss.IndexFlatIP(2)
    index.add(np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32))

    with pytest.raises(ValueError, match="metadata"):
        ChunkRetriever(chunks, index, StubEncoder())


def test_non_contiguous_chunk_ids_are_rejected():
    retriever = make_retriever()
    chunks = retriever.chunks.copy()
    chunks.loc[1, "chunk_id"] = 10

    with pytest.raises(ValueError, match="contiguous"):
        ChunkRetriever(chunks, retriever.index, StubEncoder())
