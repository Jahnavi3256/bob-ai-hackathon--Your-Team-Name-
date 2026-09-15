# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project
Python 3.10+ · Streamlit dashboard · IBM watsonx.ai (Granite) · Pytest · GitHub Actions CI

## Critical: What Doesn't Exist Yet
- `requirements.txt` — missing; README references it but it has not been created
- `src/app/dashboard.py` — the Streamlit entry point; all `src/` submodule `__init__.py` files are empty stubs
- `bob_sessions/` — empty; Bob task exports must be added here for judging

## Commands
```bash
pip install -r requirements.txt          # install deps (after creating requirements.txt)
cp src/.env.example .env                 # NOTE: .env.example is inside src/, not project root
streamlit run src/app/dashboard.py       # run the app
pytest tests/ -v                         # run all tests
pytest tests/test_foo.py::test_name -v   # run a single test
```

## Environment Variables (from `src/.env.example`)
- `WATSONX_API_KEY`, `WATSONX_PROJECT_ID`, `WATSONX_URL` (default: `https://us-south.ml.cloud.ibm.com`)
- Never commit `.env` — it is gitignored

## CI Validation (`.github/workflows/validate.yml`)
Runs on every push to any branch. Will **fail** until:
- `src/` contains at least one file beyond `README.md` and `.env.example`
- `demo/demo-video-link.txt` has a real URL (not the placeholder)
- `README.md` has no `[Your Project Title Here]` or `[Your Team Name]` text
- `submission.yaml` field `team.track` is exactly one of: `AI` | `DevOps` | `Sustainability` | `Open`

## Docs Still Needing Content
- `docs/architecture.md` — still a template with placeholder `[bracketed]` text
- `docs/setup-guide.md` — still a template; the automated eval pipeline reads this file

## Submission Checklist (from `CONTRIBUTING.md`)
- `demo/screenshots/` needs ≥3 files named `01-*.png`, `02-*.png`, etc.
- `presentation/slides.pdf` must be added
- `bob_sessions/` needs exported Bob task histories (one per member)
