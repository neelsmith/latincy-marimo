# latincy-marimo

This repository hosts [marimo notebooks](https://marimo.io) illustrating how to use `latincy` text models for Latin token and lexeme analysis. Marimo notebooks are in the `marimo` directory; sample texts are in the `data` directory.

`latin-manual.py` lets you enter Latin text (by typing or pasting into a text field), then uses `latincy` to count the frequencies of individual tokens and their lemmas (dictionary forms). `latin-delimitedfile.py` does the same thing after reading in a delimited-text file. The delimited-text file should have two columns, with a canonical reference in the first column and the corresponding text content in the second column. `data/vergileclogues.cex` is a delimited-text file with a text of Virgil's *Eclogues*.

## Installing and running

### Prerequisites

- python 3.10-3.13
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/)



### One-time set-up

```bash
uv venv
source .venv/bin/activate
uv sync --no-install-project
```

### Usage

Launch a notebook with normal `marimo` commands like:

```bash
marimo edit marimo/latin-manual.py
```

or 

```bash
marimo run marimo/latin-manual.py
```

### Note on installation

`uv sync --no-install-project` installs runtime dependencies defined in `pyproject.toml`, including `marimo`, `spacy`, and `la_core_web_sm`. The `latincy` model is installed from Hugging Face using a direct wheel URL. If you need to install it manually, run:

```bash
uv pip install --python .venv/bin/python "la-core-web-sm @ https://huggingface.co/latincy/la_core_web_sm/resolve/main/la_core_web_sm-3.9.6-py3-none-any.whl"
```
