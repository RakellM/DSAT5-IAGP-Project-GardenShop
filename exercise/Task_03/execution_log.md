# Task 03 — Execution Log & Verification Evidence

This report records the live execution outputs for all required analyses specified in `exercise/Task03.md`, using the newly created skill `analise-olist`.

---

## 1. Automated Test Suite Execution

Command:
```bash
python -m unittest discover -s exercise/Task_03/skills/analise-olist/tests -p "test_*.py"
```

Output:
```
.....
----------------------------------------------------------------------
Ran 5 tests in 1.526s

OK
```

All 5 verification tests passed:
- `test_01_total_delivered_orders`: Matches baseline 96,478 delivered orders.
- `test_02_top_5_ufs`: Correctly orders states: SP (40,501), RJ (12,350), MG (11,354), RS (5,345), PR (4,923).
- `test_03_average_ticket`: Validates R$ 137.04 average ticket on R$ 13,221,498.11 item revenue with 100% item coverage.
- `test_04_empty_period_behavior`: Gracefully handles future period (2025) with 0 orders and N/A average ticket.
- `test_05_follow_up_filtering_2017_sp`: Validates dynamic filtering for SP in 2017 (17,071 orders, R$ 125.14 average ticket).

---

## 2. Core Question 1: Monthly Delivered Orders

Command:
```bash
python exercise/Task_03/skills/analise-olist/scripts/analyze.py --data-dir data/olist --query monthly_orders --format text
```

Output:
| Month | Delivered Orders |
|---|---|
| 2016-09 | 1 |
| 2016-10 | 265 |
| 2016-12 | 1 |
| 2017-01 | 750 |
| 2017-02 | 1,653 |
| 2017-03 | 2,546 |
| 2017-04 | 2,303 |
| 2017-05 | 3,546 |
| 2017-06 | 3,135 |
| 2017-07 | 3,872 |
| 2017-08 | 4,193 |
| 2017-09 | 4,150 |
| 2017-10 | 4,478 |
| 2017-11 | 7,289 |
| 2017-12 | 5,513 |
| 2018-01 | 7,069 |
| 2018-02 | 6,555 |
| 2018-03 | 7,003 |
| 2018-04 | 6,798 |
| 2018-05 | 6,749 |
| 2018-06 | 6,099 |
| 2018-07 | 6,159 |
| 2018-08 | 6,351 |

**Total:** 96,478 delivered orders.

---

## 3. Core Question 2: Top 5 Customer States (UF)

Command:
```bash
python exercise/Task_03/skills/analise-olist/scripts/analyze.py --data-dir data/olist --query top_ufs --top-n 5 --format text
```

Output:
| Rank | State (UF) | Delivered Orders | % of Total Orders |
|---|---|---|---|
| #1 | SP | 40,501 | 41.98% |
| #2 | RJ | 12,350 | 12.80% |
| #3 | MG | 11,354 | 11.77% |
| #4 | RS | 5,345 | 5.54% |
| #5 | PR | 4,923 | 5.10% |

---

## 4. Core Question 3: Average Ticket per Delivered Order

Command:
```bash
python exercise/Task_03/skills/analise-olist/scripts/analyze.py --data-dir data/olist --query average_ticket --format text
```

Output:
- **Average Ticket:** R$ 137.04
- **Total Item Revenue:** R$ 13,221,498.11
- **Delivered Orders in Scope:** 96,478
- **Delivered Orders with Items:** 96,478 (Coverage: 100.0%)
- **Note:** Freight costs (`vlFrete`) are excluded as required by business rules.

---

## 5. Follow-Up Analysis: Restrict to SP in 2017

Command:
```bash
python exercise/Task_03/skills/analise-olist/scripts/analyze.py --data-dir data/olist --query all --start-date 2017-01-01 --end-date 2017-12-31 --uf SP --format text
```

Output:
- **Delivered Orders:** 17,071
- **Average Ticket (SP 2017):** R$ 125.14
- **Total Item Revenue:** R$ 2,136,258.96
- **Peak Month:** 2017-11 (2,899 orders)

---

## 6. Edge Case Validations

### 6.1 Period with No Data (January 2025)
Command:
```bash
python exercise/Task_03/skills/analise-olist/scripts/analyze.py --data-dir data/olist --query all --start-date 2025-01-01 --end-date 2025-01-31
```
Output:
- Delivered orders in scope: 0
- Average Ticket: `Not Applicable (N/A)`

### 6.2 Question Not Answerable by Database
- *Question:* "What is the average customer age?"
- *Agent behavior:* Identifies that `cliente.csv` contains only location attributes (`idCliente`, `idClienteUnico`, `descCidade`, `descUF`, `descCEP`) and no demographic age information. Accurately explains why the query cannot be answered.
