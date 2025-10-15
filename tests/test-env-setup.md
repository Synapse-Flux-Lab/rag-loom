# Test Environment Setup

Use the `test_env_setup.sh` helper to create a Python 3.12 virtual environment that is ready for unit and integration tests.

```bash
./utilscripts/test_env_setup.sh
```

## What the script does

- Locates a Python 3.12 interpreter (or use `--python /path/to/python3.12` to override).
- Creates a virtual environment at `./venv-tests` (customise with `--venv <dir>`).
- Upgrades `pip`, `setuptools`, and `wheel`.
- Installs runtime requirements (`requirements.txt`) and test-only packages (`tests/requirements-test.txt`).

## Optional arguments

| Flag | Description |
| ---- | ----------- |
| `--venv <dir>` | Store the virtual environment in a different directory. |
| `--python <binary>` | Explicitly choose the Python interpreter. Must be version 3.12.x. |
| `--torch-index <url>` | Provide a custom index for PyTorch wheels (for CPU-only installs use `https://download.pytorch.org/whl/cpu`). |

## After the script runs

```bash
source venv-tests/bin/activate
pytest tests/integration
```

Deactivate with `deactivate` when finished.

For more context on the testing workflow, see `tests/README.md`.
