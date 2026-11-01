# PRD — Product Requirements Document

> **Objective:** Define the problem, users, objectives, and product requirements for the Garden Shop Inventory & Restocking Decision Support Dashboard before starting implementation.

---

## 1. Project Identification
- **Project name:** Garden Shop Inventory Monitoring & Restocking Decision Support Dashboard
- **Document version:** 1.0
- **Status:** Approved
- **Owner:** Analytics & Operations Engineering Team
- **Date:** 2026-11-01

---

## 2. Overview

### 2.1. Context
Garden Shop is an established e-commerce business selling plants, seeds, gardening tools, planters, potting soils, and fertilizers across the United States. Operations rely on an SQLite database (`garden_shop.db`) tracking products, categories, suppliers, customers, orders, and order items. Replenishment decisions are currently handled through ad-hoc, manual database lookups or static spreadsheets.

### 2.2. Problem
The procurement and operations team suffers from operational blindness:
- They cannot quickly pinpoint which products are below safety reorder levels or completely out of stock.
- High-velocity bestsellers (such as *Pothos 'Golden'* and *Tomato Seeds 'Roma'*) risk stockout because current inventory is not dynamically evaluated against sales velocity.
- Discontinued products (such as *Bird Feeder*) risk being mistakenly reordered because stock is below legacy reorder points.
- Cancelled customer orders (such as Order #17) risk distorting true demand if counted as effective sales.
- Staff have no aggregated visibility into supplier-level restocking capital requirements or missing vendor contact credentials (*Ironwood Tools* has no email on file).

### 2.3. Proposed Solution
A centralized, interactive Decision Support Dashboard that ingests the relational dataset, strictly applies core business rules (filtering cancellations, isolating discontinued products, and preventing join balance duplications), and presents live KPI indicators, multi-dimensional filters, diagnostic visual charts, and an operational purchase order workbench.

### 2.4. Value Proposition
Eliminate avoidable stockouts on high-demand products, prevent capital lockup in dead inventory, and reduce the time required to compile supplier purchase orders from over 15 minutes to under 5 seconds.

---

## 3. Objectives and Expected Results

### 3.1. Objectives
- **OBJ-001:** Deliver immediate, automated visibility into all products requiring restocking (`quantity_on_hand < reorder_level`).
- **OBJ-002:** Correlate product inventory levels with actual customer sales velocity (excluding cancelled orders).
- **OBJ-003:** Provide supplier-grouped purchasing summaries with total shortage units and required reorder capital.
- **OBJ-004:** Enable interactive, zero-latency filtering by Category, Supplier, and Priority Tier.

### 3.2. Success Indicators

| Indicator | Current Situation | Target | How to Measure |
|---|---|---|---|
| **Inventory Health Index (%)** | 78.3% (5 of 23 active SKUs depleted) | $\ge 90.0\%$ | `(Healthy Active SKUs / Total Active SKUs) * 100` |
| **Critical Stockout Count** | 1 SKU (*Hanging Basket* = 0 units) | 0 SKUs | Count of active SKUs where `quantity_on_hand == 0` |
| **Bestsellers at Risk** | 2 SKUs (*Pothos*, *Tomato Seeds*) | 0 SKUs | Count of top-volume items operating below reorder point |
| **PO Compilation Time** | > 15 minutes (manual lookups) | < 5 seconds | Time to filter by vendor and review required PO quantities |

### 3.3. Success Criteria
- 100% of understocked products (5 active SKUs) are immediately flagged upon loading the dashboard.
- 0 cancelled orders are counted toward effective sales volume or revenue.
- 0 discontinued products receive automated replenishment recommendations.
- Total replenishment capital required to reach safety baseline ($152.00) is accurately computed.

---

## 4. Users and Needs

### 4.1. Target Audience
- **Operations Coordinator:** Responsible for daily morning triage, detecting zero-stock events, and monitoring fulfillment.
- **Purchasing / Procurement Specialist:** Responsible for drafting vendor purchase orders, negotiating order quantities, and managing vendor relationships.
- **Warehouse / Inventory Manager:** Responsible for physical storage space, clearance of discontinued items, and stock health audits.
- **Executive Leadership / Merchandising Director:** Needs high-level visibility into total inventory valuation ($4,731.00 cost / $10,321.25 retail) and gross margin protection.

### 4.2. User Needs
- As an **Operations Coordinator**, I want to filter products by stock health status (*Out of Stock*, *Low Stock*, *Healthy*) so that I can immediately triage critical shortages.
- As a **Purchasing Specialist**, I want to select a specific supplier from a dropdown so that I can view all their depleted items, unit deficits, and order costs in one consolidated table.
- As a **Warehouse Manager**, I want discontinued products isolated from the restock table into a clearance view so that we do not tie up capital reordering sunset inventory.
- As an **Executive**, I want to see the total inventory value at cost and potential retail margin so that I understand working capital exposure.

### 4.3. Main Journey
1. **Access:** User opens the dashboard application.
2. **Review:** User scans the Executive Scorecard (Inventory Health %, Stockouts, Capital to Min ROP).
3. **Filter:** User selects a category (e.g., *Seeds & Bulbs*) or a supplier (e.g., *Bloomfield Seeds*).
4. **Inspect:** User reviews the Priority Matrix chart and the Operational Restock Action Workbench.
5. **Act:** User views recommended purchase quantities and triggers a PO draft or CSV manifest export.

---

## 5. Product Scope

### 5.1. Included in Scope
- Ingestion and validation of the 6 relational tables from `data/garden_shop.db` (products, categories, suppliers, orders, order_items, customers).
- Calculation of at least two core operational indicators (Inventory Health Index and Capital Deficit).
- Multi-dimensional filtering by Product Category and Supplier.
- Search input for real-time SKU and vendor lookups.
- Visual stacked bar chart of category stock health.
- Visual quadrant scatter plot correlating current on-hand stock with units sold.
- Tabular Restock Action Workbench with sortable columns and priority badges.
- Dedicated Discontinued Inventory Clearance Drawer.
- Automated CSV manifest export.

### 5.2. Out of Scope
- Direct writeback or automated financial EDI transactions to external ERP/supplier platforms.
- Predictive machine learning forecasting (ARIMA/Prophet) due to sparse sales history (24 orders).
- Dynamic supplier lead-time safety stock modeling (no lead-time or shipping transit tracking in dataset).
- Customer-facing inventory storefront displays.

### 5.3. Assumptions
- The database file `data/garden_shop.db` contains clean, relational data adhering to the Data Dictionary.
- `quantity_on_hand` represents physical stock at the current point in time.
- All monetary values are recorded in USD ($).

### 5.4. Constraints
- **Data Boundary:** All analysis must preserve original database records; no external synthetic datasets.
- **Security & Privacy:** The repository `.gitignore` excludes `data/`; the dashboard must run either locally or via a self-contained application bundle.
- **Environment:** Must run seamlessly on standard Python 3.10+ environments.

---

## 6. Functional Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|---|---|---|---|
| **FR-001** | The system must calculate and display the **Inventory Health Index (%)** for active products. | Must | Displays `78.3%` on full active catalog (`18 / 23 * 100`). Updates dynamically when filters are applied. |
| **FR-002** | The system must calculate and display the **Replenishment Capital Deficit ($)** to reach minimum safety reorder level. | Must | Displays `$152.00` across the 60 deficit units for all 5 understocked active SKUs. |
| **FR-003** | The system must filter out cancelled orders from sales volume and revenue. | Must | Order #17 (1 unit of *Pruning Shears*) is excluded. *Pruning Shears* displays exactly 1 valid unit sold (from Order #7). Total store sales equals 86 units and $1,107.00 revenue. |
| **FR-004** | The system must exclude discontinued products from replenishment recommendations. | Must | Product #24 (*Bird Feeder*) is never shown in the restock queue, despite having stock (4) < ROP (6). Displayed only in the Clearance view. |
| **FR-005** | The system must provide dynamic filtering by Category and Supplier. | Must | Selecting a category (e.g., *Houseplants*) or supplier instantly updates all KPI cards, charts, and table rows without page reload. |
| **FR-006** | The system must classify products into explicit Priority Tiers (P1 to P5). | Should | Flags *Hanging Basket* (0 units) as P1 Critical Stockout, *Pothos 'Golden'* and *Tomato Seeds 'Roma'* as P1 Bestseller at Risk, and well-stocked items as P5. |
| **FR-007** | The system must alert users if a supplier has missing contact credentials. | Should | Surfaces an operational warning when *Ironwood Tools* (missing email) is involved in replenishment. |
| **FR-008** | The system must provide an exportable Purchase Order manifest. | Could | User can click a button to download filtered restock lines as a CSV file. |

---

## 7. Non-Functional Requirements

| ID | Category | Requirement | Verification Criteria |
|---|---|---|---|
| **NFR-001** | Performance | Dashboard initial load time $\le 1.5$ seconds. Filter interaction latency $\le 50$ milliseconds. | Measured in browser DevTools and Streamlit execution timer. |
| **NFR-002** | Usability | Responsive layout with clear visual hierarchy, color-coded priority badges, and formatted currency. | Visual inspection on desktop (1920x1080) and tablet viewports. |
| **NFR-003** | Reliability | Application must handle empty filter results gracefully without raising unhandled exceptions. | Test with non-matching search string (e.g., `"xyz"`): shows empty state message. |
| **NFR-004** | Maintainability | Clean separation between data extraction, business logic, test suites, and presentation layer. | Modular code organization verified by automated tests. |

---

## 8. Data and Integrations
- **Data sources:** SQLite relational database (`data/garden_shop.db`).
- **Inputs:** 6 tables: `categories`, `customers`, `orders`, `order_items`, `products`, `suppliers`.
- **Outputs:** Interactive UI, KPI summary cards, dynamic charts, CSV purchase order manifests.
- **Integrations:** None required (standalone local / static GitHub Pages architecture).
- **Sensitive data:** Customer email, phone, and city/state are present in `customers`. The dashboard aggregates order items and does not expose private customer PII in restock tables.
- **Retention and disposal:** Read-only access; source database is unmodified.

---

## 9. Business Rules
- **BR-001 (Cancelled Orders):** Orders with `status = 'cancelled'` must be completely excluded from sales velocity, gross revenue, and order occurrence counts.
- **BR-002 (Pipeline Demand):** Orders with `status IN ('shipped', 'processing', 'pending')` represent confirmed customer demand and are included in sales metrics.
- **BR-003 (Discontinued Products):** Products with `discontinued = TRUE` (or `1`) must not receive automatic replenishment recommendations, regardless of stock deficit.
- **BR-004 (Inventory Balance Integrity):** When calculating inventory metrics, product balances (`quantity_on_hand`, `cost`, `price`) must be evaluated per product and never multiplied across joined order line items.
- **BR-005 (Replenishment Prioritization):**
  - **P1 (Urgent):** Active item with `quantity_on_hand == 0` OR (`quantity_on_hand < reorder_level` AND `units_sold >= 4`).
  - **P2 (Restock Scheduled):** Active item with `quantity_on_hand < reorder_level` and moderate velocity.
  - **P3 (Watchlist):** Active item with `quantity_on_hand < reorder_level * 1.5`.
  - **P4 (Discontinued):** `discontinued == TRUE`.
  - **P5 (Healthy):** Active item with `quantity_on_hand >= reorder_level * 1.5`.

---

## 10. Flows and Exceptions

### 10.1. Main Flow
1. Application initializes and connects to `garden_shop.db`.
2. Queries extract product inventory, category hierarchies, supplier profiles, and aggregated non-cancelled sales.
3. System applies business rules (BR-001 to BR-005) and calculates baseline KPIs.
4. UI renders header, filter controls, KPI scorecards, diagnostic charts, and the restock action table.
5. User adjusts a filter; system dynamically recalculates and re-renders visible metrics.

### 10.2. Alternative Flows
- **Filter with Zero Matches:** If a user selects a filter combination yielding no rows, the dashboard displays `"No products match the selected criteria"` and zeros out filtered totals rather than crashing.
- **Export Trigger:** User clicks "Export PO Manifest (CSV)"; browser generates a downloadable file containing the visible filtered table.

### 10.3. Error Handling
- **Database Missing:** If `data/garden_shop.db` is not found, application displays a clear error instructing the user to verify database placement.
- **Corrupted Records:** Null supplier emails are replaced with `"[NO EMAIL ON FILE]"` and flagged with warning badges.

---

## 11. Experience and Interface
- **Platform:** Web application (Streamlit Python dashboard and standalone HTML5/Tailwind/Chart.js web app).
- **Interface States:**
  - *Normal:* Full dashboard displaying all active products.
  - *Filtered:* Dynamically scoped metrics and charts based on active dropdown selections.
  - *Empty:* Graceful informational placeholder when filters match zero items.
- **Compatibility:** Modern web browsers (Chrome, Edge, Firefox, Safari).

---

## 12. Risks and Dependencies

| Risk or Dependency | Impact | Mitigation |
|---|---|---|
| Inadvertent join duplication inflating stock values | High | Aggregate sales by `product_id` in a CTE/subquery before joining with `products`. Validate with unit tests. |
| Counting cancelled Order #17 in sales velocity | Medium | Enforce `status != 'cancelled'` predicate across all sales aggregation queries. |
| Missing supplier email delaying purchase orders | Medium | Visual procurement warning banner alerting staff to contact *Ironwood Tools* by phone. |
| Incomplete date parsing | Low | Use standard ISO parsing for order dates. |

---

## 13. Deliverables
- **`PRD.md`**: Complete Product Requirements Document.
- **`SPEC.md`**: Technical software specification and data contracts.
- **`AGENTS.md`**: Developer and AI agent execution instructions.
- **`data_loader.py`**: Validated data access layer with business rule enforcement.
- **`tests/test_indicators.py`**: Automated test suite verifying indicators on data subsets.
- **`app.py`**: Interactive Streamlit dashboard application.
- **`dashboard_screenshot.png`**: Legible screenshot of the active dashboard.

---

## 14. Product Completion Criteria
The product will be ready when:
- All functional requirements (FR-001 through FR-008) are implemented.
- Acceptance criteria are verified against SQLite database ground truth.
- All automated unit tests in `tests/test_indicators.py` pass with 0 failures.
- Documentation (`PRD.md`, `SPEC.md`, `AGENTS.md`) is fully articulated and aligned with implementation.
- Legible screenshot of the running dashboard is captured.

---

## 15. Relationship with Technical Documents
- **Reference specification:** [`./exercise/Task_02/SPEC.md`](./SPEC.md)
- **General instructions for agents:** [`./exercise/Task_02/AGENTS.md`](./AGENTS.md)
- **Data Dictionary:** [`./exercise/Task02-Data_Dictionary.md`](../Task02-Data_Dictionary.md)

---

## 16. Pending Decisions

| ID | Question | Owner | Status |
|---|---|---|---|
| PD-001 | Should safety stock par level default to 1.5x or 2.0x ROP? | Operations Lead | Resolved (2.0x ROP adopted as standard par order) |
| PD-002 | Deploy as pure Streamlit app or static GitHub Pages web app? | Tech Lead | Resolved (Provide both: Streamlit for Python users, HTML5 for zero-server GitHub Pages) |

---

## 17. Change History

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-11-01 | Initial baseline PRD for Task 02 created from template. |
