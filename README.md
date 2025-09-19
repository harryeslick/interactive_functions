# interactive_functions

playground for viewing mathmatical functions

## Project Organization

- **[Copier](https://copier.readthedocs.io/)** - For templating and project generation
- **[uv](https://github.com/astral-sh/uv)** - For package and dependency management
- **[MkDocs](https://www.mkdocs.org/)** - For documentation with GitHub Pages deployment
- **[pytest](https://docs.pytest.org/)** - For testing with code coverage via pytest-cov
- **[pre-commit](https://pre-commit.com/)** - For enforcing code quality with ruff and codespell


## Development Setup

### Local Development

```bash
# Setup virtual environment and install dependencies
uv sync

# Install pre-commit hooks
pre-commit install-hooks
```

### Using VS Code DevContainer

1. Open project folder in VS Code
2. Install the "Remote - Containers" extension
3. Click "Reopen in Container" or run the "Remote-Containers: Reopen in Container" command

## Pyodide Deployment for Marimo Notebooks

This project includes marimo notebooks that can run in web browsers using Pyodide. To ensure proper deployment:

### Building and Deploying Wheels

The notebooks require the local `interactive_functions` package to be available in Pyodide. Since this package is not published to PyPI, we use a local wheel file:

1. **Build the wheel**: The `tools/export_notebooks_with_wheel.sh` script automatically builds a wheel and places it in `docs/assets/wheels/interactive_functions-latest-py3-none-any.whl`.

2. **Deploy with MkDocs**: The GitHub Actions workflow (`.github/workflows/mkdocs.yml`) runs the wheel build script before deploying to GitHub Pages.

3. **Notebook compatibility**: Marimo notebooks automatically detect the Pyodide environment and install the local wheel using:
   ```python
   from urllib.parse import urljoin
   import micropip
   from js import __md_scope

   base_href = str(__md_scope.href)
   if not base_href.endswith("/"):
       base_href += "/"
   wheel_url = urljoin(base_href, "assets/wheels/interactive_functions-latest-py3-none-any.whl")
   await micropip.install(wheel_url)
   ```

### For New Releases

When releasing a new version of the package:

1. Update the version in `src/interactive_functions/__init__.py`
2. The deployment process will automatically build a new wheel
3. The deployed notebooks will use the updated wheel

### Troubleshooting

- If notebooks fail to load with package import errors, verify that `docs/assets/wheels/interactive_functions-latest-py3-none-any.whl` exists
- Check the browser console for specific error messages
- Ensure the GitHub Pages deployment completed successfully
- Run `python tools/validate_pyodide_deployment.py` to check all deployment requirements

### Validation

Use the provided validation script to ensure your deployment setup is correct:

```bash
python tools/validate_pyodide_deployment.py
```

This script checks:
- Wheel file existence and validity
- Marimo notebook Pyodide compatibility
- URL construction patterns
