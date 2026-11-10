import pandas as pd

import backend.chat.pipeline as pipeline


def test_shared_pipeline_rejects_direct_candidates_over_l2_distance_limit(monkeypatch):
    frame = pd.DataFrame([
        {"scheme_name": "Distant", "eligibility": "", "benefits": ""},
        {"scheme_name": "Near", "eligibility": "", "benefits": ""},
    ])
    monkeypatch.setattr(pipeline, "FAISS_MAX_DISTANCE", 2.0)

    result = pipeline.resolve_scheme_candidates(
        "find schemes",
        candidate_indices=[(0, 3.0), (1, 1.0)],
        dataframe=frame,
    )

    assert [candidate.scheme["scheme_name"] for candidate in result.candidates] == ["Near"]
