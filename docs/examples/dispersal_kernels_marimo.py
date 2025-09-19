from __future__ import annotations

import sys
from pathlib import Path

import marimo


def _ensure_project_src_on_path() -> None:
    """Add the project's src directory to sys.path if available."""

    file_path = Path(__file__).resolve()
    potential_roots = [file_path.parent, *file_path.parents]

    for root in potential_roots:
        if (root / "pyproject.toml").exists():
            src_dir = root / "src"
            if src_dir.exists() and str(src_dir) not in sys.path:
                sys.path.insert(0, str(src_dir))
            return


_ensure_project_src_on_path()

__generated_with = "0.15.1"
app = marimo.App()


@app.cell
async def _(app_version="0.1.0"):
    import sys
    if sys.platform == "emscripten":
        try:  # pragma: no cover - only runs in Pyodide
            import interactive_functions  # type: ignore  # noqa: F401
        except ModuleNotFoundError:
            # Fetch and exec the lightweight helper, then run the installer
            from urllib.parse import urljoin

            from js import __md_scope, fetch  # type: ignore

            base_href = str(__md_scope.href)
            if not base_href.endswith("/"):
                base_href += "/"
            helper_url = urljoin(base_href, "assets/py/pyodide_utils.py")

            print("Loading Pyodide helper...", helper_url)
            resp = await fetch(helper_url)
            code = await resp.text()
            scope: dict = {}
            exec(code, scope)
            await scope["ensure_local_wheel_installed"]("interactive_functions")

    return app_version


@app.cell
def _(app_version="0.1.0"):
    import marimo as mo
    import numpy as np
    
    # Import plotly components using explicit from-import to avoid parsing issues
    try:
        from plotly import graph_objects as go
    except ImportError:
        # Fallback for environments where plotly is not available
        go = None

    from interactive_functions import (
        ExponentialKernel,
        ExpPowerKernel,
        GaussianKernel,
        PowerLawKernel,
        RectangularHyperbolaKernel,
        kernel_exponential,
        kernel_exppower,
        kernel_gaussian,
        kernel_powerlaw,
        kernel_rectangular_hyperbola,
    )
    from interactive_functions.md_docs_parser import doc_to_markdown
    return (
        ExpPowerKernel,
        ExponentialKernel,
        GaussianKernel,
        PowerLawKernel,
        RectangularHyperbolaKernel,
        doc_to_markdown,
        go,
        kernel_exponential,
        kernel_exppower,
        kernel_gaussian,
        kernel_powerlaw,
        kernel_rectangular_hyperbola,
        mo,
        np,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
    # Dispersal Kernels
    Explore common dispersal kernels and how parameters affect tail behavior.
    """
    )
    return


@app.cell
def _(doc_to_markdown, kernel_exponential, mo):
    mo.md(f"""{doc_to_markdown(kernel_exponential)}""")
    return


@app.cell
def _(mo):
    lam_exp = mo.ui.slider(0.1, 100.0, value=10.0, step=0.1, label="lambda (scale)")
    mo.hstack([lam_exp])
    return (lam_exp,)


@app.cell
def _(ExponentialKernel, go, lam_exp, mo, np):
    r_exp = np.linspace(0.0, 200.0, 800)
    k_exp = ExponentialKernel(lam=lam_exp.value)
    y_exp = k_exp(r_exp)
    fig_exp = go.Figure(go.Scatter(x=r_exp, y=y_exp, name="exponential"))
    fig_exp.update_layout(
        title=fr"Exponential kernel<br>{k_exp.math_str()}<br><sup>{k_exp.params_str()}</sup>",
        yaxis_range=[-0.10, 1],
        xaxis_title="r",
        yaxis_title="K(r)",
    )
    mo.ui.plotly(fig_exp)
    return


@app.cell
def _():
    # Display symbolic math and parameters separately
    return


@app.cell
def _(doc_to_markdown, kernel_gaussian, mo):
    mo.md(f"""{doc_to_markdown(kernel_gaussian)}""")
    return


@app.cell
def _(mo):
    sigma_gauss = mo.ui.slider(0.1, 100.0, value=10.0, step=0.1, label="sigma (scale)")
    mo.hstack([sigma_gauss])
    return (sigma_gauss,)


@app.cell
def _(GaussianKernel, go, mo, np, sigma_gauss):
    r_gauss = np.linspace(0.0, 200.0, 800)
    g_gauss = GaussianKernel(sigma=sigma_gauss.value)
    y_gauss = g_gauss(r_gauss)
    fig_gauss = go.Figure(go.Scatter(x=r_gauss, y=y_gauss, name="gaussian"))
    fig_gauss.update_layout(
        title=fr"Gaussian kernel<br>{g_gauss.math_str()}<br><sup>{g_gauss.params_str()}</sup>",
        yaxis_range=[-0.10, 1],
        xaxis_title="r",
        yaxis_title="K(r)",
    )
    mo.ui.plotly(fig_gauss)
    return


@app.cell
def _(doc_to_markdown, kernel_powerlaw, mo):
    mo.md(f"""{doc_to_markdown(kernel_powerlaw)}""")
    return


@app.cell(hide_code=True)
def _(mo):
    alpha_pl = mo.ui.slider(0.1, 100.0, value=10.0, step=0.1, label="alpha (scale)")
    p_pl = mo.ui.slider(0.1, 10.0, value=2.0, step=0.1, label="p (tail exponent)")
    mo.hstack([alpha_pl, p_pl])
    return alpha_pl, p_pl


@app.cell
def _(PowerLawKernel, alpha_pl, go, mo, np, p_pl):
    r_pl = np.linspace(0.0, 200.0, 800)
    pl_kernel = PowerLawKernel(alpha=alpha_pl.value, p=p_pl.value)
    y_pl = pl_kernel(r_pl)
    fig_pl = go.Figure(go.Scatter(x=r_pl, y=y_pl, name="power-law"))
    fig_pl.update_layout(
        title=fr"Power-law kernel<br>{pl_kernel.math_str()}<br><sup>{pl_kernel.params_str()}</sup>",
        yaxis_range=[-0.10, 1],
        xaxis_title="r",
        yaxis_title="K(r)",
    )
    mo.ui.plotly(fig_pl)
    return


@app.cell
def _(doc_to_markdown, kernel_rectangular_hyperbola, mo):
    mo.md(f"""{doc_to_markdown(kernel_rectangular_hyperbola)}""")
    return


@app.cell(hide_code=True)
def _(mo):
    alpha_rh = mo.ui.slider(0.1, 100.0, value=10.0, step=0.1, label="alpha (scale)")
    p_rh = mo.ui.slider(0.1, 10.0, value=2.0, step=0.1, label="p (shape)")
    mo.hstack([alpha_rh, p_rh])
    return alpha_rh, p_rh


@app.cell
def _(RectangularHyperbolaKernel, alpha_rh, go, mo, np, p_rh):
    r_rh = np.linspace(0.0, 200.0, 800)
    rh_kernel = RectangularHyperbolaKernel(alpha=alpha_rh.value, p=p_rh.value)
    y_rh = rh_kernel(r_rh)
    fig_rh = go.Figure(go.Scatter(x=r_rh, y=y_rh, name="rectangular hyperbola"))
    fig_rh.update_layout(
        title=fr"Rectangular hyperbola kernel<br>{rh_kernel.math_str()}<br><sup>{rh_kernel.params_str()}</sup>",
        yaxis_range=[-0.10, 1],
        xaxis_title="r",
        yaxis_title="K(r)",
    )
    mo.ui.plotly(fig_rh)
    return


@app.cell
def _(doc_to_markdown, kernel_exppower, mo):
    mo.md(f"""{doc_to_markdown(kernel_exppower)}""")
    return


@app.cell(hide_code=True)
def _(mo):
    lam_ep = mo.ui.slider(0.1, 100.0, value=10.0, step=0.1, label="lambda (scale)")
    q_ep = mo.ui.slider(0.1, 4.0, value=1.5, step=0.1, label="q (shape)")
    mo.hstack([lam_ep, q_ep])
    return lam_ep, q_ep


@app.cell
def _(ExpPowerKernel, go, lam_ep, mo, np, q_ep):
    r_ep = np.linspace(0.0, 200.0, 800)
    ep_kernel = ExpPowerKernel(lam=lam_ep.value, q=q_ep.value)
    y_ep = ep_kernel(r_ep)
    fig_ep = go.Figure(go.Scatter(x=r_ep, y=y_ep, name="exp-power"))
    fig_ep.update_layout(
        title=fr"Exponential-power kernel<br>{ep_kernel.math_str()}<br><sup>{ep_kernel.params_str()}</sup>",
        yaxis_range=[-0.10, 1],
        xaxis_title="r",
        yaxis_title="K(r)",
    )
    mo.ui.plotly(fig_ep)
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
