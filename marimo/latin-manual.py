import marimo

__generated_with = "0.23.16"
app = marimo.App(width="columns", layout_file="layouts/latin-manual.grid.json")


@app.cell(hide_code=True)
def _():
    import marimo as mo
    import spacy

    return mo, spacy


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Latin token and lexeme counts using `latincy`
    """)
    return


@app.cell(hide_code=True)
def _(text_area):
    text_area
    return


@app.cell
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
def _(lemmalist, mo, tokenlemmalist):
    # Results
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
def _(mo):
    text_area = mo.ui.text_area(value = "Tityre, tu patulae recubans sub tegmine fagi silvestrem tenui Musam meditaris avena.", label = "*Paste in or type Latin text to analyze*:", full_width=True)
    return (text_area,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Analyze text
    """)
    return


@app.cell
def _(spacy):
    latinnlp = spacy.load("la_core_web_sm")
    return (latinnlp,)


@app.cell
def _(latinnlp, text_area):
    doc = latinnlp(text_area.value)
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
    return


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
