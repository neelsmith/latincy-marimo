# latincy-marimo

This repository hosts [marimo notebooks](https://marimo.io) illustrating how to use `latincy` text models for Latin text analysis. 


Some notebooks include parallel versions for manual text input (by typing or pasting into a text field), reading text from a plain-text file, and reading text from a delimited-text file. Delimited-text files should have two columns, with a canonical reference in the first column and the corresponding text content in the second column. `data/vergileclogues.cex` is a delimited-text file with a text of Virgil's *Eclogues* formatted in this way.



## Demo notebooks



- *Lemmatization*. `marimo/lemmatization/latin-manual.py`, `marimo/lemmatization/latin-delimitedfile.py` and `marimo/lemmatization/latin-plainttext.py` use `latincy` to count the frequencies of individual tokens and their lemmas (dictionary forms).
- *Syntactic analysis*. `marimo/syntax/syntax-manual.py` and `marimo/syntax/syntax-delimitedfile.py` use `latincy` to analyze the syntactic structure ("dependencies") of a text, and to visualize the analysis both as mermaid diagrams and tabular data.

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
marimo edit marimo/lemmatization/latin-manual.py
```

or 

```bash
marimo run marimo/lemmatization/latin-manual.py
```

### Note on installation

`uv sync --no-install-project` installs runtime dependencies defined in `pyproject.toml`, including `marimo`, `spacy`, and `latincy` text models from Hugging Face, using a direct wheel URL for the Hugging Face models.