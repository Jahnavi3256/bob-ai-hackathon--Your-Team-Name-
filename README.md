# TrialGuard — Real-Time Clinical Trial Protocol Deviation Monitor

Hybrid rule + AI system that detects clinical trial protocol deviations in real time, classifies them per ICH E6(R2) GCP standards using IBM watsonx.ai Granite, scores each site''s risk, and auto-drafts CAPA (Corrective and Preventive Action) reports.

Built for the **IBM BoB AI Innovation Hackathon 2026**.

---

## Team

**Team Name:** TrialGuard
**Track:** AI
**Lead:** Palak Dave (23ce018@charusat.edu.in)

**Members:**
- Palak Dave (23ce018)
- Darshika Dudhat (23ce027)
- Jahnavi Patel (23ce095)
- Riya Jagani (23ce044)

---

## Problem Statement

Clinical trials generate thousands of protocol deviations across hundreds of sites — missed visits, wrong doses, prohibited concomitant medications, late safety reports. Most go undetected until FDA audit, where a single rejected submission delays drug approval by 6–12 months and costs USD 50–100M. Current tools rely on manual monitoring visits every 4–8 weeks and Excel-based deviation logs that no one aggregates in real time.

See [`docs/problem-statement.md`](docs/problem-statement.md) for the full analysis.

---

## Solution

TrialGuard ingests patient visit, screening, and medication records, then:

1. **Detects deviations** using a rule engine against a machine-readable protocol specification (visit timing, dosing, prohibited meds, required labs).
2. **Classifies severity** as Major / Minor / Administrative per ICH E6(R2) using IBM watsonx.ai Granite with few-shot prompting.
3. **Scores site risk** using a composite of leading indicators, banded Red / Amber / Green.
4. **Auto-drafts CAPA reports** (Problem, Corrective Action, Preventive Action, Priority) using watsonx.ai.
5. **Presents everything** in a Streamlit dashboard with a site risk heatmap and drill-down to individual deviations.

Hybrid architecture (deterministic rules + generative AI) is deliberately defensible under FDA scrutiny — pure-LLM systems are not audit-ready.

See [`docs/solution-overview.md`](docs/solution-overview.md) and [`docs/architecture.md`](docs/architecture.md) for details.

---

## Key Features

- Rule-based deviation detection across visit timing, dosing, prohibited medications, and required labs
- ICH E6(R2) severity classification via IBM watsonx.ai Granite
- Site-level composite risk scoring with Red/Amber/Green banding
- Auto-generated CAPA reports
- Streamlit dashboard with site heatmap and deviation drill-down
- Rule engine validated against ground-truth deviation labels with precision/recall metrics

---

## Tech Stack

- **Language:** Python 3.10+
- **Frameworks:** Streamlit, Pandas, Pytest
- **IBM Technologies:** IBM Bob (AI development partner), IBM watsonx.ai (Granite foundation model)
- **Data:** Synthetic clinical trial dataset (500 patients, 10 sites, 4-visit protocol TG-101)
- **CI:** GitHub Actions

---

## How to Run

See [`docs/setup-guide.md`](docs/setup-guide.md) for the full step-by-step. Short version:

```bash
git clone https://github.com/YOUR-USERNAME/bob-ai-hackathon--Your-Team-Name-.git
cd bob-ai-hackathon--Your-Team-Name-
pip install -r requirements.txt
cp .env.example .env    # then edit .env to add your watsonx.ai credentials
streamlit run src/app/dashboard.py
```

---

## Demo

- **Video walkthrough:** see [`demo/demo-video-link.txt`](demo/demo-video-link.txt)
- **Screenshots:** [`demo/screenshots/`](demo/screenshots/)
- **Live deployment:** not deployed — runs locally via Streamlit

---

## IBM Bob Integration

IBM Bob was used across every phase of development, not just as a code autocompleter:

- **Plan mode** — designed the system architecture and rule engine structure
- **Code mode** — wrote the deviation detection rules, watsonx.ai integration, site risk scoring, CAPA generator, and Streamlit dashboard
- **Ask mode** — generated the AGENTS.md repo context file and answered ICH E6(R2) domain questions
- **`/review`** — final code review pass before submission
- **Custom mode** — created a "GCP-Auditor" mode that reviews outputs against ICH E6 principles

All Bob task session exports are in [`bob_sessions/`](bob_sessions/) for judging.

---

## Known Limitations

Built on synthetic data (not real clinical trial data). Rule coverage focuses on the four most common deviation categories; a production system would need broader rules (unscheduled visits, dose escalation logic, adverse event reporting timelines, informed consent tracking). Runs locally via Streamlit; not deployed.

---

## What We''re Most Proud Of

The hybrid deterministic rule engine + watsonx.ai Granite classification layer, validated against ground-truth deviation labels with real precision and recall metrics. This is defensible under FDA scrutiny in a way pure-LLM approaches are not — and it was built end-to-end in under a day using IBM Bob across planning, coding, testing, and documentation.

---

## Repository Structure

.
├── submission.yaml # Hackathon metadata (evaluated first)
├── README.md # This file
├── AGENTS.md # Bob-generated repo context
├── src/
│ ├── data/ # Synthetic clinical trial dataset
│ ├── rules/ # Rule-based deviation detection
│ ├── classifier/ # watsonx.ai severity classifier
│ ├── scoring/ # Site risk scoring
│ ├── capa/ # CAPA report generator
│ └── app/ # Streamlit dashboard
├── tests/ # Pytest suite
├── docs/ # Problem, solution, architecture, setup
├── demo/ # Video link, screenshots
├── presentation/ # Slide deck
└── bob_sessions/ # Exported Bob task histories (per member)
