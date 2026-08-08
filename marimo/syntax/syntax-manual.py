import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Latin syntactic analysis with `latincy`
    """)
    return


@app.cell(hide_code=True)
def _(displaytab, mo, models, orientation, smenu, text_area):
    mo.vstack([ mo.md("**Settings:**"), text_area,  mo.hstack([ models, mo.md(f"""***Using model*** `{models.value}`""")], justify="start", gap=0.01), mo.hstack([smenu, orientation, displaytab], justify="start")])
    return


@app.cell(hide_code=True)
def _(mo, schoice):
    showselection = None
    if schoice:
        tkntext = "\n".join([stkn.text for stkn in schoice])
    
        showselection = mo.md(f"""**Analysis of sentence**: *{tkntext}*""")
    showselection    
    return


@app.cell(hide_code=True)
def _(displaytab, mo, syntaxdata):
    resultstable = None
    if displaytab.value:
        resultstable =mo.md(syntax_mdtable(syntaxdata))

    resultstable    
    return


@app.cell(hide_code=True)
def _(tabdisplay):
    tabdisplay
    return


@app.cell(hide_code=True)
def _(mo):
    mo.Html("<hr/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    # Notebook implementation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## UI and user selections
    """)
    return


@app.cell
def _(mo):
    displaytab = mo.ui.checkbox(label="*Include graph data as table*")
    return (displaytab,)


@app.cell
def _(mo):
    orientation = mo.ui.dropdown(options={"horizontally": "RL", "vertically": "BT"}, value="vertically", label="*Orient graph*")
    return (orientation,)


@app.cell
def _(doc, mo):
    sdict = {f"{sentidx+1}: {sent[:3]}...":sentidx for sentidx, sent in enumerate(doc.sents)}
    smenu = mo.ui.dropdown(options=sdict, label="*Sentence to analyze*:")
    return sdict, smenu


@app.cell
def _(mo):
    text_area = mo.ui.text_area(value = "ac plerique suam ipsi vitam narrare fiduciam potius morum quam adrogantiam arbitrati sunt, nec id Rutilio et Scauro citra fidem aut obtrectationi fuit: adeo virtutes isdem temporibus optime aestimantur, quibus facillime gignuntur. at nunc narraturo mihi vitam defuncti hominis venia opus fuit, quam non petissem incusaturus: tam saeva et infesta virtutibus tempora.", full_width=True, label="*Text to analyze*:")
    return (text_area,)


@app.cell
def _(mo):
    models = mo.ui.dropdown(
        options=["la_core_web_sm", "la_core_web_md", "la_core_web_lg"],  label="*Model to use*", value="la_core_web_sm"
    )
    return (models,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Analysis
    """)
    return


@app.cell
def _():
    import spacy

    return (spacy,)


@app.cell
def _(models, spacy):
    latinnlp = spacy.load(models.value)
    return (latinnlp,)


@app.cell
def _(latinnlp, text_area):
    doc = latinnlp(text_area.value)
    return (doc,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Organizing and formatting data
    """)
    return


@app.cell
def _(doc, sdict, smenu):
    schoice = None
    if smenu.selected_key:
        stidx = sdict[smenu.selected_key]
        alltokens = [s for senum, s in enumerate(doc.sents) if senum == stidx][0]
        schoice = [lex for lex in alltokens if lex.is_punct == False]
    return (schoice,)


@app.cell
def _(schoice):
    syntaxdata = ""
    if schoice:
        syntaxdata = tabulatesyntax(schoice)
    return (syntaxdata,)


@app.cell
def _(mo, orientation, syntaxdata):
    tabdisplay = mo.md("*Choose a sentence to analyze*")
    if syntaxdata:
        tabdisplay = mo.mermaid(syntax_mermaid(syntaxdata, orientation.value))


    return (tabdisplay,)


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Library for working with spacy
    """)
    return


@app.function
def tabulatesyntax(nlpdoc):
    "Organize spacy syntactic tree as a tabular structure."
    return "\n".join([syntax_delimitedrow(tokn) for tokn in nlpdoc])


@app.function
def syntax_delimitedrow(node):
    "Format syntactic relation of a node as a row of delimited text."
    divider = "|"
    return f"{node.text}{divider}{node.idx}{divider}{node.head.text}{divider}{node.head.idx}{divider}{node.dep_}"


@app.function
def syntax_mdtable(tbl):
    "Format delimited-text table with syntax data as a Markdown table."
    rows = tbl.split("\n")
    mdrows = ["|" + r + "|" for r in rows]
    return "|Token|id|Head|head id|Relation|\n|---|---|---|---|---|\n" + "\n".join(mdrows)


@app.function
def syntax_mermaidrow(r):
    "Format syntactic relation of a node as node-edge-node in a Mermaid graph."
    token,id,head,headid,relation = r.split("|")
    return f"{id}[{token}] -- \"{relation}\" --> {headid}[{head}]"


@app.function
def syntax_mermaid(tbl, orient):
    "Format delimited-text table with syntax data as a Mermaid graph."
    hdr = f"graph {orient}\n\n"
    return hdr + "\n".join([syntax_mermaidrow(r) for r in tbl.split("\n")])


@app.cell(hide_code=True)
def _(mo):
    mo.md("""
    ## Notes
    """)
    return


if __name__ == "__main__":
    app.run()
