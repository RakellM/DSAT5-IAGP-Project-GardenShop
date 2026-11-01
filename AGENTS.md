# AGENTS.md: Instructions for AI Agents & Developers

## 1. Purpose
This document defines the rules, environment setup, testing procedures, and data governance practices that AI agents and human developers must follow when analyzing, implementing, testing, and documenting software in the `exercise/Task_02/` directory of this repository.

---

## 2. Reference Hierarchy
Before modifying code or executing commands:
1. **Read `AGENTS.md`** (this document) to understand development conventions, execution safety, and reference commands.
2. **Read `PRD.md`** ([`./PRD.md`](./PRD.md)) to understand the business problem, user stories, objectives, and product scope.
3. **Read `SPEC.md`** ([`./SPEC.md`](./SPEC.md)) to identify technical requirements, data contracts, formulas, and acceptance criteria.
4. **Consult Data Dictionary** ([`../Task02-Data_Dictionary.md`](../Task02-Data_Dictionary.md)) for exact table definitions, data types, and nullability rules.

### Conflict Resolution
- If an implementation detail conflicts with `SPEC.md`, update or clarify the specification before writing code.
- Never invent business rules or change metric definitions without explicit documentation in `PRD.md` and `SPEC.md`.
- Explicit constraints in instructions (e.g., directory write restrictions) take absolute precedence.

---

## 3. Work Process

### Stage 1: Understanding & Data Governance
- Inspect `data/garden_shop.db` in read-only mode.
- Respect `.gitignore`: never attempt to un-ignore or commit raw files from `data/`.
- Understand the core business constraints: Order #17 cancellation, Product #24 discontinuation, and Cartesian join balance deduplication.

### Stage 2: Planning & Test-Driven Development (TDD)
- Define test assertions in `tests/test_indicators.py` based on `SPEC.md` requirements before modifying application logic.
- Plan minimal, cohesive modules with single responsibilities (`data_loader.py` for queries, `app.py` for UI).

### Stage 3: Implementation
- Implement logic strictly within `./exercise/Task_02/`.
- Maintain clean Python formatting and explicit error handling.
- Avoid premature abstractions or complex external dependencies.

### Stage 4: Verification
- Execute automated tests (`pytest` or `python -m unittest`).
- Verify that all test cases (TEST-001 through TEST-007) pass with 100% success.
- Test the application locally and capture a legible screenshot (`dashboard_screenshot.png`).

### Stage 5: Documentation & Delivery
- Keep `PRD.md`, `SPEC.md`, and `AGENTS.md` updated and synchronized with the actual codebase.

---

## 4. Development & Data Care Rules

### 4.1. Code Quality
- Modular separation: keep data access (`data_loader.py`) decoupled from presentation (`app.py`).
- Explicit SQL queries: use Common Table Expressions (CTEs) to pre-aggregate sales before joining to product tables to prevent balance inflation.
- Explicit null handling: replace null contact emails with `"[NO EMAIL ON FILE]"` and null coupon codes gracefully.

### 4.2. Directory & Scope Restrictions
- **CRITICAL RESTRICTION:** All development, testing scripts, and generated assets must reside strictly within `./exercise/Task_02/`.
- Never modify files in `./data/`, `./sql/`, or parent project directories without explicit authorization.

### 4.3. Dependency Management
- Use the existing Python environment (Python 3.10+ with `pandas`, `streamlit`, `plotly`).
- Never run global `pip install` commands.

---

## 5. Project-Specific Standards

- **Primary Language:** Python 3.10+
- **Database Engine:** SQLite 3 (`data/garden_shop.db`)
- **Web Dashboard Framework:** Streamlit (Python) and HTML5/Tailwind/Chart.js (Static SPA)
- **Visualization Libraries:** Plotly Express / Plotly Graph Objects (in Streamlit) and Chart.js (in HTML5)
- **Test Framework:** Python standard library `unittest` / `pytest`
- **Directory Layout:**
  ```
  exercise/Task_02/
  ├── PRD.md                 # Product Requirements Document
  ├── SPEC.md                # Software Specification
  ├── AGENTS.md              # Agent & Developer Instructions
  ├── data_loader.py         # Data Access & Metric Engine
  ├── app.py                 # Streamlit Interactive Dashboard
  ├── index.html             # Standalone Web Dashboard (GitHub Pages)
  ├── dashboard_data.json    # Pre-processed Data Payload
  ├── tests/
  │   ├── __init__.py
  │   └── test_indicators.py # Automated Test Suite
  └── dashboard_screenshot.png # Verification Screenshot
  ```

---

## 6. Reference Commands

| Purpose | Command | Notes |
|---|---|---|
| **Run Unit Tests** | `python -m unittest discover -s exercise/Task_02/tests -p "test_*.py"` | Executes TDD indicator test suite |
| **Run Streamlit Dashboard** | `streamlit run exercise/Task_02/app.py` | Launches local dashboard on `http://localhost:8501` |
| **Extract JSON Data** | `python exercise/Task_02/data_loader.py` | Refreshes `dashboard_data.json` for web app |
| **Run Static Web Server** | `python -m http.server 8000` | Serves `exercise/Task_02/index.html` locally |

---

## 7. Quality Criteria

A change is certified when:
1. **Indicator Accuracy:** `Inventory Health Index` equals 78.3% and `Capital Needed to ROP` equals $152.00 on baseline data.
2. **Business Rule Compliance:** Order #17 (cancelled) is excluded; Product #24 (discontinued) has 0 reorder recommendation.
3. **Non-Duplication:** Active stock cost equals $4,731.00 (not duplicated across order lines).
4. **Test Suite:** All unit tests in `tests/test_indicators.py` execute and pass.
5. **Documentation Alignment:** `PRD.md`, `SPEC.md`, and `AGENTS.md` accurately describe the running system.

---

## 8. Delivery Format
Upon completion, the deliverables provided in `./exercise/Task_02/` are:
- `PRD.md` (Product Requirements Document)
- `SPEC.md` (Software Specification)
- `AGENTS.md` (Instructions for AI Agents & Developers)
- `data_loader.py` (Data Access Layer)
- `app.py` (Streamlit Application)
- `index.html` (Standalone Web App for GitHub Pages)
- `tests/test_indicators.py` (Unit Tests)
- `dashboard_screenshot.png` (Verification Screenshot)
