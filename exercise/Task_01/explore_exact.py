import sqlite3
import pandas as pd

conn = sqlite3.connect('data/garden_shop.db')

print("--- 1. ACTIVE PRODUCTS REQUIRING RESTOCK (quantity_on_hand < reorder_level) ---")
q1 = """
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
    (p.reorder_level - p.quantity_on_hand) AS deficit_units,
    (p.reorder_level - p.quantity_on_hand) * p.cost AS restock_cost_to_min,
    ROUND((p.price - p.cost) / p.price * 100, 1) AS margin_pct
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN suppliers s ON p.supplier_id = s.supplier_id
WHERE p.discontinued = 0 
  AND p.quantity_on_hand < p.reorder_level
ORDER BY p.quantity_on_hand ASC;
"""
print(pd.read_sql_query(q1, conn).to_string())

print("\n--- 2. CATEGORY BREAKDOWN (EXACT) ---")
q2 = """
SELECT 
    c.category_id,
    c.category_name,
    COUNT(p.product_id) AS total_products,
    SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand < p.reorder_level THEN 1 ELSE 0 END) AS products_below_reorder,
    SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand = 0 THEN 1 ELSE 0 END) AS zero_stock_products,
    SUM(CASE WHEN p.discontinued = 0 THEN p.quantity_on_hand ELSE 0 END) AS active_units_on_hand,
    ROUND(SUM(CASE WHEN p.discontinued = 0 THEN p.quantity_on_hand * p.cost ELSE 0 END), 2) AS stock_value_at_cost,
    ROUND(SUM(CASE WHEN p.discontinued = 0 THEN p.quantity_on_hand * p.price ELSE 0 END), 2) AS stock_value_at_retail
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_id, c.category_name
ORDER BY products_below_reorder DESC, stock_value_at_cost DESC;
"""
print(pd.read_sql_query(q2, conn).to_string())

print("\n--- 3. SUPPLIER BREAKDOWN (EXACT) ---")
q3 = """
SELECT 
    s.supplier_id,
    s.supplier_name,
    s.contact_email,
    s.state,
    COUNT(p.product_id) AS active_products_supplied,
    SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand < p.reorder_level THEN 1 ELSE 0 END) AS products_to_restock,
    SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand < p.reorder_level THEN (p.reorder_level - p.quantity_on_hand) ELSE 0 END) AS units_deficit,
    ROUND(SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand < p.reorder_level THEN (p.reorder_level - p.quantity_on_hand) * p.cost ELSE 0 END), 2) AS restock_capital_needed
FROM suppliers s
LEFT JOIN products p ON s.supplier_id = p.supplier_id AND p.discontinued = 0
GROUP BY s.supplier_id, s.supplier_name, s.contact_email, s.state
ORDER BY products_to_restock DESC, restock_capital_needed DESC;
"""
print(pd.read_sql_query(q3, conn).to_string())

print("\n--- 4. PRODUCT SALES VS INVENTORY (EXCLUDING CANCELLED) ---")
q4 = """
WITH sales_summary AS (
    SELECT 
        oi.product_id,
        SUM(oi.quantity) AS total_sold_units,
        SUM(oi.quantity * oi.unit_price) AS total_gross_revenue,
        COUNT(DISTINCT oi.order_id) AS order_occurrences
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    WHERE o.status != 'cancelled'
    GROUP BY oi.product_id
)
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    p.quantity_on_hand,
    p.reorder_level,
    p.discontinued,
    COALESCE(ss.total_sold_units, 0) AS total_sold_units,
    COALESCE(ss.total_gross_revenue, 0) AS total_gross_revenue,
    COALESCE(ss.order_occurrences, 0) AS order_occurrences,
    CASE 
        WHEN p.discontinued = 1 THEN 'Discontinued'
        WHEN p.quantity_on_hand = 0 THEN 'Stockout (0 units)'
        WHEN p.quantity_on_hand < p.reorder_level THEN 'Under Reorder Level'
        ELSE 'Healthy'
    END AS stock_health_status,
    CASE
        WHEN p.discontinued = 0 AND p.quantity_on_hand < p.reorder_level AND COALESCE(ss.total_sold_units, 0) >= 4 THEN 'P1 - High Urgency (Top Seller + Low Stock)'
        WHEN p.discontinued = 0 AND p.quantity_on_hand = 0 THEN 'P1 - Immediate Restock (Out of Stock)'
        WHEN p.discontinued = 0 AND p.quantity_on_hand < p.reorder_level THEN 'P2 - Restock Needed'
        WHEN p.discontinued = 0 AND p.quantity_on_hand < (p.reorder_level * 1.5) THEN 'P3 - Watchlist (Near Reorder)'
        WHEN p.discontinued = 1 THEN 'P4 - Discontinued (Do Not Restock)'
        ELSE 'P5 - Adequate Inventory'
    END AS management_priority
FROM products p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN sales_summary ss ON p.product_id = ss.product_id
ORDER BY 
    CASE 
        WHEN p.quantity_on_hand = 0 THEN 1
        WHEN p.quantity_on_hand < p.reorder_level THEN 2
        ELSE 3
    END,
    total_sold_units DESC;
"""
print(pd.read_sql_query(q4, conn).to_string())

conn.close()
