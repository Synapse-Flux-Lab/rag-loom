import pytest
import requests


pytestmark = pytest.mark.e2e


def test_ingest_search_generate_flow(base_url: str, sample_text_path: str):
    # Ingest sample file
    with open(sample_text_path, "rb") as f:
        files = {"file": ("sample.txt", f, "text/plain")}
        r = requests.post(f"{base_url}/api/v1/ingest", files=files, timeout=60)
    assert r.status_code == 200, r.text
    ingest_data = r.json()
    assert ingest_data.get("chunks_created", 0) >= 1 or ingest_data.get("message")

    # Search for a term present in sample.txt
    search_payload = {
        "query": "embeddings",
        "top_k": 3,
        "similarity_threshold": 0.0
    }
    r = requests.post(f"{base_url}/api/v1/search", json=search_payload, timeout=30)
    assert r.status_code == 200, r.text
    results = r.json()
    assert isinstance(results, list)
    assert len(results) >= 1
    first = results[0]
    # Flexible shape assertions
    assert any(k in first for k in ["content", "text", "chunk"])  # text field
    assert any(k in first for k in ["similarity_score", "score", "similarity"])  # score field

    # Generate answer using retrieved context
    gen_payload = {
        "query": "Explain how RAG uses embeddings and a vector database.",
        "temperature": 0.1,
        "max_tokens": 128,
        "search_params": {
            "query": "RAG embeddings vector database",
            "top_k": 3,
            "similarity_threshold": 0.0
        }
    }
    r = requests.post(f"{base_url}/api/v1/generate", json=gen_payload, timeout=120)
    assert r.status_code == 200, r.text
    gen = r.json()
    assert isinstance(gen.get("answer", ""), str) and len(gen["answer"]) > 0
    assert isinstance(gen.get("sources", []), list) and len(gen["sources"]) >= 1


