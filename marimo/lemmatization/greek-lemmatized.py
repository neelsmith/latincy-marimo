import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import csv
    import io
    from pathlib import Path

    import marimo as mo
    import spacy

    return Path, csv, io, mo, spacy


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Token-by-token lemmatization of a delimited-text file using LatinCy Greek models

    Produces a table with one row for each token, with columns `token`, `passage`,
    `type`, `lemma` and `pos`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## UI
    """)
    return


@app.cell
def _(mo):
    delimiter_dict = mo.ui.dropdown(
        options={"pipe ('|')": "|", "comma": ",", "tab": "\t"},
        value="pipe ('|')",
        label="*Delimiter of source file*:",
    )
    return (delimiter_dict,)


@app.cell
def _(mo):
    output_delimiter_dict = mo.ui.dropdown(
        options={"pipe ('|')": "|", "comma": ",", "tab": "\t"},
        value="pipe ('|')",
        label="*Delimiter for downloaded table*:",
    )
    return (output_delimiter_dict,)


@app.cell
def _(mo):
    models = mo.ui.dropdown(
        options=["grc_dep_web_sm", "grc_dep_web_md", "grc_dep_web_lg"],
        label="*Model to use*",
        value="grc_dep_web_sm",
    )
    return (models,)


@app.cell
def _(mo):
    file_area = mo.ui.file(kind="area")
    return (file_area,)


@app.cell(hide_code=True)
def _(delimiter_dict, file_area, mo, models, output_delimiter_dict):
    uploadlabel = "*Please select a delimited-text file to upload*:"
    if file_area.name():
        uploadlabel = f"Uploaded `{file_area.name()}`"
    mo.vstack(
        [
            delimiter_dict,
            models,
            mo.md(f"Using model `{models.value}`"),
            mo.md(uploadlabel),
            file_area,
            output_delimiter_dict,
        ]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Read the file
    """)
    return


@app.cell
def _(delimiter_dict, file_area, mo):
    # Each line is expected to look like `urn<delimiter>text`.
    mo.stop(
        not file_area.value,
        mo.callout(mo.md("Upload a delimited-text file to begin."), kind="info"),
    )
    _divider = delimiter_dict.value
    _lines = file_area.contents().decode("utf-8").splitlines()
    # Split on the first delimiter only; skip blank or malformed lines.
    _pairs = [s.split(_divider, 1) for s in _lines if _divider in s]
    def _tokens_urn_prefix(urn):
        """Convert a CTS URN for a text passage into the URN prefix (up to and
        including the final colon) for its token-level edition.

        `urn:cts:greekLit:tlg0012.tlg001.msA.normalized:1.1` becomes
        `urn:cts:greekLit:tlg0012.tlg001.msA.normalized-tokens:`: the version
        (`msA`) is kept, and `-tokens` is appended to the exemplar
        (`normalized`). If the URN has a version but no exemplar, the exemplar
        `tokens` is added.
        """
        parts = urn.strip().split(":")
        if len(parts) >= 5:
            work = parts[3].split(".")
            if len(work) >= 4:
                work[-1] = work[-1] + "-tokens"
            else:
                work.append("tokens")
            parts[3] = ".".join(work)
        return ":".join(parts[:-1]) + ":"

    # Each entry: (token-edition URN prefix, passage reference, text), e.g.
    # (`urn:cts:greekLit:tlg0012.tlg001.msA.normalized-tokens:`, `1.1`, ...).
    passages = [
        (_tokens_urn_prefix(urn), urn.strip().split(":")[-1], text)
        for urn, text in _pairs
    ]
    return (passages,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Analyze text
    """)
    return


@app.cell
def _(mo, models, spacy):
    # If the selected model is not installed, say so rather than failing.
    try:
        greeknlp = spacy.load(models.value)
        load_error = None
    except OSError as err:
        greeknlp = None
        load_error = str(err)

    mo.stop(
        greeknlp is None,
        mo.callout(
            mo.md(
                f"Model `{models.value}` is not installed in this environment "
                f"(run `uv sync --extra greek`).\n\n`{load_error}`"
            ),
            kind="danger",
        ),
    )
    return (greeknlp,)


@app.cell
def _(greeknlp, passages):
    # Analyze each passage separately so every token belongs to one passage.
    # Token IDs (`t1`, `t2`, ...) are numbered from 1 within each passage,
    # counting every token (punctuation included). The `passage` column holds
    # the full token URN, e.g.
    # `urn:cts:greekLit:tlg0012.tlg001.msA.normalized-tokens:1.1.t1`.
    rows = []
    for (_prefix, _passage, _), _doc in zip(
        passages,
        greeknlp.pipe([t for _, _, t in passages]),
    ):
        _n = 0
        for _token in _doc:
            if _token.is_space:
                continue
            _n += 1
            rows.append(
                {
                    "token": _token.text,
                    "passage": f"{_prefix}{_passage}.t{_n}",
                    "type": "punctuation"
                    if (_token.is_punct or _token.pos_ == "PUNCT")
                    else "lexical",
                    "lemma": _token.lemma_,
                    "pos": _token.pos_,
                }
            )
    return (rows,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Results
    """)
    return


@app.cell
def _(Path, csv, file_area, io, mo, output_delimiter_dict, rows):
    _delim = output_delimiter_dict.value
    _ext = {"|": "psv", ",": "csv", "\t": "tsv"}[_delim]
    _buf = io.StringIO()
    _writer = csv.writer(_buf, delimiter=_delim, lineterminator="\n")
    _fields = ["token", "passage", "type", "lemma", "pos"]
    _writer.writerow(_fields)
    for _row in rows:
        _writer.writerow([_row[f] for f in _fields])

    _stem = Path(file_area.name()).stem if file_area.name() else "tokens"
    download = mo.download(
        data=_buf.getvalue().encode("utf-8"),
        filename=f"{_stem}-lemmatized.{_ext}",
        mimetype="text/plain",
        label="Download table as delimited text",
    )
    return (download,)


@app.cell
def _(download, mo, rows):
    mo.vstack(
        [
            mo.md(f"**{len(rows)}** tokens"),
            download,
            mo.ui.table(rows, page_size=50, selection=None),
        ]
    )
    return


if __name__ == "__main__":
    app.run()
