# PRD: Garden Shop Inventory Monitoring & Restocking Decision Support Dashboard

**Author:** Raquel Marques
**Status:** In review  
**Last updated:** 2026-10-31  

---

## Problem

Garden Shop's warehouse and purchasing staff (e.g., operations coordinators preparing weekly vendor orders) currently have no unified, real-time visibility into inventory depletion, safety stock thresholds, or supplier dependencies. When high-velocity gardening products like *Pothos 'Golden'* or *Tomato Seeds 'Roma'* deplete to danger levels, operations staff only discover the stockout reactively after customer orders stall in "pending" or "processing" status. Without an automated decision support system connecting on-hand inventory to supplier profiles and sales demand, purchasing decisions are made via fragmented manual spreadsheet lookups. This causes avoidable stockouts on top revenue drivers (such as *Hanging Basket* currently sitting at zero units), risks lost sales, and leaves working capital trapped in discontinued products (*Bird Feeder*).

---

## Goals

- An operations coordinator can identify all products below reorder point and their associated suppliers in under 5 seconds.
- Zero stockout occurrences for high-velocity SKUs (top 30% sales volume) by surfacing proactive Priority 1 (P1) replenishment warnings before physical stock depletion.
- Purchasing specialists can generate consolidated vendor replenishment manifests (detailing exact unit deficits, unit costs, and total capital needed) with a single click.
- The dashboard is 100% version-controlled, maintained, and published directly through GitHub (e.g., GitHub Pages or Streamlit Cloud connected to the repository), providing instantaneous client-side dynamic filtering with zero server infrastructure overhead.

---

## Non-goals

- **Dynamic Lead-Time Modeling & ML Forecasting:** We are deliberately NOT implementing predictive ARIMA/Prophet time-series models or dynamic lead-time safety stock algorithms. The database lacks supplier delivery lead times and transit logs, and 24 orders across 5 months represent sparse event density where statistical forecasting would hallucinate arbitrary trends.
- **Two-Way ERP/WMS Transaction Writeback:** This dashboard is a read-only Decision Support System (DSS). It will NOT execute automated financial transactions, place binding EDI purchase orders, or write inventory adjustments back to `garden_shop.db`.
- **Live IoT / Real-Time RFID Warehouse Tracking:** We are not building real-time warehouse location tracking or bin-sensor telemetry. The system ingests the batch relational database snapshot.
- **Customer-Facing Storefront Inventory:** Out of scope. This dashboard is strictly an internal operational tool for operations, merchandising, and warehouse leadership.

---

## User stories

- As an **Operations Coordinator**, I want to filter products by stock health status (*Out of Stock*, *Below Reorder Point*, *Healthy*) so that I can triage immediate inventory emergencies during morning standups.
- As a **Purchasing Specialist**, I want to select a supplier from a dropdown and see all their understocked items, shortage deficits, and required capital so that I can draft purchase orders in minutes.
- As a **Warehouse Manager**, I want discontinued products strictly quarantined from replenishment queues into a separate Clearance Drawer so that the business never reorders sunset inventory.
- As an **Executive / Merchandising Director**, I want to monitor active inventory capital valuation ($4,731.00 cost / $10,321.25 retail) and gross margin health so that I can balance working capital with fulfillment service levels.
- As a **Stakeholder / Auditor**, I want to open a URL directly hosted on GitHub, interact with dynamic multi-select filters, and drill into category diagnostics without needing a local Python or database installation.

---

## Requirements

### Must have

1. **Strict Order Status Filtration (Business Rule 1):**
   - The reporting engine must explicitly filter out cancelled orders (`WHERE orders.status != 'cancelled'`).
   - Order #17 (1 unit of *Pruning Shears*, customer #9) must be excluded from effective sales volume, realized gross revenue, and depletion velocity calculations.
   - Orders in `shipped` (17 orders, 66 units) represent fulfilled historical sales; orders in `processing` (3 orders, 11 units) and `pending` (3 orders, 9 units) represent committed pipeline demand.

2. **Strict Discontinued Product Isolation (Business Rule 2):**
   - Products marked `discontinued = 1` (*Bird Feeder*, SKU #24) must be programmatically excluded from all automated restock recommendations, reorder queues, and supplier deficit tallies (`WHERE products.discontinued = 0`).
   - Discontinued items must be routed to a dedicated "Clearance & Liquidation Drawer" displaying locked capital ($32.00 cost) with recommended markdown actions.

3. **5-Tier Operational Priority Triage Engine:**
   - Every catalog item must be automatically classified into an actionable priority tier:
     - **P1 - Critical Stockout / Bestseller at Risk:** Zero stock (*Hanging Basket*) OR under reorder level with high sales volume (*Pothos 'Golden'*, *Tomato Seeds 'Roma'*).
     - **P2 - Restock Scheduled:** Active products below reorder level with moderate velocity (*Hand Cultivator*, *Orchid Food*).
     - **P3 - Watchlist (Near Threshold):** Active products within 150% of reorder level (*Solar Lantern*, *Fiddle-Leaf Fig*, *Cactus Mix Soil*).
     - **P4 - Discontinued Liquidation:** Inactive products with positive stock (*Bird Feeder*).
     - **P5 - Healthy Inventory:** Active products meeting or exceeding safe stock thresholds (15 SKUs).

4. **Dynamic Client-Side Filtering & Slicing:**
   - Instantaneous filtering by **Category** (8 categories: *Houseplants*, *Seeds & Bulbs*, *Tools*, *Pots & Planters*, *Soil & Compost*, *Watering*, *Fertilizer*, *Outdoor Decor*).
   - Instantaneous filtering by **Supplier** (6 suppliers).
   - Instantaneous filtering by **Inventory Health Tier** (*Out of Stock*, *Below Reorder*, *Watchlist*, *Healthy*).
   - Independent toggle switch to show/hide discontinued products (default: OFF in reorder views, ON in inventory audit views).

5. **Executive Summary KPI Scorecard:**
   - **Inventory Health Index:** Display percentage of active SKUs meeting safety stock (Current: **78.3%**; Target: >90%).
   - **Active Stockouts:** Count of SKUs with 0 physical units (Current: **1 SKU** - *Hanging Basket*).
   - **SKUs Below Reorder Point:** Count of understocked active SKUs (Current: **5 SKUs**).
   - **Immediate Restock Capital Needed:** Working capital needed to reach reorder level (Current: **$152.00** across 60 deficit units).
   - **Active Inventory Valuation:** Real-time cost ($4,731.00) and retail market value ($10,321.25) across 933 physical units.
   - **Revenue at Immediate Risk:** Gross revenue generated by currently understocked SKUs ($71.00).

6. **Interactive Visual Diagnostic Suite:**
   - **Chart 1: Category Stock Health Distribution:** Stacked horizontal or vertical bar chart showing Out of Stock, Below Reorder, and Healthy SKU counts per category.
   - **Chart 2: Priority Scatter Matrix (Stock vs. Sales Velocity):** Visual quadrant plot mapping on-hand inventory against historical units sold, visually isolating the high-risk upper-demand/lower-stock quadrant.
   - **Chart 3: Supplier Restock Capital & Deficit Allocation:** Bar chart breaking down purchasing capital needed and units deficit across all 4 impacted vendors.

7. **Operational Restock Action Workbench (Data Grid):**
   - Interactive, sortable tabular grid containing: Product ID, Product Name, Category, Supplier, Unit Price, Unit Cost, Quantity on Hand, Reorder Level, Shortage Deficit, Capital Needed, and Priority Badge.
   - Highlight supplier data gaps prominently (e.g. flashing warning badge on *Ironwood Tools* indicating **MISSING CONTACT EMAIL**).

8. **GitHub-Centric Storage & Publishing Architecture:**
   - The entire codebase, database snapshot, build scripts, and dashboard deployment assets must reside in this Git repository.
   - The live dashboard must be publishable to **GitHub Pages** (as a static client-side web application with dynamic filtering) or **Streamlit Community Cloud** (directly synchronized with the GitHub repository).

### Nice to have

- **One-Click Vendor Order Manifest Export:** Button to download filtered restock lines as a vendor-ready CSV or formatted PDF.
- **Automated "Mailto:" PO Draft Launcher:** Clicking a supplier row opens the user's default email client pre-populated with the supplier's contact email, subject line ("Purchase Order - Garden Shop"), and a pre-formatted body table of required SKUs and quantities.
- **WebAssembly In-Browser SQL Console:** An optional developer tab powered by `sql.js` or `DuckDB-WASM` enabling power users to run ad-hoc SQL queries against `garden_shop.db` directly inside the browser.
- **Warehouse Dark Mode:** High-contrast UI theme tailored for mobile tablets and warehouse floor handhelds.

---

## Architecture & Publishing Strategy (Brainstorming & Technical Evaluation)

To fulfill the requirement of creating a dashboard that is **dynamically filterable** and **stored/published via GitHub**, we evaluated four architectural pathways:

| Architectural Option | Technology Stack | Hosting & GitHub Integration | Pros | Cons | Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Option A: Client-Side Web App (SPA) on GitHub Pages** | HTML5, Tailwind CSS, Chart.js / Plotly, vanilla JS or lightweight React/Vue | **GitHub Pages** (native to repository, zero external hosting) | • 100% free, permanent URL.<br>• Instant client-side dynamic filtering with 0 latency.<br>• Zero server maintenance, zero cold-starts.<br>• GitHub Actions extracts SQLite data to `data.json` on push. | • Requires frontend web build or automated JSON extraction pipeline. | **TOP RECOMMENDATION for GitHub Pages** |
| **Option B: Streamlit Community Cloud** | Python, Streamlit, Pandas, SQLite3 | **Streamlit Cloud** connected directly to the GitHub repo | • Pure Python development.<br>• Queries `data/garden_shop.db` directly using native SQLite.<br>• Rich out-of-the-box widgets, filters, and tables.<br>• Continuous deployment on `git push`. | • App sleeps after periods of inactivity on free tier (takes 10-15s to wake).<br>• Hosted on `share.streamlit.io` rather than `github.io`. | **TOP RECOMMENDATION for Python Ecosystem** |
| **Option C: Evidence.dev on GitHub Pages** | Markdown + SQL + DuckDB-WASM | **GitHub Pages** via GitHub Actions workflow | • Code-driven BI: writes SQL queries inside Markdown documents.<br>• Compiles to ultra-fast static site.<br>• Renders interactive charts with client-side DuckDB. | • Requires Node.js build step and familiarization with Evidence syntax. | **Strong Alternative for SQL-centric teams** |
| **Option D: In-Browser SQLite via WebAssembly (sql.js / DuckDB-WASM)** | WebAssembly (WASM), JavaScript, HTML | **GitHub Pages** loading `garden_shop.db` into browser memory | • Delivers the literal SQLite database to the browser.<br>• Enables interactive SQL filtering in real time on GitHub Pages. | • Slightly heavier initial page payload (WASM binary + database file). | **Excellent Hybrid Enhancement** |

### Selected Publishing Architecture: Hybrid Client-Side SPA for GitHub Pages

For maximum reliability, zero hosting cost, and pure GitHub integration, the recommended path is:
1. **Repository Core:** `data/garden_shop.db` remains the authoritative database in Git.
2. **Automated Data Extraction:** A lightweight Python script (executable locally or via GitHub Actions) executes verified SQL views against `garden_shop.db` and exports structured, optimized data into `dashboard_data.json`.
3. **Interactive Frontend:** A responsive, modern single-page dashboard application (`index.html`) using Tailwind CSS and Chart.js.
4. **Publishing:** Deployed to **GitHub Pages** (via the `docs/` folder or `gh-pages` branch). When any user visits `https://<username>.github.io/<repo>/`, the browser loads the page, fetches `dashboard_data.json`, and provides instantaneous dynamic filtering across categories, suppliers, and stock tiers without needing any backend server.
5. **Parallel Streamlit Option:** A companion `app.py` script can also be maintained in the repository for local operational exploration or one-click deployment to Streamlit Community Cloud.

---

## Success metrics

- **100% Triage Coverage:** All 5 understocked active SKUs are prominently displayed on the default dashboard view without requiring manual search.
- **Stockout Elimination:** 0 stockouts on top-volume SKUs over the next 90 days following dashboard adoption.
- **Triage Speed:** Time to identify all supplier replenishment requirements reduced from >15 minutes to **under 5 seconds**.
- **Page Load & Interaction Latency:** The GitHub Pages dashboard achieves a First Contentful Paint (FCP) of **< 1.0s** and filter response times of **< 50ms** (instantaneous client-side filtering).
- **Data Governance Accuracy:** 0 cancelled orders included in sales velocity and 0 discontinued products recommended for replenishment.

---

## Rollout

- **Ship behind:** Phased Git deployment. 
  - *Phase 1:* Local build and verification in `./exercise/Task_01`.
  - *Phase 2:* Deployment of static dashboard assets to GitHub Pages (`docs/` or `gh-pages`).
  - *Phase 3:* Optional activation of Streamlit Community Cloud instance.
- **Before launch:**
  - Execute automated verification script checking that KPI scorecard numbers match SQL truth from `garden_shop.db`.
  - Validate that Order #17 (cancelled) is excluded and Bird Feeder #24 (discontinued) is routed only to the Clearance view.
  - Review dashboard layout on desktop and mobile viewports.
- **Rollback:**
  - Standard Git revert (`git revert <commit-hash>`). GitHub Pages re-deploys previous working state in under 60 seconds.
