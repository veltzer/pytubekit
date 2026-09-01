# Development Guide

## Prerequisites

- Python >= 3.14
- A Google Cloud project with the YouTube Data API v3 enabled
- OAuth2 client credentials at `~/.config/pytubekit/client_secret.json` (required to build a release: the build hook copies it into the package)

## Setting Up a Development Environment

```bash
git clone https://github.com/veltzer/pytubekit.git
cd pytubekit
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install pytest mypy ruff pylint
```

## Running Tests

```bash
# Run unit tests
pytest tests

# Run the full CI suite (tests + linting + type checking)
rsconstruct build
```

The rsconstruct build runs:

1. `pytest tests` - unit tests
2. `ruff check` - linter
3. `pylint` - code analysis
4. `mypy` - type checking
5. `luacheck` on `config/`, `taplo` on the TOML files and `actionlint` on the workflows

## Code Quality Tools

| Tool | Config File | Purpose |
|------|------------|---------|
| ruff | `pyproject.toml` (`[tool.ruff]`) | Linting, line length = 130 |
| pylint | `.pylintrc` | Code analysis |
| mypy | `pyproject.toml` (`[tool.mypy]`) | Static type checking |
| pytest | `pyproject.toml` (`[tool.pytest.ini_options]`) | Test runner, pythonpath = `["src"]` |

## Project Layout

Source code lives in `src/pytubekit/` following the `src` layout convention. The `pyproject.toml` configures pytest to include `src` in the Python path.

## Code Generation with rsconstruct

`README.md` and `src/pytubekit/static.py` are rendered from tera templates in `tera.templates/` by rsconstruct. The source of truth for project metadata lives in the `config/` directory:

- `config/project.lua` - Project name, description, keywords
- `config/version.lua` - Version tuple
- `config/personal.lua` - Author details

To regenerate files, run:

```bash
rsconstruct build
```

Do not manually edit the generated files (`README.md`, `static.py`). Edit the templates or config files instead. `pyproject.toml` is hand-edited and is the authoritative dependency list.

## Adding a New CLI Command

1. Define any new configuration classes in `src/pytubekit/configs.py`:

```python
class ConfigMyFeature(Config):
    """ Parameters for my feature """
    my_param = ParamCreator.create_str(
        help_string="Description of the parameter",
        default="default_value",
    )
```

2. Add the endpoint function in `src/pytubekit/main.py`:

```python
@register_endpoint(
    description="Description of what this command does",
    configs=[ConfigMyFeature],
)
def my_command() -> None:
    youtube = get_youtube()
    # ... implementation
```

3. Import the new config class at the top of `main.py`.

The command will automatically be available as `pytubekit my_command`.

## YouTube API Notes

### Deleted and Private Videos

When listing playlist items, the YouTube API returns deleted videos with the title `"Deleted video"` and private videos with the title `"Private video"`. Fetching video details for a deleted video returns an empty `items` array.

### Pagination

The YouTube API returns at most 50 items per request. The `PagedRequest` class in `util.py` handles pagination automatically by following `nextPageToken` values.

### API Quota

The YouTube Data API v3 has a daily quota of 10,000 units. Different operations consume different amounts of quota. If you hit the limit, wait until the next day.

### Test Video IDs

For manual testing:

| Type | Video ID |
|------|----------|
| Regular video | `xL_sMXfzzyA` |
| Deleted video | `6k2nFwVqQFw` |
| Private video | `MZnlL8uCCU0` |

## CI/CD

The project uses GitHub Actions (`.github/workflows/build.yml`) running on Ubuntu 26.04 with Python 3.14.

## Building the Documentation

The documentation site lives in the `mkdocs/` directory and uses [MkDocs](https://www.mkdocs.org/) with the [Material](https://squidfundamental.github.io/mkdocs-material/) theme.

### Install dependencies

```bash
pip install mkdocs-material
```

### Preview locally

```bash
cd mkdocs
mkdocs serve
```

Then open <http://127.0.0.1:8000> in your browser. Changes to the Markdown files are picked up automatically.

### Build the static site

```bash
cd mkdocs
mkdocs build
```

The output goes to `mkdocs/site/` (git-ignored).

### Deploy to GitHub Pages

```bash
cd mkdocs
mkdocs gh-deploy
```

This builds the site and pushes it to the `gh-pages` branch. In the GitHub repository settings, set Pages source to "Deploy from a branch" with `gh-pages` / `/ (root)`.
