# DSAT5-IAGP-Project-GardenShop

> **Garden Shop Project**  
> Operational Intelligence, Inventory Management, and Replenishment Decision Support System for an E-Commerce Garden Supply Business.  
> Developed with Generative AI assistance and rigorous relational database analysis.

---

# Task 01


## 📌 Table of Contents
- [Project Overview](#project-overview)
- [Relational Dataset](#relational-dataset)
- [Task 01: Dashboard Proposal & Strategic Inventory Diagnosis](#task-01-dashboard-proposal--strategic-inventory-diagnosis)
  - [1. Dashboard Objective and Business Needs Addressed](#1-dashboard-objective-and-business-needs-addressed)
  - [2. Answers to Management's 7 Key Strategic Questions](#2-answers-to-managements-7-key-strategic-questions)
  - [3. Key Performance Indicators (KPIs) & Business Justifications](#3-key-performance-indicators-kpis--business-justifications)
  - [4. Business Rules & Data Handling Logic](#4-business-rules--data-handling-logic)
  - [5. Dataset Limitations & Operational Impact](#5-dataset-limitations--operational-impact)
  - [6. Interactive Dashboard Architecture & UI Modules](#6-interactive-dashboard-architecture--ui-modules)
- [Official Deliverable (.docx Word Proposal)](#official-deliverable-docx-word-proposal)
- [Tech Stack](#tech-stack)


---

## 🌿 Project Overview

**Garden Shop** is an e-commerce retailer specialized in gardening supplies, houseplants, seeds, tools, planters, potting soil, and fertilizers. The company maintains an operational relational database tracking products, categories, customers, orders, order items, and suppliers.

The management team faced a critical issue of **operational blindness**: difficulty identifying products requiring urgent attention, determining whether available physical inventory is sufficient relative to incoming sales velocity, and prioritizing procurement orders without tying up excess working capital.

This repository implements an interactive, production-ready **Inventory & Replenishment Intelligence Dashboard**, complete with a purchase order simulator and an automated generator for the official formal Word document (`.docx`).

---

## 🗄️ Relational Dataset

The analysis is based on the benchmark [Garden Shop SQL Practice Dataset](https://sqlshed.com/practice-datasets/garden-shop/):
- **Tables (6):** `products`, `categories`, `suppliers`, `orders`, `order_items`, `customers`
- **Volume:** 130 records in total (24 products, 8 categories, 6 suppliers, 24 orders, 48 order line items, and 20 customers).

---

## 🚀 Task 01: Dashboard Proposal & Strategic Inventory Diagnosis

### 1. Dashboard Objective and Business Needs Addressed
The primary objective is to transform raw transactional and inventory records into an intuitive, daily tactical decision-support dashboard for the procurement and operations team:
- **Eradicate Out-of-Stock Events (*Stockouts*):** Immediate alerts for products with 0 stock or stock below safety thresholds (`reorder_level`).
- **Turnover vs. Stock Coverage Analysis:** Correlating real sales velocity with remaining physical stock to detect imminent stock depletion.
- **Working Capital Optimization:** Real-time visibility into total tied-up inventory value at cost and the exact budget needed for reorders.
- **Supplier Order Automation:** Grouping deficient products by vendor and auto-generating quotation requests with supplier contact details.

---

### 2. Answers to Management's 7 Key Strategic Questions

Grounded directly in the database records, the dashboard answers the 7 core executive questions:

| Management Question | Analytical Diagnosis & Data Evidence |
| :--- | :--- |
| **1. Which products are below the recommended reorder level?** | **5 active SKUs:**<br>• *Tomato Seeds 'Roma'* (5 units in stock vs reorder level 40 — **critical deficit of -35 units**)<br>• *Hanging Basket* (0 units in stock vs reorder level 10 — **total stockout**)<br>• *Hand Cultivator* (3 units in stock vs reorder level 10 — **deficit of -7 units**)<br>• *Pothos 'Golden'* (8 units in stock vs reorder level 12 — **deficit of -4 units**)<br>• *Orchid Food* (6 units in stock vs reorder level 10 — **deficit of -4 units**)<br>*(Bird Feeder has 4 units vs reorder level 6, but was excluded because it is discontinued).* |
| **2. Which products are currently out of stock or running very low?** | • **Out of Stock (Zero Inventory):** *Hanging Basket* (0 units — actively losing e-commerce cart conversions).<br>• **Very Low Stock (≤ 10 units):** *Hand Cultivator* (3 un), *Bird Feeder* (4 un — discontinued), *Tomato Seeds 'Roma'* (5 un), *Orchid Food* (6 un), *Pothos 'Golden'* (8 un), and *Solar Lantern* (9 un). |
| **3. Which products show the highest sales volume and deserve availability monitoring?** | *Sunflower Seeds* has the highest absolute sales volume (12 units sold, but 200 units in stock provide ample safety). The **critical risk** lies with **Tomato Seeds 'Roma'** (4 units sold with only 5 remaining in stock) and **Pothos 'Golden'** (5 units sold with only 8 remaining in stock). |
| **4. Which categories concentrate the most products in need of replenishment?** | Reorder requirements span 5 key categories:<br>• *Pots & Planters* (1 SKU out of stock)<br>• *Seeds & Bulbs* (1 SKU with a 35-unit deficit)<br>• *Tools* (1 SKU)<br>• *Houseplants* (1 SKU)<br>• *Fertilizer* (1 SKU) |
| **5. What is the estimated total inventory value at registered cost?** | • **Total Inventory Value at Cost:** **\$4,731.00** (933 units across 23 active SKUs) / **\$4,763.00** (937 units across all 24 SKUs).<br>• **Total Inventory Value at Retail Price:** **\$10,321.25** (across 23 active SKUs).<br>• **Estimated Reorder Budget Required:** **\$152.00** (60 units deficit) to restore all critical products to safety levels. **\$383.00** (If using a 2x ROP safety target, it is \$383.00 (142 units)). |
| **6. Which products should the management team prioritize for immediate action?** | • **Priority 1 (Emergency / Day 0):** *Hanging Basket* (zero stock; issue emergency purchase order today).<br>• **Priority 2 (Imminent Stockout Risk):** *Tomato Seeds 'Roma'* (deficit of 35 units) and *Hand Cultivator* (3 units remaining).<br>• **Priority 3 (Clearance Strategy):** *Bird Feeder* (discontinued; do not reorder; discount remaining 4 units). |
| **7. Which suppliers are linked to products requiring replenishment?** | • **Terra Pots Co** (OH, `hello@terrapots.example`): *Hanging Basket*<br>• **Bloomfield Seeds** (OR, `contact@bloomfield.example`): *Tomato Seeds 'Roma'*<br>• **SunGrow Nurseries** (FL, `sales@sungrow.example`): *Pothos 'Golden'* & *Orchid Food*<br>• **Ironwood Tools** (PA, *no email registered — operational limitation*): *Hand Cultivator* |

---

### 3. Key Performance Indicators (KPIs) & Business Justifications
1. **Safety Stock Coverage Ratio (`quantity_on_hand / reorder_level`):** Provides instant traffic-light classification (Red = Stockout, Amber = Critical, Yellow = Borderline/Warning, Green = Healthy).
2. **Physical Deficit Units (`reorder_level - quantity_on_hand`):** Quantifies the exact shortfall needed to recover baseline protection.
3. **Total Inventory Value at Cost:** Tracks tied-up working capital (\$4,731.00).
4. **Estimated Replenishment Cost:** Pre-calculated budgetary requirement based on registered cost prices (\$152.00).
5. **Real Sales Velocity per SKU:** Net units shipped/processed, excluding canceled orders.

---

### 4. Business Rules & Data Handling Logic

#### A) Exclusion of Canceled Orders
- In the `orders` table, **Order #17** (customer Lucas Romano, placed 2024-04-03) has `status = 'cancelled'`. This order contained 1 unit of *Pruning Shears* (item ID 9).
- **Rule:** Real customer demand must only account for valid orders (`status != 'cancelled'`). Including canceled orders would artificially inflate product turnover and cause over-purchasing. The dashboard includes an interactive toggle to audit this rule in real time.

#### B) Exclusion of Discontinued Products
- The item **Bird Feeder** (product ID 24) has 4 units in stock and `reorder_level = 6` (a mathematical deficit of -2 units).
- **Rule:** The flag `discontinued = TRUE` indicates that the company will not replenish this product. The business rule strictly prevents automated reorder recommendations for this item and prompts a promotional clearance of the remaining 4 units, protecting capital from dead stock.

#### C) Operational Reorder Recommendation Algorithm
- Ordering only the deficit quantity would cause inventory to drop back below the safety threshold on the very next sale. The algorithm applies a 50% buffer over the reorder level:
$$\text{Recommended Purchase Quantity} = (\text{reorder\_level} - \text{quantity\_on\_hand}) + (\text{reorder\_level} \times 0.5)$$

---

### 5. Dataset Limitations & Operational Impact
1. **Absence of Supplier Lead Times:** The dataset does not track delivery lead time (days required from purchase order to warehouse arrival). Thus, reorder levels must remain static rather than dynamically scaling with transit variance.
2. **Lack of Inventory Transaction Logs (Kardex):** The database only captures a static snapshot (`quantity_on_hand`), with no audit trail for inbound receipts, shrinkage/plant spoilage, or customer returns.
3. **Incomplete Supplier Contact Information:** Suppliers *Ironwood Tools* and *RootWorks Supply* have `NULL` contact emails, necessitating manual phone follow-up.
4. **Absence of Minimum Order Quantities (MOQ) and Freight Costs:** No case pack or shipping minimum constraints are modeled, requiring buyer review during negotiation.

---

### 6. Interactive Dashboard Architecture & UI Modules
The application is structured into 6 specialized views:
- 📊 **Executive Overview:** High-level KPI cards, category risk charts, and an interactive diagnostic panel answering the 7 executive questions.
- 📦 **Inventory & Replenishment Matrix:** Interactive table with three-dimensional filters (Status, Category, Supplier), real-time search, visual stock meters, and action buttons.
- 🚚 **Supplier Intelligence:** Overview of all 6 suppliers with geography, contact status, and critical SKU allocation.
- 🛒 **Purchase Order Simulator:** Interactive quantities adjustment, live cost recalculation, and one-click quotation export grouped by vendor.
- 📄 **Word Proposal Deliverable (.docx):** Full formatted academic/executive report with direct download of the official `.docx` file.
- 🔍 **SQL Database Auditor:** Raw table inspector allowing verification across all 6 tables.

---

## 📄 Official Deliverable (.docx Word Proposal)

As required by the assignment guidelines (*"Entregue um único arquivo Word contendo a proposta final do dashboard"*), the complete formal proposal can be downloaded directly from the application in Microsoft Word format (`.docx`).

- **File Name:** [`Garden_Shop_Inventory_Dashboard_Proposal.docx`](./exercise/Task_01/Garden_Shop_Inventory_Dashboard_Proposal.docx)
- **Contents:** Executive summary, project objectives, KPI definitions, UI/chart justifications, business rules with mathematical formulations, answers to all 7 questions, dataset limitations, and a phased action plan.

<br>

- **File Name:** [PRD.md](./exercise/Task_01/PRD.md)
- **Contents:** Product Requirement Document.

---

## 🛠️ Tech Stack

- **Database:** SQLite 3 (`data/garden_shop.db`)
- **Web Dashboard (GitHub Pages):** HTML5, Tailwind CSS, Chart.js
(zero-server, client-side dynamic filtering)
- **Data Science & Local Prototype:** Python 3.12, Pandas, Streamlit,
Plotly
- **Document Generation:** `python-docx`, `lxml`
- **Visualization:** Matplotlib, Seaborn
                                                                            
---    

