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

`uv sync --no-install-project` installs runtime dependencies from [pyproject.toml](pyproject.toml), including `marimo`, `spacy`, and `la_core_web_sm` when compatible with your Python version.

Notes:

- On Python 3.13, `la_core_web_sm` may be unavailable. The notebooks should still run with a fallback pipeline.
- `uv sync` without `--no-install-project` may fail in this repository because setuptools auto-discovers multiple top-level directories (`data` and `marimo`).

## Run Marimo Notebooks

Start from the project root with your virtual environment active. Open a notebook in edit mode:

```bash
marimo edit marimo/latin-manual.py
```
un marimo edit latin-from_file.py
```

Run a notebook as an app:

```bash
marimo run marimo/latin-manual.py
```

The browser URL is printed in the terminal when Marimo starts.
