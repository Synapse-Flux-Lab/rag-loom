import os
import time
import pathlib
import pytest
import requests


DEFAULT_BASE_URL = "http://localhost:8000"


def _wait_for_ready(url: str, timeout: int = 120, interval: float = 2.0):
    start = time.time()
    last_err = None
    while time.time() - start < timeout:
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                return
        except Exception as e:
            last_err = e
        time.sleep(interval)
    raise TimeoutError(f"Timed out waiting for {url}: {last_err}")


@pytest.fixture(scope="session", autouse=True)
def wait_stack_ready():
    # Ensure core services are reachable before tests start
    _wait_for_ready("http://localhost:6333/readyz", timeout=180)
    _wait_for_ready("http://localhost:11434/api/tags", timeout=240)
    _wait_for_ready(os.environ.get("BASE_URL", f"{DEFAULT_BASE_URL}") + "/health", timeout=180)
    yield


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ.get("BASE_URL", DEFAULT_BASE_URL)


@pytest.fixture(scope="session")
def sample_text_path() -> str:
    return str(pathlib.Path(__file__).resolve().parents[1] / "data" / "sample.txt")


