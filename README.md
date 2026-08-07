# latincy-marimo

Marimo notebooks for experimenting with Latin token and lexeme analysis.

## Quick Start

```bash
uv venv
source .venv/bin/activate
uv sync --no-install-project
```

Then launch a notebook:

```bash
marimo edit marimo/latin-manual.py
```

## Prerequisites

- uv
- Python 3.10-3.13
- macOS/Linux shell (commands below use `bash`/`zsh` style)

## Instantiate The Project

From the project root:

```bash
uv venv
source .venv/bin/activate
uv sync --no-install-project
```

`uv sync --no-install-project` installs runtime dependencies from [pyproject.toml](pyproject.toml), including `marimo`, `spacy`, and `la_core_web_sm`.

The notebooks require `la_core_web_sm` to be installed in your environment. They do not include fallback behavior.

Notes:

- The model is installed from Hugging Face using a direct wheel URL.
- If you need to install it manually, run:

```bash
uv pip install --python .venv/bin/python "la-core-web-sm @ https://huggingface.co/latincy/la_core_web_sm/resolve/main/la_core_web_sm-3.9.6-py3-none-any.whl"
```
- `uv sync` without `--no-install-project` may fail in this repository because setuptools auto-discovers multiple top-level directories (`data` and `marimo`).

## Run Marimo Notebooks

Start from the project root with your virtual environment active. Open a notebook in edit mode:

```bash
marimo edit marimo/latin-manual.py
```

```bash
marimo edit marimo/latin-from_file.py
```

Run a notebook as an app:

```bash
marimo run marimo/latin-manual.py
```

The browser URL is printed in the terminal when Marimo starts.
