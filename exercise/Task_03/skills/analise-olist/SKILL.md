---
name: analise-olist
description: "Answers analytical questions on the Olist e-commerce database (orders, customer states, average ticket) by executing verified Python code and presenting reproducible results."
---

# analise-olist

Analytics copilot skill for investigating orders, customer distribution, and item ticket economics on the Brazilian Olist marketplace database.

## 1. Task and expected result

Perform data investigations over the Olist CSV database for product, marketing, and marketplace operations teams, producing verified calculations and explanations.

- **Objective:** Answer natural-language business questions regarding sales volume, geographical concentration, and ticket metrics with reproducible code execution.
- **Included:**
  - Count of delivered orders grouped by month (`dtPedido`).
  - Top 5 customer states (UF) by delivered order count.
  - Average ticket of item prices per delivered order (excluding freight) with coverage explanation.
  - Dynamic follow-up filtering (date range restrictions, customer UF filtering).
  - Explicit handling of empty periods and queries outside database scope.
- **Out of scope:**
  - Database schema modifications or editing source CSV files.
  - Predictive machine learning or forecasting.
  - Speculating on external attributes not present in Olist tables.

## 2. When to use

Use this skill when:
- The user asks questions about Olist orders, sales trends, customer distribution by state (UF), or item spending.
- The user requests follow-up adjustments to an existing query (e.g., "now restrict that to SP in 2017").
- Verifiable numbers backed by code execution against the Olist CSV files are required.

Do not use this skill for general non-Olist questions, modifying database schemas, or tasks involving unrelated databases.

## 3. Inputs

| Input | Format or source | Required | How to use or validate |
| --- | --- | --- | --- |
| Natural language question | User text prompt | Yes | Parse intent (monthly volume, top UFs, average ticket, or custom filter). |
| Data directory | File path (`data/olist/`) | Yes | Defaults to `data/olist/`. Verify directory contains `pedido.csv`, `cliente.csv`, `item_pedido.csv`. |
| Date range filter | Text `YYYY-MM-DD` | No | Optional start/end date filter applied to `dtPedido`. |
| State (UF) filter | Two-letter code (e.g. `SP`) | No | Optional filter matched against `cliente.descUF`. |

When an input parameter is ambiguous (e.g. date format or whether cancelled orders should be counted), apply standard defaults (`descSituacao == 'delivered'`, reference date `dtPedido`) and explicitly declare the convention used.

## 4. Output

- **Deliverable:** Clear, structured analytical answer in chat answering the user's question.
- **Format:** Formatted markdown tables, KPI summaries, and explicit statements of filters applied.
- **Evidence:** Always cite the executed command or script path (`scripts/analyze.py`), the files queried, and the raw metric values.
- **Convention:**
  - Monetary values formatted in Brazilian Reais (`R$ #,##0.00`).
  - Order counts formatted with thousand separators (`#,##0`).
  - Empty periods return count `0` and average ticket `N/A`.

## 5. Task-specific rules

1. **Delivered Status Criterion:** Standard performance analysis applies strictly to delivered orders (`descSituacao == 'delivered'`) unless explicitly instructed otherwise.
2. **Reference Date:** Use `dtPedido` (order placement date) as the standard chronological anchor.
3. **Cartesian Join Prevention:** Never multiply order lines when combining `item_pedido.csv` and `pagamento_pedido.csv`. Aggregate at the order level first.
4. **Average Ticket Formula:** Sum of item prices `vlPreco` for delivered orders divided by the count of distinct delivered orders. Freight `vlFrete` is explicitly excluded.
5. **No Hardcoded Numbers:** Never state a metric value from memory or prior conversation without running the query script or code.

For complete mathematical definitions and relational structures, consult:
- [business_rules.md](references/business_rules.md)
- [schema_guide.md](references/schema_guide.md)

## 6. Procedure

### Understand the request
1. Identify the metric requested (monthly orders, state ranking, average ticket, or multi-metric).
2. Extract any temporal boundaries (`start_date`, `end_date`) or geographical filters (`UF`).
3. If the question cannot be answered by Olist tables (e.g. customer age, competitor prices), state that the database cannot answer the question and explain what fields exist.

### Perform the task
4. Execute the reusable script with appropriate flags:
   ```bash
   python exercise/Task_03/skills/analise-olist/scripts/analyze.py --data-dir data/olist --query [monthly_orders|top_ufs|average_ticket|all] [--start-date YYYY-MM-DD] [--end-date YYYY-MM-DD] [--uf UF]
   ```
5. Inspect the JSON output returned by the engine.

### Check the result
6. Verify that delivered order count matches expected boundaries (e.g. maximum 96,478 for entire database).
7. If order count is 0, verify that average ticket is presented as "Not Applicable (N/A)" and total is 0.
8. If a script execution error occurs, verify file paths and permissions before responding.

### Deliver
9. Present the metric results in a clean table or bullet points.
10. State:
    - The metric name and formula.
    - Files queried (`pedido.csv`, `cliente.csv`, `item_pedido.csv`).
    - Filters applied (date range, UF, status).
    - Code command executed.

## 7. Supporting resources

- **References:**
  - [business_rules.md](references/business_rules.md) — Consult for metric formulas, freight exclusions, and coverage handling.
  - [schema_guide.md](references/schema_guide.md) — Consult for table joins and primary/foreign keys.
- **Scripts:**
  - [analyze.py](scripts/analyze.py) — Reusable analytics engine accepting `--query`, `--data-dir`, `--start-date`, `--end-date`, `--uf`.
- **Tests:**
  - [test_analysis.py](tests/test_analysis.py) — Unit tests validating metrics, subset calculations, and edge cases.

## 8. Environment and tools

- **Required tools:** Terminal/CLI with Python 3.10+.
- **Dependencies:** Standard Python libraries (`csv`, `collections`, `json`, `argparse`, `unittest`). No external packages required.
- **Execution Command:**
  ```bash
  python exercise/Task_03/skills/analise-olist/scripts/analyze.py --data-dir data/olist --query all
  ```

## 9. Scope limits

- **Preserve:** All source CSV files in `data/olist/` must remain unchanged and read-only.
- **Expected changes:** New analysis scripts or tests stored within `exercise/Task_03/`.

## 10. Completion criteria

Consider the task complete when:
- The question is answered using values directly computed from Olist data files.
- The command and executed script path are shown or cited.
- Follow-up filter changes re-run the code and display updated figures.
- Empty period and out-of-scope boundaries are handled without exceptions.
- Unit test suite in `tests/test_analysis.py` passes 100%.

## 11. Usage examples

### Relevant request
> "How many delivered orders were placed in each month?"

**Execution:**
```bash
python exercise/Task_03/skills/analise-olist/scripts/analyze.py --data-dir data/olist --query monthly_orders
```
**Expected result:** Chronological list of months from 2016-09 to 2018-08 with order counts (e.g., 2017-11: 7,289 orders).

---

### Follow-up request
> "Now restrict the analysis to the state of SP during 2017."

**Execution:**
```bash
python exercise/Task_03/skills/analise-olist/scripts/analyze.py --data-dir data/olist --query all --start-date 2017-01-01 --end-date 2017-12-31 --uf SP
```
**Expected result:** 17,071 delivered orders, average ticket R$ 125.14, and monthly breakdown for 2017 in SP.

---

### Missing data / Empty period
> "What was the average ticket in January 2025?"

**Execution:**
```bash
python exercise/Task_03/skills/analise-olist/scripts/analyze.py --data-dir data/olist --query average_ticket --start-date 2025-01-01 --end-date 2025-01-31
```
**Expected result:** 0 delivered orders found; Average Ticket reported as `Not Applicable (N/A)`.

---

### Out-of-scope request
> "What is the average age of customers who bought smartphones?"

**Expected behavior:** The skill recognizes that customer demographic age is not recorded in the Olist schema (`cliente.csv` contains only location data like city, state, zip code). The agent explains that this question cannot be answered from the available data.
