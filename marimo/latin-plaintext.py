import marimo

__generated_with = "0.23.16"
app = marimo.App(
    width="columns",
    layout_file="layouts/latin-plaintext.grid.json",
)


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import spacy

    return mo, spacy


@app.cell
def _():
    return


@app.cell
def _(mo):
    mo.md("""
    # Find Latin token and lexeme counts for plain-text file using `latincy`
    """)
    return


@app.cell
def _(models):
    models
    return


@app.cell
def _(mo, models):
    mo.md(f"Using model `{models.value}`")
    return


@app.cell(hide_code=True)
def _(file_area):
    file_area
    return


@app.cell(hide_code=True)
def _(side_by_side):
    side_by_side
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## UI
    """)
    return


@app.cell
def _(mo):
    models = mo.ui.dropdown(
        options=["la_core_web_sm", "la_core_web_md", "la_core_web_lg"],  label="*Model to use*", value="la_core_web_sm"
    )
    return (models,)


@app.cell
def _(file_area, mo):
    uploadlabel = "*Please select a file to upload*:"
    if file_area.name():
        uploadlabel = f"Uploaded `{file_area.name()}`"
    mo.md(uploadlabel)
    return


@app.cell
def _():
    divider = "|"
    return


@app.cell
def _(mo):
    file_area = mo.ui.file(kind="area")
    return (file_area,)


@app.cell
def _(file_area):
    raw = file_area.contents()
    return (raw,)


@app.cell
def _(lemmalist, mo, tokenlemmalist):
    left_content = tokenlemmalist
    right_content = lemmalist

    # 1. Define left scrollable column
    left_col = mo.vstack([
        mo.md(f"### Frequency of individual *forms* (tokens)\n\n{left_content}")
    ]).style({
        "max-height": "900px",
        "overflow-y": "auto",
        "padding": "12px",
        "border": "1px solid #e2e8f0",
        "border-radius": "8px",
        "width": "100%"
    })

    # 2. Define right scrollable column
    right_col = mo.vstack([
        mo.md(f"### Frequency of *vocabulary items* (lexemes)\n\n{right_content}")
    ]).style({
        "max-height": "900px",
        "overflow-y": "auto",
        "padding": "12px",
        "border": "1px solid #e2e8f0",
        "border-radius": "8px",
        "width": "100%"
    })

    # 3. Combine side-by-side using hstack
    side_by_side = mo.hstack([left_col, right_col], widths="equal", gap=1)
    return (side_by_side,)


@app.cell
def _(file_area, raw):
    stringlines =[]
    if file_area.contents():
        stringlines = raw.decode("utf-8").splitlines()
    return (stringlines,)


@app.cell
def _(stringlines):
    fulltext = "\n".join([s for s in stringlines])
    return (fulltext,)


@app.cell
def _(lemmacounts):
    hapax = [cnt for cnt in lemmacounts if cnt[1] == 1]
    return (hapax,)


@app.cell
def _(hapax):
    len(hapax)
    return


@app.cell
def _(lemmacounts):
    len(lemmacounts)
    return


@app.cell
def _(tokencounts):
    len(tokencounts)
    return


@app.cell
def _(tokencounts):
    tokenhapax = [cnt for cnt in tokencounts if cnt[1] == 1]
    return (tokenhapax,)


@app.cell
def _(tokenhapax):
    len(tokenhapax)
    return


@app.cell
def _(lemmacounts):
    sum([cnt[1] for cnt in lemmacounts])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Analyze text
    """)
    return


@app.cell
def _(models, spacy):
    latinnlp = spacy.load(models.value)
    return (latinnlp,)


@app.cell
def _(fulltext, latinnlp):
    doc = latinnlp(fulltext)
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
def _():
    return


@app.cell
def _():
    from collections import Counter

    return (Counter,)


@app.cell
def _(Counter, lexical):
    lemmacounts = Counter([token.lemma_ for token in lexical]).most_common()
    return (lemmacounts,)


@app.cell
def _(Counter, lexical):
    tokencounts = Counter([token.text for token in lexical]).most_common()
    return (tokencounts,)


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
    tokenlist = "\n".join(["- " + f"{pr[0]} **{pr[1]}**" for pr in lemmacounts])
    return


@app.cell
def _(lemmacounts):
    lemmalist ="\n".join(["- " + f"{pr[0]} **{pr[1]}**" for pr in lemmacounts])
    return (lemmalist,)


@app.cell
def _(tokenlemmacounts):
    tokenlemmalist = "\n".join(["- " + f"{pr[0]} **{pr[1]}**" for pr in tokenlemmacounts])
    return (tokenlemmalist,)


if __name__ == "__main__":
    app.run()
