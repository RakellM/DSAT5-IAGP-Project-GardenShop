import sqlite3
import pandas as pd

conn = sqlite3.connect('data/garden_shop.db')

# 1. Total stock value
print("--- STOCK VALUE SUMMARY ---")
df_stock_summary = pd.read_sql_query("""
SELECT 
    CASE WHEN discontinued = 1 THEN 'Discontinued' ELSE 'Active' END AS status,
    COUNT(*) AS sku_count,
    SUM(quantity_on_hand) AS total_units,
    ROUND(SUM(quantity_on_hand * cost), 2) AS total_cost,
    ROUND(SUM(quantity_on_hand * price), 2) AS total_retail,
    ROUND(SUM(quantity_on_hand * (price - cost)), 2) AS potential_gross_profit,
    ROUND(SUM(quantity_on_hand * (price - cost)) / SUM(quantity_on_hand * price) * 100, 2) AS gross_margin_pct
FROM products
GROUP BY discontinued;
""", conn)
print(df_stock_summary)

# 2. Restock details
print("\n--- RESTOCK DEFICIT DETAILS ---")
df_restock = pd.read_sql_query("""
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    s.supplier_name,
    s.contact_email,
    p.price,
    p.cost,
    p.quantity_on_hand,
    p.reorder_level,
    (p.reorder_level - p.quantity_on_hand) AS deficit_to_min,
    ROUND((p.reorder_level - p.quantity_on_hand) * p.cost, 2) AS cost_to_min,
    -- Recommended restock to 2x reorder level for safety stock
    (p.reorder_level * 2 - p.quantity_on_hand) AS suggested_order_qty,
    ROUND((p.reorder_level * 2 - p.quantity_on_hand) * p.cost, 2) AS suggested_order_cost
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN suppliers s ON p.supplier_id = s.supplier_id
WHERE p.discontinued = 0 AND p.quantity_on_hand < p.reorder_level
ORDER BY p.quantity_on_hand ASC;
""", conn)
print(df_restock)

# 3. Overall Sales Velocity
print("\n--- SALES VELOCITY (EXCLUDING CANCELLED) ---")
df_sales = pd.read_sql_query("""
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    p.quantity_on_hand,
    p.reorder_level,
    COALESCE(SUM(oi.quantity), 0) AS units_sold,
    COALESCE(ROUND(SUM(oi.quantity * oi.unit_price), 2), 0) AS revenue_sold,
    COALESCE(ROUND(SUM(oi.quantity * (oi.unit_price - p.cost)), 2), 0) AS profit_sold,
    COUNT(DISTINCT oi.order_id) AS distinct_orders
FROM products p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.order_id AND o.status != 'cancelled'
WHERE p.discontinued = 0
GROUP BY p.product_id, p.product_name, c.category_name, p.quantity_on_hand, p.reorder_level
ORDER BY units_sold DESC;
""", conn)
print(df_sales)

# 4. Total Store Sales Performance
print("\n--- STORE TOTAL PERFORMANCE ---")
df_store_perf = pd.read_sql_query("""
SELECT 
    COUNT(DISTINCT o.order_id) AS total_valid_orders,
    SUM(oi.quantity) AS total_units_sold,
    ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue,
    ROUND(SUM(oi.quantity * (oi.unit_price - p.cost)), 2) AS total_gross_profit,
    ROUND(SUM(oi.quantity * (oi.unit_price - p.cost)) / SUM(oi.quantity * oi.unit_price) * 100, 2) AS realized_gross_margin_pct
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status != 'cancelled';
""", conn)
print(df_store_perf)

conn.close()
