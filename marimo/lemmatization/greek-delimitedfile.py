import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import spacy
    from collections import Counter

    return Counter, mo, spacy


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Greek token and lexeme counts for a delimited-text file using LatinCy Greek models
    """)
    return


@app.cell(hide_code=True)
def _(delimiter_dict, file_area, mo, models):
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
        ]
    )
    return


@app.cell(hide_code=True)
def _(lemmalist, mo, tokenlemmalist):
    _style = {
        "max-height": "900px",
        "overflow-y": "auto",
        "padding": "12px",
        "border": "1px solid #e2e8f0",
        "border-radius": "8px",
        "width": "100%",
    }
    left_col = mo.vstack(
        [mo.md(f"### Frequency of individual *forms* (tokens)\n\n{tokenlemmalist}")]
    ).style(_style)
    right_col = mo.vstack(
        [mo.md(f"### Frequency of *vocabulary items* (lexemes)\n\n{lemmalist}")]
    ).style(_style)
    mo.hstack([left_col, right_col], widths="equal", gap=1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html("<br/><br/><br/><br/><br/><br/><br/><br/><br/>")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Implementation
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
        label="*Delimiter*:",
    )
    return (delimiter_dict,)


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
def _(mo):
    mo.md("""
    ## Read the file
    """)
    return


@app.cell
def _(delimiter_dict, file_area, mo):
    # Each line is expected to look like `identifier<delimiter>text`.
    mo.stop(
        not file_area.value,
        mo.callout(
            mo.md("Upload a delimited-text file to begin."), kind="info"
        ),
    )
    divider = delimiter_dict.value
    stringlines = file_area.contents().decode("utf-8").splitlines()
    # Split only on the first delimiter so that delimiters inside the Greek
    # text (e.g. commas) are preserved; skip blank or malformed lines.
    fulltext = "\n".join(
        [s.split(divider, 1)[1] for s in stringlines if divider in s]
    )
    return (fulltext,)


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
def _(fulltext, greeknlp):
    doc = greeknlp(fulltext)
    return (doc,)


@app.cell
def _(doc):
    lexical = [token for token in doc if token.pos_ != "PUNCT"]
    return (lexical,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Count
    """)
    return


@app.cell
def _(Counter, lexical):
    lemmacounts = Counter([token.lemma_ for token in lexical]).most_common()
    return (lemmacounts,)


@app.cell
def _(lexical):
    tokenlemmastrings = [token.text + f" (< *{token.lemma_}*)" for token in lexical]
    return (tokenlemmastrings,)


@app.cell
def _(Counter, tokenlemmastrings):
    tokenlemmacounts = Counter(tokenlemmastrings).most_common()
    return (tokenlemmacounts,)


@app.cell
def _(lemmacounts):
    lemmalist = "\n".join(["- " + f"{pr[0]} **{pr[1]}**" for pr in lemmacounts])
    return (lemmalist,)


@app.cell
def _(tokenlemmacounts):
    tokenlemmalist = "\n".join(
        ["- " + f"{pr[0]} **{pr[1]}**" for pr in tokenlemmacounts]
    )
    return (tokenlemmalist,)


if __name__ == "__main__":
    app.run()
