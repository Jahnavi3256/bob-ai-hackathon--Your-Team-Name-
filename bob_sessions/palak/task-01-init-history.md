# /init

---

**Status:** active  **Date:** 2026-09-15

---

### 👤 User

<task>
Please analyze this codebase and create an AGENTS.md file containing:
1. Build/lint/test commands - especially for running a single test
2. Code style guidelines including imports, formatting, types, naming conventions, error handling, etc.
</task>

<initialization>
  <purpose>
    Create (or update) a concise AGENTS.md file that enables immediate productivity for AI assistants.
    Focus ONLY on project-specific, non-obvious information that you had to discover by reading files.

    CRITICAL: Only include information that is:
    - Non-obvious (couldn't be guessed from standard practices)
    - Project-specific (not generic to the framework/language)
    - Discovered by reading files (config files, code patterns, custom utilities)
    - Essential for avoiding mistakes or following project conventions

    Usage notes:
    - The file you create will be given to agentic coding agents (such as yourself) that operate in this repository
    - Keep the main AGENTS.md concise - aim for about 20 lines, but use more if the project complexity requires it
    - If there's already an AGENTS.md, improve it
    - If there are Claude Code rules (in CLAUDE.md), Cursor rules (in .cursor/rules/ or .cursorrules), or Copilot rules (in .github/copilot-instructions.md), make sure to include them
    - Be sure to prefix the file with: "# AGENTS.md\n\nThis file provides guidance to agents when working with code in this repository."
  </purpose>

  <todo_list_creation>
    If the update_todo_list tool is available, create a todo list with these focused analysis steps:

    1. Check for existing AGENTS.md files
       CRITICAL - Check these EXACT paths IN THE PROJECT ROOT:
       - AGENTS.md (in project root directory)
       - .bob/rules-agent/AGENTS.md (relative to project root)
       - .bob/rules-ask/AGENTS.md (relative to project root)
       - .bob/rules-plan/AGENTS.md (relative to project root)

       IMPORTANT: All paths are relative to the project/workspace root, NOT system root!

       If ANY of these exist:
       - Read them thoroughly
       - CRITICALLY EVALUATE: Remove ALL obvious information
       - DELETE entries that are standard practice or framework defaults
       - REMOVE anything that could be guessed without reading files
       - Only KEEP truly non-obvious, project-specific discoveries
       - Then add any new non-obvious patterns you discover

       Also check for other AI assistant rules:
       - .cursorrules, CLAUDE.md, .roorules
       - .cursor/rules/, .github/copilot-instructions.md

    2. Identify stack
       - Language, framework, build tools
       - Package manager and dependencies

    3. Extract commands
       - Build, test, lint, run
       - Critical directory-specific commands

    4. Map core architecture
       - Main components and flow
       - Key entry points

    5. Document critical patterns
       - Project-specific utilities (that you discovered by reading code)
       - Non-standard approaches (that differ from typical patterns)
       - Custom conventions (that aren't obvious from file structure)

    6. Extract code style
       - From config files only
       - Key conventions

    7. Testing specifics
       - Framework and run commands
       - Directory requirements

    8. Compile/Update AGENTS.md files
       - If files exist: AGGRESSIVELY clean them up
         * DELETE all obvious information (even if it was there before)
         * REMOVE standard practices, framework defaults, common patterns
         * STRIP OUT anything derivable from file structure or names
         * ONLY KEEP truly non-obvious discoveries
         * Then add newly discovered non-obvious patterns
         * Result should be SHORTER and MORE FOCUSED than before
       - If creating new: Follow the non-obvious-only principle
       - Create mode-specific files in .bob/rules-*/ directories (IN PROJECT ROOT)

    Note: If update_todo_list is not available, proceed with the analysis workflow directly without creating a todo list.
  </todo_list_creation>
</initialization>

<analysis_workflow>
  Follow the comprehensive analysis workflow to:

  1. **Discovery Phase**:
     CRITICAL - First check for existing AGENTS.md files at these EXACT locations IN PROJECT ROOT:
     - AGENTS.md (in project/workspace root)
     - .bob/rules-agent/AGENTS.md (relative to project root)
     - .bob/rules-ask/AGENTS.md (relative to project root)
     - .bob/rules-plan/AGENTS.md (relative to project root)

     IMPORTANT: The .bob folder should be created in the PROJECT ROOT, not system root!

     If found, perform CRITICAL analysis:
     - What information is OBVIOUS and must be DELETED?
     - What violates the non-obvious-only principle?
     - What would an experienced developer already know?
     - DELETE first, then consider what to add
     - The file should get SHORTER, not longer

     Also find other AI assistant rules and documentation

  2. **Project Identification**: Identify language, stack, and build system
  3. **Command Extraction**: Extract and verify essential commands
  4. **Architecture Mapping**: Create visual flow diagrams of core processes
  5. **Component Analysis**: Document key components and their interactions
  6. **Pattern Analysis**: Identify project-specific patterns and conventions
  7. **Code Style Extraction**: Extract formatting and naming conventions
  8. **Security & Performance**: Document critical patterns if relevant
  9. **Testing Discovery**: Understand testing setup and practices
  10. **Example Extraction**: Find real examples from the codebase
</analysis_workflow>

<output_structure>
  <main_file>
    Create or deeply improve AGENTS.md with ONLY non-obvious information:

    If AGENTS.md exists:
    - FIRST: Delete ALL obvious information
    - REMOVE: Standard commands, framework defaults, common patterns
    - STRIP: Anything that doesn't require file reading to know
    - EVALUATE: Each line - would an experienced dev be surprised?
    - If not surprised, DELETE IT
    - THEN: Add only truly non-obvious new discoveries
    - Goal: File should be SHORTER and MORE VALUABLE

    Content should include:
    - Header: "# AGENTS.md\n\nThis file provides guidance to agents when working with code in this repository."
    - Build/lint/test commands - ONLY if they differ from standard package.json scripts
    - Code style - ONLY project-specific rules not covered by linter configs
    - Custom utilities or patterns discovered by reading the code
    - Non-standard directory structures or file organizations
    - Project-specific conventions that violate typical practices
    - Critical gotchas that would cause errors if not followed

    EXCLUDE obvious information like:
    - Standard npm/yarn commands visible in package.json
    - Framework defaults (e.g., "React uses JSX")
    - Common patterns (e.g., "tests go in __tests__ folders")
    - Information derivable from file extensions or directory names

    Keep it concise (aim for ~20 lines, but expand as needed for complex projects).
    Include existing AI assistant rules from CLAUDE.md, Cursor rules (.cursor/rules/ or .cursorrules), or Copilot rules (.github/copilot-instructions.md).
  </main_file>

  <mode_specific_files>
    Create or deeply improve mode-specific AGENTS.md files IN THE PROJECT ROOT.

    CRITICAL: For each of these paths (RELATIVE TO PROJECT ROOT), check if the file exists FIRST:
    - .bob/rules-agent/AGENTS.md (relative to project root)
    - .bob/rules-ask/AGENTS.md (relative to project root)
    - .bob/rules-plan/AGENTS.md (relative to project root)

    IMPORTANT: The .bob directory must be created in the current project/workspace root directory,
    NOT at the system root (/) or home directory. All paths are relative to where the project is located.

    If files exist:
    - AGGRESSIVELY DELETE obvious information
    - Remove EVERYTHING that's standard practice
    - Strip out framework defaults and common patterns
    - Each remaining line must be surprising/non-obvious
    - Only then add new non-obvious discoveries
    - Files should become SHORTER, not longer

    Example structure (ALL IN PROJECT ROOT):
    ```
    project-root/
    ├── AGENTS.md                    # General project guidance
    ├── .bob/                        # IN PROJECT ROOT, NOT SYSTEM ROOT!
    │   ├── rules-agent/
    │   │   └── AGENTS.md           # Advance mode specific instructions
    │   ├── rules-ask/
    │   │   └── AGENTS.md           # Ask mode specific instructions
    │   └── rules-plan/
    │       └── AGENTS.md           # Plan mode specific instructions
    ├── src/
    ├── package.json
    └── ... other project files
    ```

    .bob/rules-agent/AGENTS.md - ONLY non-obvious advance coding rules discoveries:
    - Custom utilities that replace standard approaches
    - Non-standard patterns unique to this project
    - Hidden dependencies or coupling between components
    - Required import orders or naming conventions not enforced by linters
    - Access to tools like MCP and Browser

    Example of non-obvious rules worth documenting:
    ```
    # Project Coding Rules (Non-Obvious Only)
    - Always use safeWriteJson() from src/utils/ instead of JSON.stringify for file writes (prevents corruption)
    - API retry mechanism in src/api/providers/utils/ is mandatory (not optional as it appears)
    - Database queries MUST use the query builder in packages/evals/src/db/queries/ (raw SQL will fail)
    - Provider interface in packages/types/src/ has undocumented required methods
    - Test files must be in same directory as source for vitest to work (not in separate test folder)
    ```

    .bob/rules-ask/AGENTS.md - ONLY non-obvious documentation context:
    - Hidden or misnamed documentation
    - Counterintuitive code organization
    - Misleading folder names or structures
    - Important context not evident from file structure

    Example of non-obvious documentation rules worth documenting:
    ```
    # Project Documentation Rules (Non-Obvious Only)
    - "src/" contains VSCode extension code, not source for web apps (counterintuitive)
    - Provider examples in src/api/providers/ are the canonical reference (docs are outdated)
    - UI runs in VSCode webview with restrictions (no localStorage, limited APIs)
    - Package.json scripts must be run from specific directories, not root
    - Locales in root are for extension, webview-ui/src/i18n for UI (two separate systems)
    ```

    .bob/rules-plan/AGENTS.md - ONLY non-obvious architectural constraints:
    - Hidden coupling between components
    - Undocumented architectural decisions
    - Non-standard patterns that must be followed
    - Performance bottlenecks discovered through investigation

    Example of non-obvious architecture rules worth documenting:
    ```
    # Project Architecture Rules (Non-Obvious Only)
    - Providers MUST be stateless - hidden caching layer assumes this
    - Webview and extension communicate through specific IPC channel patterns only
    - Database migrations cannot be rolled back - forward-only by design
    - React hooks required because external state libraries break webview isolation
    - Monorepo packages have circular dependency on types package (intentional)
    ```
  </mode_specific_files>
</output_structure>

<quality_criteria>
  - ONLY include non-obvious information discovered by reading files
  - Exclude anything that could be guessed from standard practices
  - Focus on gotchas, hidden requirements, and counterintuitive patterns
  - Include specific file paths when referencing custom utilities
  - Be extremely concise - if it's obvious, don't include it
  - Every line should prevent a potential mistake or confusion
  - Test: Would an experienced developer be surprised by this information?
  - If updating existing files: DELETE obvious info first, files should get SHORTER
  - Measure success: Is the file more concise and valuable than before?
</quality_criteria>

Remember: The goal is to create documentation that enables AI assistants to be immediately productive in this codebase, focusing on project-specific knowledge that isn't obvious from the code structure alone.

---

### 🤖 Assistant

> 🔧 called: list_files

I'm in Ask mode, which is read-only. I can analyze the codebase and tell you exactly what should go in `AGENTS.md`, but I cannot write or create files. To actually create the file, you'll need to switch to **Agent mode**.

Let me do the analysis first so you have the full picture.

> 🔧 **list_files** — .

### 🤖 Assistant

> 🔧 called: list_files



> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-

### 🤖 Assistant

> 🔧 called: list_files, list_files



> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/tests

> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/src

### 🤖 Assistant

> 🔧 called: list_files, list_files, list_files



> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/src/app

> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/src/classifier

> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/src/capa

### 🤖 Assistant

> 🔧 called: read_file, read_file, read_file, read_file, read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/app/__init__.py

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/capa/__init__.py

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/classifier/__init__.py

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/scoring/__init__.py

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/rules/__init__.py

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/README.md

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/submission.yaml

### 🤖 Assistant

> 🔧 called: list_files, list_files



> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/docs

> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/demo

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/docs/architecture.md

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/docs/setup-guide.md

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/CONTRIBUTING.md

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/.env.example

### 🤖 Assistant

> 🔧 called: glob, glob



> 🔧 **glob** — bob-ai-hackathon--Your-Team-Name-/**/requirements*.txt

> 🔧 **glob** — bob-ai-hackathon--Your-Team-Name-/**/*.py

### 🤖 Assistant

> 🔧 called: glob, glob, glob



> 🔧 **glob** — bob-ai-hackathon--Your-Team-Name-/**/*.cfg

> 🔧 **glob** — bob-ai-hackathon--Your-Team-Name-/**/*.toml

> 🔧 **glob** — bob-ai-hackathon--Your-Team-Name-/.github/**/*

### 🤖 Assistant

> 🔧 called: list_files, list_files



> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/bob_sessions

> 🔧 **list_files** — bob-ai-hackathon--Your-Team-Name-/.github

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/.gitignore

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/.github/workflows/validate.yml

### 🤖 Assistant

Here's my full analysis. I cannot write the file myself in Ask mode — **please switch to Agent mode** to have it created. Here's exactly what the `AGENTS.md` should contain based on everything I discovered:

---

## Analysis Findings

### What this repo is
This is a **hackathon submission template** for the IBM BoB AI Innovation Hackathon. The project is called **TrialGuard** — a Python/Streamlit/watsonx.ai application. Critically: **all `src/` module `__init__.py` files are empty stubs**, `requirements.txt` doesn't exist yet, no actual Python source code beyond stubs is present, and `docs/setup-guide.md` and `docs/architecture.md` still contain unfilled template placeholders.

### Non-obvious things discovered

1. **`requirements.txt` does not exist** — README says `pip install -r requirements.txt` but the file is not committed. It needs to be created at the project root.
2. **`.env.example` lives inside `src/`**, not the project root. The copy command in README (`cp .env.example .env`) is wrong — the correct path is `cp src/.env.example .env` (or `.env` should be placed at root and read from there).
3. **watsonx.ai URL default** is `https://us-south.ml.cloud.ibm.com` (specified in `src/.env.example`). The required env vars are `WATSONX_API_KEY`, `WATSONX_PROJECT_ID`, and `WATSONX_URL`.
4. **GitHub Actions CI** (`validate.yml`) runs on every push to **any branch** and checks: required files present, `submission.yaml` valid YAML with all fields, `src/` has ≥1 non-README/non-.env file, `demo/demo-video-link.txt` is not the placeholder, README has no placeholder text. **CI will fail** until real source code is in `src/`.
5. **`team.track` in `submission.yaml`** must be exactly one of: `AI`, `DevOps`, `Sustainability`, or `Open` — the CI validates this with regex.
6. **`docs/architecture.md` and `docs/setup-guide.md`** are still template stubs with placeholder `[bracketed]` content — they need to be filled in before submission.
7. **`bob_sessions/` directory is empty** — Bob session exports must be added here for judging.
8. **No `pytest.ini`, `setup.cfg`, or `pyproject.toml`** exists — the test runner (`pytest tests/ -v`) will work but there's no configuration for coverage, markers, or paths.
9. **`demo/screenshots/` directory exists but is empty** — at least 3 screenshots named `01-*.png`, `02-*.png`, etc. are required.
10. **The entry point** per README is `streamlit run src/app/dashboard.py` — but `src/app/dashboard.py` does not exist yet.

---

Here is the exact content to put in `AGENTS.md` at the project root (`bob-ai-hackathon--Your-Team-Name-/AGENTS.md`):

```markdown
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
```

Switch to **Agent mode** and I can write all of this for you.

---

### 👤 User

Yes, please write the AGENTS.md file at the project root with the exact content you proposed above. Just create the file — do not make any other changes to the repo.

---

### 🤖 Assistant

> 🔧 called: write_file



> 🔧 **write_file** — bob-ai-hackathon--Your-Team-Name-/AGENTS.md

### 🤖 Assistant

[`AGENTS.md`](bob-ai-hackathon--Your-Team-Name-/AGENTS.md) created at the project root. No other files were touched.