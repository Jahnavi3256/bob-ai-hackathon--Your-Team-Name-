# Design the complete system architecture for TrialGuard, our clinical trial protocol deviation monitoring system.

Read these files first for context:
- @AGENTS.md
- @README.md
- @src/data/DATASET_README.md
- @src/data/trialguard_protocol_rules.csv
- @src/data/trialguard_data_dictionary.csv

Then produce a file at `docs/architecture.md` containing the following sections in this exact order:

## 1. Overview
Two paragraphs. What the system does end-to-end, and the core design decision (hybrid deterministic rule engine + LLM classification, and why this is defensible under FDA scrutiny in a way pure-LLM is not).

## 2. Architecture Diagram
A Mermaid `graph TD` diagram showing every component and how data flows between them. Include:
- Input CSV files as source nodes (patient_screening, visit_records, protocol_rules)
- Data loader module
- Rule-based deviation detector (with its 4 checks named: visit timing, dose, prohibited medication, missing lab)
- watsonx.ai severity classifier
- Site risk scoring engine
- watsonx.ai CAPA generator
- Streamlit dashboard as the final output surface
- Ground-truth comparison branch for validation metrics
Use meaningful edge labels (e.g., "deviations", "classified deviations", "site scores").

## 3. Component Table
A markdown table with columns: Component | File Path | Responsibility | Depends On | Technology
List all components: data loader, each rule check, severity classifier, risk scorer, CAPA generator, dashboard, validation harness.

## 4. Data Flow
A numbered step-by-step walkthrough of what happens from CSV load to dashboard render. 8-12 numbered steps.

## 5. Protocol TG-101 Rules (extracted from data)
Summarize the rules from trialguard_protocol_rules.csv:
- Eligibility criteria
- Visit schedule with windows
- Dose specification
- Prohibited medications
- Required labs at each visit
- Severity classification rules

## 6. ICH E6(R2) Severity Mapping
A table showing how each deviation type maps to Major / Minor / Administrative per the ICH E6(R2) GCP standard AND per the protocol's own classification rules. Reference the protocol rules for consistency.

## 7. Site Risk Scoring Formula
The exact formula for computing site risk: Risk = ((5 × Major) + (2 × Minor) + (1 × Administrative)) / completed_visits × 100, capped at 100. Bands: Low <25, Medium 25-49.9, High 50-74.9, Critical ≥75. Explain why majors are weighted 5x.

## 8. Validation Strategy
Explain that the synthetic dataset comes with ground-truth Deviation_Severity labels, so we can compute precision and recall for our rule engine — a hackathon-differentiating feature.

## 9. Assumptions and Simplifications
Bullet list of scope choices: single trial (TG-101), synthetic data, no real PHI, no deployment, local Streamlit only.

Do not write any code. Do not modify any other file. Only create docs/architecture.md.

---

**Status:** active  **Date:** 2026-09-15

---

### 👤 User

Design the complete system architecture for TrialGuard, our clinical trial protocol deviation monitoring system.

Read these files first for context:
- @AGENTS.md
- @README.md
- @src/data/DATASET_README.md
- @src/data/trialguard_protocol_rules.csv
- @src/data/trialguard_data_dictionary.csv

Then produce a file at `docs/architecture.md` containing the following sections in this exact order:

## 1. Overview
Two paragraphs. What the system does end-to-end, and the core design decision (hybrid deterministic rule engine + LLM classification, and why this is defensible under FDA scrutiny in a way pure-LLM is not).

## 2. Architecture Diagram
A Mermaid `graph TD` diagram showing every component and how data flows between them. Include:
- Input CSV files as source nodes (patient_screening, visit_records, protocol_rules)
- Data loader module
- Rule-based deviation detector (with its 4 checks named: visit timing, dose, prohibited medication, missing lab)
- watsonx.ai severity classifier
- Site risk scoring engine
- watsonx.ai CAPA generator
- Streamlit dashboard as the final output surface
- Ground-truth comparison branch for validation metrics
Use meaningful edge labels (e.g., "deviations", "classified deviations", "site scores").

## 3. Component Table
A markdown table with columns: Component | File Path | Responsibility | Depends On | Technology
List all components: data loader, each rule check, severity classifier, risk scorer, CAPA generator, dashboard, validation harness.

## 4. Data Flow
A numbered step-by-step walkthrough of what happens from CSV load to dashboard render. 8-12 numbered steps.

## 5. Protocol TG-101 Rules (extracted from data)
Summarize the rules from trialguard_protocol_rules.csv:
- Eligibility criteria
- Visit schedule with windows
- Dose specification
- Prohibited medications
- Required labs at each visit
- Severity classification rules

## 6. ICH E6(R2) Severity Mapping
A table showing how each deviation type maps to Major / Minor / Administrative per the ICH E6(R2) GCP standard AND per the protocol's own classification rules. Reference the protocol rules for consistency.

## 7. Site Risk Scoring Formula
The exact formula for computing site risk: Risk = ((5 × Major) + (2 × Minor) + (1 × Administrative)) / completed_visits × 100, capped at 100. Bands: Low <25, Medium 25-49.9, High 50-74.9, Critical ≥75. Explain why majors are weighted 5x.

## 8. Validation Strategy
Explain that the synthetic dataset comes with ground-truth Deviation_Severity labels, so we can compute precision and recall for our rule engine — a hackathon-differentiating feature.

## 9. Assumptions and Simplifications
Bullet list of scope choices: single trial (TG-101), synthetic data, no real PHI, no deployment, local Streamlit only.

Do not write any code. Do not modify any other file. Only create docs/architecture.md.

---

### 🤖 Assistant

> 🔧 called: use_skill



> 🔧 **use_skill** — create-plan

### 🤖 Assistant

> 🔧 called: read_file, read_file

The requirements here are very clear and complete — the user has specified exact sections, content for each, and explicit source files to read. I'll go directly to reading all the referenced files in parallel before writing the architecture document.

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/AGENTS.md

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/README.md

### 🤖 Assistant

> 🔧 called: read_file, read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/data/DATASET_README.md

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/data/trialguard_protocol_rules.csv

### 🤖 Assistant

> 🔧 called: read_file



> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/src/data/trialguard_data_dictionary.csv

### 🤖 Assistant

> 🔧 called: read_file

All source files have been read. I now have everything needed to write a fully grounded architecture document. Let me also check the existing `docs/architecture.md` template to understand what's already there.

> 🔧 **read_file** — bob-ai-hackathon--Your-Team-Name-/docs/architecture.md

### 🤖 Assistant

> 🔧 called: write_file

Now I have full context. I'll write the complete `docs/architecture.md` file grounded entirely in the data from the source files.

> 🔧 **write_file** — bob-ai-hackathon--Your-Team-Name-/docs/architecture.md

### 🤖 Assistant

[`docs/architecture.md`](bob-ai-hackathon--Your-Team-Name-/docs/architecture.md) has been written in full. Here is a summary of every section and the grounding for each decision:

---

### What was produced

**§1 Overview** — Two paragraphs explaining end-to-end flow (CSV → rule engine → watsonx.ai classifier → risk scorer → CAPA → dashboard) and the core design argument: the hybrid deterministic + LLM architecture is FDA-defensible because every detected deviation traces to a numbered row in `trialguard_protocol_rules.csv`, and the LLM is used only downstream of that fixed detection step.

**§2 Architecture Diagram** — A `graph TD` Mermaid diagram with all three CSV source nodes, the Data Loader, all four named rule checks (Visit Timing, Dose, Prohibited Medication, Missing Lab), the Deviation Aggregator, the watsonx.ai Severity Classifier, Site Risk Scoring Engine, watsonx.ai CAPA Generator, Streamlit Dashboard, and the ground-truth → Validation Harness → Dashboard branch. Every edge is labelled (e.g. `deviations`, `classified deviations`, `site scores`, `precision and recall metrics`).

**§3 Component Table** — 11 rows covering every logical component with file paths derived from the `src/` directory structure in `README.md`, responsibilities grounded in the data dictionary columns, dependency chains, and technology stack.

**§4 Data Flow** — 12 numbered steps from CSV load through protocol rule parsing, each of the four rule checks (referencing actual column names like `Actual_Day_From_Enrollment`, `Prohibited_Drug_X`, `CBC_Completed`), aggregation, Granite classification, risk scoring, CAPA generation, validation, and dashboard render.

**§5 Protocol TG-101 Rules** — All content extracted verbatim from `trialguard_protocol_rules.csv`: eligibility (age 18–65, Diabetes/Hypertension), visit schedule table (V1 Day 0 ±1, V2 Day 14 ±3, V3 Day 28 ±3, V4 Day 56 ±5), dose (100 mg), prohibited medication (Drug X), required labs (CBC and Chemistry Panel at V2 and V4), and the three severity classification rules exactly as written in the CSV.

**§6 ICH E6(R2) Severity Mapping** — Six-row table mapping Wrong Dose, Prohibited Medication, Visit >7 days, Visit ≤7 days outside window, Missing Lab, and Documentation Deviation to ICH E6(R2) tier with regulatory clause references (§4.5, §5.18.3, §8.3, §4.9) and confirmation of alignment with TG-101 rules.

**§7 Site Risk Scoring Formula** — The exact formula from `DATASET_README.md`, the four bands with colour coding, and an explanation of why Majors are 5× (direct safety/endpoint impact that triggers regulatory rejection) vs. Minor 2× vs. Administrative 1×, plus the per-visit normalization rationale.

**§8 Validation Strategy** — Explains the ground-truth `Deviation_Severity` column in `trialguard_visit_records.csv`, the composite key alignment strategy, the precision/recall/F1 metrics per tier, and why this is differentiating in a hackathon context. Cites the actual dataset counts (628 visits, 26 deviations: 20 Major, 5 Minor, 1 Administrative).

**§9 Assumptions and Simplifications** — Eight bullets covering single trial scope, synthetic data, no PHI, no deployment, local Streamlit only, four deviation categories, watsonx.ai call volume, and the architectural constraint that the LLM never independently detects deviations.