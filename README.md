# Vivre le bourget Map idee 🗺️💡

[![pipeline status](https://gitlab.com/Tonow/vivre-le-bourget-map-idee/badges/main/pipeline.svg)](https://gitlab.com/Tonow/vivre-le-bourget-map-idee/-/commits/main)
[![coverage report](https://gitlab.com/Tonow/vivre-le-bourget-map-idee/badges/main/coverage.svg)](https://gitlab.com/Tonow/vivre-le-bourget-map-idee/-/commits/main)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

---

## 🚀 Getting Started

### Requirements

* install [uv](https://docs.astral.sh/uv/getting-started/installation/)
* create virtual env `uv venv`
* activate env `source .venv/bin/activate`
* install requirement `uv pip install -r requirements.txt`
* run the application `uv run streamlit run cartes_des_idee.py`


### Setting up Pre-commit Hooks

This project uses **pre-commit** to ensure code quality and formatting are consistent across the team. To set up the hooks, make sure you have `pre-commit` installed and run the following command in your project directory:

```bash
uv install pre-commit
pre-commit install
