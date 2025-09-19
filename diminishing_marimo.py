import marimo as mo

__generated_with = "0.15.1"
app = mo.App()


@app.cell
def _():
    # `mo` (marimo) is already imported at the module level
    import numpy as np
    
    # Import plotly components using explicit from-import to avoid parsing issues
    try:
        from plotly import graph_objects as go
    except ImportError:
        # Fallback for environments where plotly is not available
        go = None

    # Import reusable functions/classes from the src package
    from interactive_functions import LogGrowth, PowerLawDecay, log_growth, power_law_decay
    from interactive_functions.md_docs_parser import doc_to_markdown
    return (
        LogGrowth,
        PowerLawDecay,
        doc_to_markdown,
        go,
        log_growth,
        mo,
        np,
        power_law_decay,
    )


@app.cell
def _():
    mo.md(
        r"""
    # Diminishing Returns
    Explore diminishing return shapes like power-law and logarithmic curves.
    """
    )
    return


@app.cell
def _(doc_to_markdown, power_law_decay):
    mo.md(f"""{doc_to_markdown(power_law_decay)}""")
    return


@app.cell
def _():
    a = mo.ui.slider(0.1, 5.0, value=1.5, step=0.1, label="a")
    p = mo.ui.slider(0.1, 5.0, value=1.0, step=0.1, label="p")
    b = mo.ui.slider(-5, 5.0, value=0.0, step=0.1, label="b")
    mo.hstack([a, p, b])
    return a, b, p


@app.cell
def _(PowerLawDecay, a, b, go, np, p):
    x = np.linspace(0.00001, 1, 1000)
    f = PowerLawDecay(a=a.value, p=p.value, b=b.value)
    y = f(x)
    fig = go.Figure(go.Scatter(x=x, y=y, name="power-law"))
    fig.add_hline(y=0, line_dash="dot", line_color="gray")
    fig.update_layout(
        title=fr"Power-law<br>{f.math_str()}<br><sup>{f.params_str()}</sup>",
        xaxis_title="x",
        yaxis_title="f(x)",
        yaxis_range=(-0, 100),
    )

    mo.ui.plotly(fig)
    return


@app.cell
def _(doc_to_markdown, log_growth):
    mo.md(f"""{doc_to_markdown(log_growth)}""")
    return


@app.cell
def _():
    a2 = mo.ui.slider(0.05, 50.0, value=1.0, step=0.01, label="a")
    b2 = mo.ui.slider(0.01, 5.0, value=1.0, step=0.01, label="b")
    mo.hstack([a2, b2])
    return a2, b2


@app.cell
def _(LogGrowth, a2, b2, go, np):
    x2 = np.linspace(0.001, 100, 800)
    g = LogGrowth(a=a2.value, b=b2.value)
    y2 = g(x2)
    fig2 = go.Figure(go.Scatter(x=x2, y=y2, name="log"))
    fig2.add_vline(x=max(0.0, -b2.value), line_dash="dot", line_color="gray", annotation_text="domain start")
    fig2.update_layout(
        title=fr"Logarithmic growth<br>{g.math_str()}<br><sup>{g.params_str()}</sup>",
        xaxis_title="x",
        yaxis_title="f(x)",
        xaxis_range=(0, 100),
        yaxis_range=(-10, 10),
    )
    mo.ui.plotly(fig2)
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
