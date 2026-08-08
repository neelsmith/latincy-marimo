import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import spacy

    return (spacy,)


@app.cell(hide_code=True)
def _(models):
    models
    return


@app.cell(hide_code=True)
def _(mo, models):
    mo.md(f"""Using model `{models.value}`""")
    return


@app.cell
def _(text_area):
    text_area
    return


@app.cell
def _(doc, mo):
    sdict = {f"{sentidx+1}: {sent[:3]}...":sentidx for sentidx, sent in enumerate(doc.sents)}
    smenu = mo.ui.dropdown(options=sdict, label="*Sentence to analyze*:")
    smenu
    return sdict, smenu


@app.cell
def _(orientation):
    orientation.value
    return


@app.cell
def _(mo):
    orientation = mo.ui.dropdown(options={"horizontally": "RL", "vertically": "BT"}, value="vertically", label="*Orient graph*")

    orientation
    return (orientation,)


@app.cell
def _(smenu):
    smenu.selected_key
    return


@app.cell
def _(doc, sdict, smenu):
    schoice = None
    if smenu.selected_key:
        stidx = sdict[smenu.selected_key]
        schoice = [s for senum, s in enumerate(doc.sents) if senum == stidx][0]

    return (schoice,)


@app.cell
def _(schoice):
    syntaxdata = tabulatesyntax(schoice)
    return (syntaxdata,)


@app.cell
def _(mo, schoice):
    mo.md(f"Analysis of sentence: *{schoice}*")
    return


@app.cell
def _(mo, syntaxdata):
    mo.md(syntaxtable_md(syntaxdata))
    return


@app.cell
def _(mo, orientation, syntaxdata):
    mo.mermaid(mermaidifytable(syntaxdata, orientation.value))
    return


@app.function
def mermaidrow(r):
    token,id,head,headid,relation = r.split("|")
    return f"{id}[{token}] -- \"{relation}\" --> {headid}[{head}]"


@app.function
def mermaidifytable(tbl, orient):
    hdr = f"graph {orient}\n\n"
    return hdr + "\n".join([mermaidrow(r) for r in tbl.split("\n")])


@app.cell
def _(syntaxdata):
    syntaxdata
    return


@app.cell
def _():
    #Jakob1["Jakob Saudek"] --> JakobRozel([ ])
    # A -- "text" --> B
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Tabular summary of passage syntax
    """)
    return


@app.cell
def _(doc, mo):
    stables = [f"## Sentence {sentidx+1}\n{syntaxtable_md(tabulatesyntax(sent))}" for sentidx, sent in enumerate(doc.sents)]
    mo.md("\n\n".join(stables))
    
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## UI
    """)
    return


@app.cell
def _(mo):
    text_area = mo.ui.text_area(value = "ac plerique suam ipsi vitam narrare fiduciam potius morum quam adrogantiam arbitrati sunt, nec id Rutilio et Scauro citra fidem aut obtrectationi fuit: adeo virtutes isdem temporibus optime aestimantur, quibus facillime gignuntur. at nunc narraturo mihi vitam defuncti hominis venia opus fuit, quam non petissem incusaturus: tam saeva et infesta virtutibus tempora.", full_width=True)
    return (text_area,)


@app.cell
def _(mo):
    models = mo.ui.dropdown(
        options=["la_core_web_sm", "la_core_web_md", "la_core_web_lg"],  label="*Model to use*", value="la_core_web_sm"
    )
    return (models,)


@app.cell
def _(mo):
    mo.md("""
    ## Analysis
    """)
    return


@app.cell
def _(models, spacy):
    latinnlp = spacy.load(models.value)
    return (latinnlp,)


@app.cell
def _(latinnlp, text_area):
    doc = latinnlp(text_area.value)
    return (doc,)


@app.cell
def _():
    return


@app.cell
def _(doc):
    [t for t in doc[:25]]
    return


@app.cell
def _(doc):
    eg = [t for t in doc if t.idx == 75][0]
    syntaxrow(eg)
    return


@app.function
def syntaxrow(node):
    "Format syntactic relation of a node as a table row."
    divider = "|"
    return f"{node.text}{divider}{node.idx}{divider}{node.head.text}{divider}{node.head.idx}{divider}{node.dep_}"


@app.function
def tabulatesyntax(nlpdoc):
    "Organize syntactic tree as a tabular structure."
    return "\n".join([syntaxrow(tokn) for tokn in nlpdoc])


@app.function
def syntaxtable_md(tbl):
    "Make markdown for syntax table"
    rows = tbl.split("\n")
    mdrows = ["|" + r + "|" for r in rows]
    return "|Token|id|Head|head id|Relation|\n|---|---|---|---|---|\n" + "\n".join(mdrows)


@app.cell
def _(doc):
    for sidx, s in enumerate(doc.sents):
        print(f"{sidx}. {s}")
    return


@app.cell
def _():
    #for token in doc:
    #    print(token.text, token.dep_, token.head.text, token.head.pos_,
    #            [child for child in token.children])
    return


@app.cell
def _(doc):
    for chunk in doc.noun_chunks:
        print(chunk.text, chunk.root.text, chunk.root.dep_,
                chunk.root.head.text)

    return


@app.cell
def _(doc):
    doc.sents
    return


if __name__ == "__main__":
    app.run()
