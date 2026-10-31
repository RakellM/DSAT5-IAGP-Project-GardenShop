import sqlite3
import json
import os

def export_data():
    db_path = 'data/garden_shop.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 1. KPI Summary
    # Active inventory valuation
    cur.execute("""
    SELECT 
        COUNT(*) AS total_skus,
        SUM(CASE WHEN discontinued = 0 THEN 1 ELSE 0 END) AS active_skus,
        SUM(CASE WHEN discontinued = 1 THEN 1 ELSE 0 END) AS discontinued_skus,
        SUM(CASE WHEN discontinued = 0 THEN quantity_on_hand ELSE 0 END) AS active_units_on_hand,
        ROUND(SUM(CASE WHEN discontinued = 0 THEN quantity_on_hand * cost ELSE 0 END), 2) AS active_stock_cost_value,
        ROUND(SUM(CASE WHEN discontinued = 0 THEN quantity_on_hand * price ELSE 0 END), 2) AS active_stock_retail_value,
        ROUND(SUM(CASE WHEN discontinued = 1 THEN quantity_on_hand * cost ELSE 0 END), 2) AS discontinued_cost_value,
        SUM(CASE WHEN discontinued = 0 AND quantity_on_hand = 0 THEN 1 ELSE 0 END) AS zero_stock_skus,
        SUM(CASE WHEN discontinued = 0 AND quantity_on_hand < reorder_level THEN 1 ELSE 0 END) AS understocked_skus,
        SUM(CASE WHEN discontinued = 0 AND quantity_on_hand >= reorder_level THEN 1 ELSE 0 END) AS healthy_skus,
        SUM(CASE WHEN discontinued = 0 AND quantity_on_hand < reorder_level THEN (reorder_level - quantity_on_hand) ELSE 0 END) AS total_units_deficit,
        ROUND(SUM(CASE WHEN discontinued = 0 AND quantity_on_hand < reorder_level THEN (reorder_level - quantity_on_hand) * cost ELSE 0 END), 2) AS total_capital_to_rop,
        ROUND(SUM(CASE WHEN discontinued = 0 AND quantity_on_hand < reorder_level THEN (reorder_level * 2 - quantity_on_hand) * cost ELSE 0 END), 2) AS target_po_capital
    FROM products;
    """)
    kpi_raw = dict(cur.fetchone())
    kpi_raw['inventory_health_pct'] = round(kpi_raw['healthy_skus'] / kpi_raw['active_skus'] * 100, 1)
    kpi_raw['potential_margin_pct'] = round((kpi_raw['active_stock_retail_value'] - kpi_raw['active_stock_cost_value']) / kpi_raw['active_stock_retail_value'] * 100, 1)

    # Valid store sales performance (excluding cancelled order #17)
    cur.execute("""
    SELECT 
        COUNT(DISTINCT o.order_id) AS valid_orders,
        SUM(oi.quantity) AS total_units_sold,
        ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_gross_revenue,
        ROUND(SUM(oi.quantity * (oi.unit_price - p.cost)), 2) AS total_gross_profit,
        ROUND(SUM(oi.quantity * (oi.unit_price - p.cost)) / SUM(oi.quantity * oi.unit_price) * 100, 2) AS realized_margin_pct
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status != 'cancelled';
    """)
    sales_perf = dict(cur.fetchone())
    kpi_summary = {**kpi_raw, **sales_perf}

    # 2. Categories
    cur.execute("""
    SELECT 
        c.category_id,
        c.category_name,
        COUNT(p.product_id) AS total_products,
        SUM(CASE WHEN p.discontinued = 0 THEN p.quantity_on_hand ELSE 0 END) AS total_units,
        ROUND(SUM(CASE WHEN p.discontinued = 0 THEN p.quantity_on_hand * p.cost ELSE 0 END), 2) AS cost_value,
        ROUND(SUM(CASE WHEN p.discontinued = 0 THEN p.quantity_on_hand * p.price ELSE 0 END), 2) AS retail_value,
        SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand = 0 THEN 1 ELSE 0 END) AS out_of_stock,
        SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand > 0 AND p.quantity_on_hand < p.reorder_level THEN 1 ELSE 0 END) AS low_stock,
        SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand >= p.reorder_level THEN 1 ELSE 0 END) AS healthy_stock
    FROM categories c
    LEFT JOIN products p ON c.category_id = p.category_id
    GROUP BY c.category_id, c.category_name
    ORDER BY (out_of_stock + low_stock) DESC, cost_value DESC;
    """)
    categories = [dict(row) for row in cur.fetchall()]

    # 3. Suppliers
    cur.execute("""
    SELECT 
        s.supplier_id,
        s.supplier_name,
        COALESCE(s.contact_email, 'MISSING') AS contact_email,
        s.state,
        COUNT(p.product_id) AS active_skus_supplied,
        SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand < p.reorder_level THEN 1 ELSE 0 END) AS restock_skus,
        SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand < p.reorder_level THEN (p.reorder_level - p.quantity_on_hand) ELSE 0 END) AS units_deficit,
        ROUND(SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand < p.reorder_level THEN (p.reorder_level - p.quantity_on_hand) * p.cost ELSE 0 END), 2) AS capital_needed
    FROM suppliers s
    LEFT JOIN products p ON s.supplier_id = p.supplier_id AND p.discontinued = 0
    GROUP BY s.supplier_id, s.supplier_name, s.contact_email, s.state
    ORDER BY restock_skus DESC, capital_needed DESC;
    """)
    suppliers = [dict(row) for row in cur.fetchall()]

    # 4. Products with Sales & Prioritization
    cur.execute("""
    WITH sales_summary AS (
        SELECT 
            oi.product_id,
            SUM(oi.quantity) AS units_sold,
            ROUND(SUM(oi.quantity * oi.unit_price), 2) AS gross_revenue,
            COUNT(DISTINCT oi.order_id) AS order_count
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status != 'cancelled'
        GROUP BY oi.product_id
    )
    SELECT 
        p.product_id,
        p.product_name,
        c.category_name,
        s.supplier_name,
        COALESCE(s.contact_email, '') AS contact_email,
        p.price,
        p.cost,
        p.quantity_on_hand,
        p.reorder_level,
        p.discontinued,
        COALESCE(ss.units_sold, 0) AS units_sold,
        COALESCE(ss.gross_revenue, 0.0) AS gross_revenue,
        COALESCE(ss.order_count, 0) AS order_count,
        CASE 
            WHEN p.quantity_on_hand < p.reorder_level THEN (p.reorder_level - p.quantity_on_hand)
            ELSE 0 
        END AS deficit_to_min,
        ROUND(CASE 
            WHEN p.quantity_on_hand < p.reorder_level THEN (p.reorder_level - p.quantity_on_hand) * p.cost
            ELSE 0 
        END, 2) AS cost_to_min,
        CASE 
            WHEN p.quantity_on_hand < p.reorder_level THEN (p.reorder_level * 2 - p.quantity_on_hand)
            ELSE 0 
        END AS suggested_po_units,
        ROUND(CASE 
            WHEN p.quantity_on_hand < p.reorder_level THEN (p.reorder_level * 2 - p.quantity_on_hand) * p.cost
            ELSE 0 
        END, 2) AS suggested_po_cost,
        ROUND((p.price - p.cost) / p.price * 100, 1) AS margin_pct,
        CASE 
            WHEN p.discontinued = 1 THEN 'P4: Discontinued'
            WHEN p.quantity_on_hand = 0 THEN 'P1: Critical Stockout'
            WHEN p.quantity_on_hand < p.reorder_level AND COALESCE(ss.units_sold, 0) >= 4 THEN 'P1: Top Seller at Risk'
            WHEN p.quantity_on_hand < p.reorder_level THEN 'P2: Restock Required'
            WHEN p.quantity_on_hand < (p.reorder_level * 1.5) THEN 'P3: Watchlist'
            ELSE 'P5: Healthy'
        END AS priority_tier,
        CASE 
            WHEN p.discontinued = 1 THEN 'Discontinued'
            WHEN p.quantity_on_hand = 0 THEN 'Out of Stock'
            WHEN p.quantity_on_hand < p.reorder_level THEN 'Low Stock'
            ELSE 'Healthy'
        END AS health_status
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    JOIN suppliers s ON p.supplier_id = s.supplier_id
    LEFT JOIN sales_summary ss ON p.product_id = ss.product_id
    ORDER BY 
        CASE 
            WHEN p.quantity_on_hand = 0 THEN 1
            WHEN p.quantity_on_hand < p.reorder_level AND COALESCE(ss.units_sold, 0) >= 4 THEN 2
            WHEN p.quantity_on_hand < p.reorder_level THEN 3
            WHEN p.discontinued = 1 THEN 5
            ELSE 4
        END,
        units_sold DESC;
    """)
    products = [dict(row) for row in cur.fetchall()]

    payload = {
        "kpis": kpi_summary,
        "categories": categories,
        "suppliers": suppliers,
        "products": products,
        "generated_at": "2026-10-31T17:55:00Z"
    }

    out_path = os.path.join(os.path.dirname(__file__), 'dashboard_data.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)

    print(f"Data exported successfully to {out_path} ({len(products)} products, {len(categories)} categories, {len(suppliers)} suppliers)")

if __name__ == '__main__':
    export_data()
