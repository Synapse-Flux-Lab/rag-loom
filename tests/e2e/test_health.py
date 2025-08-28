import pytest
import requests


pytestmark = pytest.mark.e2e


def test_health_ok(base_url: str):
    r = requests.get(f"{base_url}/health", timeout=15)
    assert r.status_code == 200, r.text
    data = r.json()
    # Accept flexible key naming; assert presence of common metadata
    assert any(k in data for k in ["status", "vector_store", "embedding_model", "llm_provider"])  # shape check


