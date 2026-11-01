# Business Rules & Metrics Reference — Olist Analytics

This document defines the official business rules, metric formulas, and edge-case handling conventions for analytics on the Olist e-commerce database.

---

## 1. Scope & Delivered Order Definition

All standard marketplace performance questions apply specifically to **delivered orders** unless the user explicitly requests otherwise.

- **Delivered Order Criterion:**
  - Table: `pedido.csv`
  - Field: `descSituacao == 'delivered'`
- **Order Count Granularity:**
  - Count distinct `idPedido` values.
  - Never count raw line items (`item_pedido.csv`) or payments (`pagamento_pedido.csv`) as orders.
- **Reference Date:**
  - The default temporal reference for all period analyses is `dtPedido` (order placement timestamp).
  - Date format in Olist: `YYYY-MM-DD HH:MM:SS`.
  - Date filtering includes start and end boundaries (inclusive dates: e.g. `start_date <= dtPedido[:10] <= end_date`).

---

## 2. Metric Formulas

### 2.1. Monthly Delivered Orders
- **Objective:** Number of distinct delivered orders placed in each calendar month.
- **Formula:**
  $$\text{Monthly Orders} = \text{Count}(\text{distinct } idPedido) \quad \text{where } descSituacao = \text{'delivered'}$$
  grouped by `SUBSTR(dtPedido, 1, 7)` (e.g. `2017-01`).
- **Edge cases:**
  - Months with zero orders return count `0`.

### 2.2. Top 5 Customer States (UF)
- **Objective:** Top 5 Federative Units (UFs) ranked by volume of delivered orders.
- **Table Relationship:**
  - Join `pedido.csv` on `idCliente` to `cliente.csv` on `idCliente`.
- **Field:** `cliente.descUF`.
- **Formula:**
  $$\text{Orders per UF} = \text{Count}(\text{distinct } idPedido) \quad \text{where } descSituacao = \text{'delivered'}$$
  sorted descending, top 5.
- **Edge cases:**
  - Unmatched customer records should be categorized as `UNKNOWN` rather than silently dropped.

### 2.3. Average Ticket per Delivered Order (Excluding Freight)
- **Objective:** Average spending on items per delivered order.
- **Table Relationship:**
  - Match delivered orders from `pedido.csv` to their items in `item_pedido.csv` by `idPedido`.
- **Formula:**
  $$\text{Average Ticket} = \frac{\sum (vlPreco)}{\text{Count}(\text{distinct delivered } idPedido)}$$
- **Freight Exclusion:**
  - Explicitly exclude `vlFrete`. Do not include freight costs in the ticket calculation.
- **Coverage & Orders Without Items:**
  - In Olist, 100% of delivered orders have item records (96,478 / 96,478).
  - If a filtered subset contains delivered orders with zero items, their item total contribution is 0, but the distinct order remains in the denominator.
  - If distinct delivered orders count is 0, the Average Ticket is **Not Applicable (N/A)**.

---

## 3. Data Integrity & Join Cardinality Rules

1. **Avoid Cartesian Duplication:**
   - Orders can have multiple items and multiple payment installments.
   - When calculating item metrics, aggregate `item_pedido.csv` items or sum item prices directly filtered on delivered `idPedido`.
   - Never join `item_pedido.csv` directly with `pagamento_pedido.csv` without pre-aggregation, as doing so multiplies rows and inflates totals.
2. **Missing / Invalid Values:**
   - Null prices or invalid numbers default to `0.0`.
   - Malformed dates that cannot be parsed are excluded from temporal metrics and logged.
