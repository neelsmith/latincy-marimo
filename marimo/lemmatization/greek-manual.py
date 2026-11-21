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
    # Greek token and lexeme counts using spaCy Greek models
    """)
    return


@app.cell(hide_code=True)
def _(mo, models, text_area):
    mo.vstack(
        [
            models,
            mo.md(f"Using model `{models.value}`"),
            text_area,
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
    # LatinCy Greek pipelines (small, medium, large), trained on the
    # UD Ancient Greek treebanks (PTNK, PROIEL, Perseus).
    model_names = ["grc_dep_web_sm", "grc_dep_web_md", "grc_dep_web_lg"]
    models = mo.ui.dropdown(
        options=model_names,
        label="*Model to use*",
        value="grc_dep_web_sm",
    )
    return (models,)


@app.cell
def _(mo):
    text_area = mo.ui.text_area(
        value="μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος οὐλομένην, ἣ μυρί᾽ Ἀχαιοῖς ἄλγε᾽ ἔθηκε.",
        label="*Paste in or type Greek text to analyze*:",
        full_width=True,
    )
    return (text_area,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Analyze text
    """)
    return


@app.cell
def _(mo, models, spacy):
    # Load the selected model; if it is not installed, say so and stop
    # downstream cells rather than showing a traceback.
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
                f"(add it to the project's dependencies).\n\n`{load_error}`"
            ),
            kind="danger",
        ),
    )
    return (greeknlp,)


@app.cell
def _(greeknlp, text_area):
    doc = greeknlp(text_area.value)
    return (doc,)


@app.cell
def _(doc):
    lexical = [token for token in doc if token.pos_ != "PUNCT"]
    return (lexical,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Counting
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
