# Brainstorm: Garden Shop Inventory & Restocking Dashboard

> Project-specific brainstorm.
> Purpose: give another person or agent session enough context to adapt `PRD.md`, `SPEC.md`, `AGENTS.md` and `CLAUDE.md` to this project, without implementing anything yet.

## How to use

Provide this file together with the four templates (`PRD.md`, `SPEC.md`, `AGENTS.md`, `CLAUDE.md`) and, if available, `data/garden_shop.db`.

Suggested request:

> Read brainstorming_garden_shop_dashboard.md and the four templates. Review the items marked **Pending** with me (2 to 4 questions per round), then adapt the four documents to this project. Do not implement the solution yet.

### Status legend

| Label | Meaning |
|---|---|
| **Confirmed** | Stated as a requirement or business rule in the proposal |
| **Proposed** | Suggestion from the proposal that the owner has not explicitly approved |
| **Hypothesis** | Interpretation not verifiable from the materials provided |
| **Pending** | Needs an answer before the related document section can be closed |

### Sources and their limits

- Read: the proposal (`.docx`) and the template (`brainstorming.md`).
- **Not available:** `data/garden_shop.db`, the data dictionary, any repository or code. Every number below comes from the proposal and has **not** been re-checked against the database. Table and field names are inferred from the SQL written in the proposal and must be confirmed against the real schema.
- The four document templates were not provided in this session either; they are needed for the adaptation step.

---

## 1. Problem, users and objective

**Problem (Confirmed).** An online shop selling gardening supplies, houseplants, seeds and outdoor tools has no clear view of which products need replenishment, whether stock is adequate for how fast items sell, or which supplier orders to place. The proposal states that the main failure is lack of visibility and timely purchase orders, not lack of capital.

**Concrete example (from the proposal).** Hanging Basket (#14) has 0 units in stock against a reorder level of 10. Pothos 'Golden' and Tomato Seeds 'Roma' are among the best sellers and are already below their reorder levels. Ironwood Tools supplies a product that needs restocking but has no email on file.

**Users (Confirmed):** executive leadership, operations director, warehouse and merchandising managers.

**Decisions the users need to make (Confirmed, from the 7 management questions):**
1. Which products are below the recommended reorder level?
2. Which have zero or critically low stock?
3. Which high-volume sellers need availability protection?
4. Which categories concentrate restock needs?
5. What is the value of available stock at cost?
6. Which products need priority monitoring?
7. Which suppliers are linked to products that need restock?

**Objective of the first delivery (Proposed):** an interactive dashboard that answers the 7 questions from the database, classifies products by restock priority, and shows what to order from each supplier and at what cost.

**How we will know it helped (Pending).** The proposal lists KPI targets, but no one has confirmed them as success measures (see section 6).

---

## 2. Scope

### Included in the first version (Proposed)
- KPI cards (inventory health, stockouts, SKUs below reorder level, replenishment capital, stock value at cost, retail value, margin, revenue at risk, discontinued capital).
- Category health chart, stock-versus-sales priority matrix, supplier capital chart.
- Restock action workbench (table of products to reorder, by priority).
- Clearance drawer for discontinued products.
- Filters: category, supplier, stock health, discontinued toggle.
- Alert for suppliers without a contact email.
- Semantic SQL views feeding the dashboard.

### Left for later (record outside the current scope)
- One-click purchase order email drafts (proposal week 5).
- Audit log of daily inventory snapshots (to enable stock history).
- Physical attributes and perishability (proposal "phase 2 WMS expansion").

### Explicitly rejected or deferred (Confirmed in the proposal, with reasons)
| Idea | Decision | Reason |
|---|---|---|
| Dynamic reorder point (lead time and variability) | Rejected | No supplier lead times or stock movement dates in the data |
| ML demand forecasting | Rejected | Only 24 orders over about 5 months |
| Economic Order Quantity | Deferred | No holding cost or order cost in the data; replaced by a 2x reorder level heuristic |

---

## 3. Data and business rules

### Data available (to verify against the real database)
SQLite file `data/garden_shop.db`: 6 tables, 130 records (per the proposal). Tables inferred from the proposal's SQL:

| Table | Row represents | Fields seen in the proposal's SQL |
|---|---|---|
| `products` | One product (SKU) | `product_id`, `product_name`, `category_id`, `supplier_id`, `price`, `cost`, `quantity_on_hand`, `reorder_level`, `discontinued` |
| `categories` | One category | `category_id`, `category_name` |
| `suppliers` | One supplier | `supplier_id`, `supplier_name`, `contact_email`, state (column name not shown) |
| `orders` | One customer order | `order_id`, `status`, customer reference, order date (column names not shown) |
| `order_items` | One product line within an order | `order_id`, `product_id`, `quantity`, `unit_price` |
| customers | One customer | not shown in the proposal's SQL |

Relationships (inferred): `products.category_id` to `categories`, `products.supplier_id` to `suppliers`, `order_items.order_id` to `orders`, `order_items.product_id` to `products`.

Size per the proposal: 24 products (23 active, 1 discontinued), 8 categories, 6 suppliers, 24 orders, 20 customers, orders from 2024-01-15 to 2024-06-14. **Pending:** is there a data dictionary?

### Business rules
| Rule | Status |
|---|---|
| Orders with `status = 'cancelled'` are excluded from sales volume, revenue and restock prioritization (Order #17, 1 unit of Pruning Shears) | **Confirmed** |
| Discontinued products (`discontinued = 1`, Bird Feeder #24) never enter restock queues, PO recommendations or supplier deficit totals; they go to a clearance view | **Confirmed** |
| Orders in `processing` and `pending` count as valid demand in sales velocity | **Proposed** (the proposal treats them as valid; confirm) |
| Below reorder level means `quantity_on_hand < reorder_level` (strictly less than) | **Proposed** (confirm that equal counts as healthy) |
| Sales velocity is total units sold across the whole data period, not a daily rate | **Proposed** (follows from the data sparsity limitation) |

### Calculations
| Item | Formula (from the proposal) | Status |
|---|---|---|
| Minimum deficit | `MAX(0, reorder_level - quantity_on_hand)`; capital = deficit x `cost` | Proposed |
| Target par order | `MAX(0, 2 x reorder_level - quantity_on_hand)`; capital = units x `cost` | Proposed (2x is a heuristic, not a business rule) |
| Priority tiers | P4 if discontinued; P1 if stock = 0; P1 if below reorder level and units sold >= 4; P2 if below reorder level; P3 if stock < 1.5 x reorder level; otherwise P5 | Proposed (thresholds 4 and 1.5 need owner approval) |
| KPI definitions | Table in proposal section 4 | Proposed (see section 6) |

### Absences and limitations
- No stock movement history: only a point-in-time snapshot of stock.
- No supplier lead times.
- Very sparse sales (24 orders), so no statistical forecasting.
- Ironwood Tools has no email; RootWorks Supply also has none but has no products assigned.
- **Hypothesis:** the proposal says Hanging Basket has 0 sales because it is out of stock. The data cannot distinguish "never sold" from "could not sell". The dashboard should flag it as a stockout either way.
- **Pending:** handling of duplicates, invalid dates and orders with no matching product or customer. The proposal does not cover these.
- **Pending:** is any data sensitive (customer identity)? The first version does not appear to need customer details.

---

## 4. Solution

**Format (Proposed):** interactive dashboard with three levels of detail: executive KPIs, charts, then an action table. Layout is sketched as an ASCII wireframe in proposal section 5.1.

**Simplest alternative that still solves the problem:** the two SQL views plus one page with KPI cards and the restock table. Charts and the clearance drawer can follow. **Pending:** does the owner want this smaller first slice?

**Filters (Proposed):** category multi-select, supplier, stock health (out of stock / below reorder / watchlist / healthy), discontinued toggle (off in restock views).

**Main usage path:** the user opens the dashboard, reads the KPIs, filters by supplier or category, and works through the restock table from P1 down, preparing orders by supplier.

**No-results behavior (Pending):** what the dashboard shows when no product is below its reorder level.

---

## 5. Technical decisions

| Topic | Status |
|---|---|
| Data source: SQLite `data/garden_shop.db` | **Confirmed** |
| Semantic SQL views `vw_kpi_summary` and `vw_restock_workbench` between the database and the dashboard | **Proposed** |
| Front-end tool: Streamlit recommended; Power BI, Tableau and Metabase listed as alternatives | **Pending** (a recommendation, not a decision) |
| Language, libraries, how to run | **Pending** |
| Repository and where input/output files live | **Pending** |
| Implementation approach (SDD, TDD, combination, other) | **Pending** |

### Implementation approach (pending decision)
The template requires asking this before closing the work instructions. Short summary to help the choice:
- **SDD:** the specification guides planning, implementation and validation, and is revised when understanding changes.
- **TDD:** for each rule, write a test, see it fail for the expected reason, implement, then refactor.
- **Combination:** the specification guides delivery, and TDD drives the rules that are easy to test in isolation (priority tier, deficit, par order).

Recommendation (Proposal, to discuss): a combination, because the project is small but has precise rules (tiers, deficits, exclusions) that map well to small tests, while the dashboard layout is better guided by the specification. This is not a decision.

Follow-up questions to ask once chosen: which steps the agent follows, when the SPEC is reviewed, which checks run before a part counts as done, and what evidence is shown.

---

## 6. Acceptance criteria and examples

Reference values below are the proposal's figures. They are **expected results to verify against the database**, not verified facts.

| # | Check | Input | Expected result |
|---|---|---|---|
| A1 | Cancelled orders excluded | Order #17 (Pruning Shears, 1 unit, $22) | Not counted in units sold, revenue or tiers; total valid demand 86 units, revenue $1,107.00 |
| A2 | Discontinued excluded from restock | Bird Feeder #24 (4 on hand, reorder level 6) | Absent from the restock workbench and supplier totals; shown in clearance ($32 cost, $68 retail) |
| A3 | Below reorder level count | Active products | 5 products: Hanging Basket, Hand Cultivator, Tomato Seeds 'Roma', Orchid Food, Pothos 'Golden' |
| A4 | Stockout flagged | Hanging Basket #14 (0 on hand) | P1, shown as stockout |
| A5 | Minimum deficit and capital | The 5 products above | 60 units, $152.00 in total |
| A6 | Target par order | The 5 products above | 142 units, $383.00 in total |
| A7 | Stock value | Active products | 933 units, $4,731.00 at cost, $10,321.25 at retail |
| A8 | Inventory health | 18 of 23 active SKUs at or above reorder level | 78.3% |
| A9 | Supplier alert | Ironwood Tools, no email | Visible warning on the dashboard |
| A10 | Supplier rollup | Orders by supplier | Terra Pots $60.00; SunGrow $36.00; Bloomfield $31.50; Ironwood $24.50 |

**Edge cases to cover (Pending, to define with the owner):** no product below reorder level, a product with no sales, a product with no supplier, a supplier with no products.

**Who confirms the delivery meets the problem (Pending):** the proposal names the audience but not a person or role who signs off.

---

## 7. Points in the proposal to resolve before writing the SPEC

These are inconsistencies and gaps found while reading. None was changed in the proposal.

1. **SKU count by category adds up to 24, not 23.** The category table lists 5+3+3+3+3+2+2+3 = 24 SKUs but the active total says 23. Likely Outdoor Decor's 3 includes the discontinued Bird Feeder, while its 34 units exclude it. Check against the database.
2. **"8-way tie at 5 units sold" versus 7 items listed** in the high-volume answer (Fiddle-Leaf Fig, Monstera, Snake Plant, Pothos, Tulip Bulbs, Potting Soil, Compost Mix). One name is missing or the count is wrong.
3. **"Top volume decile" claim.** Tomato Seeds 'Roma' sold 4 units, below the 5-unit group, so the claim needs a definition of the top group.
4. **`vw_restock_workbench` only returns products below reorder level** (`WHERE quantity_on_hand < reorder_level` and `discontinued = 0`). So the view can never return P3, P4 or P5, although the proposal classifies all 24 products into 5 tiers and needs P3 and P4 data for the watchlist and the clearance drawer. Likewise the `P4` branch of its `CASE` is unreachable. A separate classification view over all products is probably needed.
5. **`suggested_po_units` in the view has no `MAX(0, ...)`**, unlike the formula in section 6.4.
6. **`vw_kpi_summary` does not compute** realized margin, revenue at risk or discontinued capital, which the KPI table and wireframe show.
7. **Revenue at Immediate Risk** uses `price` in the KPI definition, while the workbench view sums `unit_price` from `order_items`. Confirm which one the KPI uses (they may be equal in this data).
8. **KPI targets are proposals.** ">90%" health, ">50%" margin and "$0" for the others were not set by the business. The template says not to invent targets; confirm or mark as "monitor only".
9. **Priority names differ:** P2 is "Restock Scheduled" in the answer to question 6 and "Restock Required" in the algorithm. Clearance discount is "25%" in the wireframe and "25-30%" in section 6.2.
10. **Sign-off checklist marks all items as done** ([X]) and the proposal calls itself "production-ready". Nothing has been built, so the SPEC should treat these as planned, not verified.
11. **Wireframe mentions a "direct phone contact placeholder"** for Ironwood Tools, but the supplier fields shown do not include a phone number.

---

## 8. Open questions for the owner (ask in rounds of 2 to 4)

**Round 1: what changes the objective and scope**
1. Is the goal to deliver the working dashboard, or is the proposal itself the current deliverable (it refers to "Task 01" and "assignment objectives")? What is the deadline or environment?
2. What should the first version include: the smaller slice (views + KPI cards + restock table) or the full layout with charts and clearance drawer?
3. Who is the person who will confirm the dashboard is correct?

**Round 2: tools and way of working**
4. Which tool for the dashboard: Streamlit, Power BI, Tableau, Metabase, or other? Is there any mandatory language or tool?
5. Is there a repository or code to reuse? Where will the database and outputs live, and how are paths configured on another machine?
6. Implementation approach: SDD, TDD, a combination, or another (see section 5)?
7. In which language should the conversation and the four documents be written?

**Round 3: rules and acceptance**
8. Do `processing` and `pending` orders count as sales for the velocity ranking?
9. Are the priority thresholds (4 units sold, 1.5x reorder level) and the 2x par level approved, or should they be changed?
10. Which KPI targets are real business targets and which should be "monitor only"?
11. What should the dashboard do with duplicates, invalid dates and unmatched relationships, if any exist?
12. Which commands have already been run successfully on this database (for `AGENTS.md`)?

---

## 9. Synthesis for the four documents

| Document | What to take from this brainstorm |
|---|---|
| `PRD.md` | Sections 1, 2, 4 (problem, users, 7 questions, scope, exclusions, KPIs in business language, pending decisions) |
| `SPEC.md` | Section 3 (inputs, formulas, filters, relationships), section 6 (examples), the corrected views from section 7 |
| `AGENTS.md` | Section 5 (environment, implementation approach, commands), data care limits (read-only database, no fabricated lead times) |
| `CLAUDE.md` | Point to `AGENTS.md`, `PRD.md` and `SPEC.md`; add only Claude Code instructions the owner actually uses (pending) |

Keep one naming scheme in all four files: product/SKU, reorder level (ROP), deficit to minimum, target par order, priority tier P1 to P5, restock workbench, clearance drawer.

**Destination folder for the four files: Pending.** Ask before saving. Keep the original templates unchanged.
