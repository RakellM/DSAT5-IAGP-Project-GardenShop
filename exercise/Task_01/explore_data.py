import sqlite3
import pandas as pd

conn = sqlite3.connect('data/garden_shop.db')

print("=== TABLE COUNTS ===")
for t in ['customers', 'products', 'categories', 'orders', 'order_items', 'suppliers']:
    cnt = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"{t}: {cnt} rows")

print("\n=== ORDER STATUSES ===")
df_orders = pd.read_sql_query("SELECT status, COUNT(*) as count FROM orders GROUP BY status", conn)
print(df_orders)

print("\n=== CANCELLED ORDERS & ITEMS ===")
df_cancelled = pd.read_sql_query("""
SELECT o.order_id, o.status, oi.product_id, p.product_name, oi.quantity, oi.unit_price
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id
WHERE o.status = 'cancelled'
""", conn)
print(df_cancelled)

print("\n=== DISCONTINUED PRODUCTS ===")
df_disc = pd.read_sql_query("""
SELECT product_id, product_name, quantity_on_hand, reorder_level, discontinued
FROM products
WHERE discontinued = 1 OR discontinued = 'true' OR discontinued = 'TRUE'
""", conn)
print(df_disc)

print("\n=== PRODUCTS STOCK STATUS (ALL PRODUCTS) ===")
df_stock = pd.read_sql_query("""
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    s.supplier_name,
    p.price,
    p.cost,
    p.quantity_on_hand,
    p.reorder_level,
    p.discontinued,
    (p.quantity_on_hand - p.reorder_level) as stock_diff,
    (p.quantity_on_hand * p.cost) as stock_value_cost,
    CASE 
        WHEN p.discontinued = 1 THEN 'Discontinued'
        WHEN p.quantity_on_hand = 0 THEN 'Out of Stock (Zero)'
        WHEN p.quantity_on_hand < p.reorder_level THEN 'Critical Low Stock'
        WHEN p.quantity_on_hand = p.reorder_level THEN 'At Reorder Point'
        ELSE 'Adequate Stock'
    END as inventory_status
FROM products p
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN suppliers s ON p.supplier_id = s.supplier_id
ORDER BY p.discontinued ASC, p.quantity_on_hand ASC
""", conn)
print(df_stock.to_string())

print("\n=== TOTAL STOCK VALUE (ACTIVE VS DISCONTINUED) ===")
df_val = pd.read_sql_query("""
SELECT 
    CASE WHEN discontinued = 1 THEN 'Discontinued' ELSE 'Active' END as product_type,
    COUNT(*) as total_items,
    SUM(quantity_on_hand) as total_units,
    SUM(quantity_on_hand * cost) as total_cost_value,
    SUM(quantity_on_hand * price) as total_retail_value
FROM products
GROUP BY discontinued
""", conn)
print(df_val)

print("\n=== SALES VOLUME BY PRODUCT (EXCLUDING CANCELLED ORDERS) ===")
df_sales = pd.read_sql_query("""
SELECT 
    p.product_id,
    p.product_name,
    c.category_name,
    p.quantity_on_hand,
    p.reorder_level,
    p.discontinued,
    SUM(CASE WHEN o.status != 'cancelled' THEN oi.quantity ELSE 0 END) as valid_units_sold,
    SUM(CASE WHEN o.status != 'cancelled' THEN oi.quantity * oi.unit_price ELSE 0 END) as valid_revenue,
    SUM(CASE WHEN o.status = 'cancelled' THEN oi.quantity ELSE 0 END) as cancelled_units
FROM products p
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.order_id
GROUP BY p.product_id, p.product_name, c.category_name, p.quantity_on_hand, p.reorder_level, p.discontinued
ORDER BY valid_units_sold DESC
""", conn)
print(df_sales.to_string())

print("\n=== CATEGORY ANALYSIS (RESTOCK NEED & VALUE) ===")
df_cat = pd.read_sql_query("""
SELECT 
    c.category_name,
    COUNT(p.product_id) as total_products,
    SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand <= p.reorder_level THEN 1 ELSE 0 END) as needs_restock_count,
    SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand = 0 THEN 1 ELSE 0 END) as out_of_stock_count,
    SUM(p.quantity_on_hand) as current_stock_units,
    SUM(p.quantity_on_hand * p.cost) as stock_cost_value,
    SUM(CASE WHEN o.status != 'cancelled' THEN oi.quantity ELSE 0 END) as total_units_sold
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
LEFT JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN orders o ON oi.order_id = o.order_id
GROUP BY c.category_name
ORDER BY needs_restock_count DESC, out_of_stock_count DESC
""", conn)
print(df_cat.to_string())

print("\n=== SUPPLIER ANALYSIS (RESTOCK NEED) ===")
df_sup = pd.read_sql_query("""
SELECT 
    s.supplier_name,
    s.contact_email,
    s.state,
    COUNT(p.product_id) as total_supplied_products,
    SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand <= p.reorder_level THEN 1 ELSE 0 END) as products_needing_restock,
    SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand < p.reorder_level THEN (p.reorder_level - p.quantity_on_hand) ELSE 0 END) as shortage_units_deficit,
    SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand < p.reorder_level THEN (p.reorder_level - p.quantity_on_hand) * p.cost ELSE 0 END) as estimated_reorder_cost
FROM suppliers s
LEFT JOIN products p ON s.supplier_id = p.supplier_id
GROUP BY s.supplier_id, s.supplier_name, s.contact_email, s.state
ORDER BY products_needing_restock DESC
""", conn)
print(df_sup.to_string())
conn.close()
