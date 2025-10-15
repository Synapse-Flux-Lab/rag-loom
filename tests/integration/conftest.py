import os
import sys
import tempfile
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient
from pytest import MonkeyPatch

# Normalise configuration so integration tests use local, test-friendly components.
os.environ.setdefault("VECTOR_STORE_TYPE", "chroma")
os.environ.setdefault("LLM_PROVIDER", "openai")
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("CHROMA_PERSIST_DIRECTORY", tempfile.mkdtemp(prefix="chroma-test-"))

GLOBAL_PATCH = MonkeyPatch()


class SentenceTransformerStub:
    def __init__(self, *_, **__):
        pass

    def encode(self, texts, convert_to_numpy=True):
        vectors = [[0.0, 0.0, 0.0] for _ in texts]
        if convert_to_numpy:
            try:
                import numpy as np
                return np.array(vectors)
            except Exception:
                return vectors
        return vectors


class OpenAIStub:
    def __init__(self, *_, **__):
        self.models = SimpleNamespace(list=lambda: [])
        self.chat = SimpleNamespace(
            completions=SimpleNamespace(
                create=lambda **__: SimpleNamespace(
                    choices=[SimpleNamespace(message=SimpleNamespace(content="stubbed-response"))]
                )
            )
        )


GLOBAL_PATCH.setattr("sentence_transformers.SentenceTransformer", SentenceTransformerStub, raising=False)
GLOBAL_PATCH.setattr("openai.OpenAI", OpenAIStub, raising=False)

# Ensure the app package is importable when tests run without an editable install.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.main import app


@pytest.fixture(scope="session", autouse=True)
def stub_external_dependencies():
    """Replace network-dependent services with lightweight test doubles."""
    from app.api.endpoints import ingestion as ingestion_module
    from app.core import embeddings as embeddings_module
    from app.core import vector_store as vector_module
    from app.services import llm_service as llm_module
    import app.main as main_module

    class DummyEmbeddingService:
        model_name = "test-embeddings"
        model_type = "test"

        def generate_embeddings(self, texts):
            return [[0.0] * 3 for _ in texts]

        def health(self):
            return {"status": "up", "model": self.model_name, "provider": self.model_type}

    class DummyVectorStore:
        provider = "test-vector"

        def __init__(self):
            self.chunks = []

        def store_chunks(self, chunks):
            self.chunks.extend(chunks)

        def health(self):
            return {"status": "up", "provider": self.provider}

    class DummyLLMService:
        provider = "test-llm"
        model_name = "test-llm-model"

        def health(self):
            return {"status": "up", "provider": self.provider, "model": self.model_name}

        def generate_response(self, *_, **__):
            return "stubbed-response"

    dummy_embedding = DummyEmbeddingService()
    dummy_vector = DummyVectorStore()
    dummy_llm = DummyLLMService()

    GLOBAL_PATCH.setattr(embeddings_module, "embedding_service", dummy_embedding, raising=False)
    GLOBAL_PATCH.setattr(vector_module, "vector_store", dummy_vector, raising=False)
    GLOBAL_PATCH.setattr(llm_module, "llm_service", dummy_llm, raising=False)

    # Ensure the FastAPI app references the same doubles.
    main_module.embedding_service = dummy_embedding
    main_module.vector_store = dummy_vector
    main_module.llm_service = dummy_llm
    ingestion_module.embedding_service = dummy_embedding
    ingestion_module.vector_store = dummy_vector

    yield

    GLOBAL_PATCH.undo()


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)
