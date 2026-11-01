"""
data_loader.py - Data Access and Metric Calculation Engine for Garden Shop Task 02.
Enforces business rules:
- BR-001: Exclude cancelled orders (Order #17).
- BR-002: Exclude discontinued products from replenishment (Product #24).
- BR-003: Deduplicate balances by pre-aggregating sales before joining products.
- BR-004: Priority triage classification (P1 to P5).
"""

import sqlite3
import os
import json
import pandas as pd

DEFAULT_DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../../data/garden_shop.db')
)

def get_connection(db_path: str = None) -> sqlite3.Connection:
    path = db_path or DEFAULT_DB_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Database file not found at: {path}")
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def load_products_master(db_path: str = None) -> pd.DataFrame:
    """
    Loads master products DataFrame joined with categories, suppliers,
    and pre-aggregated sales data (strictly excluding cancelled orders).
    """
    conn = get_connection(db_path)
    query = """
    WITH valid_sales AS (
        -- Pre-aggregate order items to prevent Cartesian join balance duplication
        SELECT 
            oi.product_id,
            SUM(oi.quantity) AS units_sold,
            ROUND(SUM(oi.quantity * oi.unit_price), 2) AS gross_revenue,
            COUNT(DISTINCT oi.order_id) AS order_count
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        WHERE o.status != 'cancelled'  -- Rule BR-001: Exclude cancelled orders
        GROUP BY oi.product_id
    )
    SELECT 
        p.product_id,
        p.product_name,
        c.category_name,
        s.supplier_name,
        COALESCE(s.contact_email, '[NO EMAIL ON FILE]') AS contact_email,
        s.state AS supplier_state,
        p.price,
        p.cost,
        p.quantity_on_hand,
        p.reorder_level,
        p.discontinued,
        COALESCE(vs.units_sold, 0) AS units_sold,
        COALESCE(vs.gross_revenue, 0.0) AS gross_revenue,
        COALESCE(vs.order_count, 0) AS order_count,
        -- Deficit calculation (discontinued products always 0 per BR-002)
        CASE 
            WHEN p.discontinued = 1 THEN 0
            WHEN p.quantity_on_hand < p.reorder_level THEN (p.reorder_level - p.quantity_on_hand)
            ELSE 0 
        END AS deficit_to_min,
        -- Capital to min reorder level
        ROUND(CASE 
            WHEN p.discontinued = 1 THEN 0.0
            WHEN p.quantity_on_hand < p.reorder_level THEN (p.reorder_level - p.quantity_on_hand) * p.cost
            ELSE 0.0 
        END, 2) AS cost_to_min,
        -- Target Par Order (2x ROP)
        CASE 
            WHEN p.discontinued = 1 THEN 0
            WHEN p.quantity_on_hand < p.reorder_level THEN (p.reorder_level * 2 - p.quantity_on_hand)
            ELSE 0 
        END AS suggested_po_units,
        -- Target Par Order Cost
        ROUND(CASE 
            WHEN p.discontinued = 1 THEN 0.0
            WHEN p.quantity_on_hand < p.reorder_level THEN (p.reorder_level * 2 - p.quantity_on_hand) * p.cost
            ELSE 0.0 
        END, 2) AS suggested_po_cost,
        -- Profit Margin %
        ROUND((p.price - p.cost) / p.price * 100, 1) AS margin_pct,
        -- Priority Triage Classification
        CASE 
            WHEN p.discontinued = 1 THEN 'P4: Discontinued'
            WHEN p.quantity_on_hand = 0 THEN 'P1: Critical Stockout'
            WHEN p.quantity_on_hand < p.reorder_level AND COALESCE(vs.units_sold, 0) >= 4 THEN 'P1: Top Seller at Risk'
            WHEN p.quantity_on_hand < p.reorder_level THEN 'P2: Restock Required'
            WHEN p.quantity_on_hand < (p.reorder_level * 1.5) THEN 'P3: Watchlist'
            ELSE 'P5: Healthy'
        END AS priority_tier,
        -- Health Status Badge
        CASE 
            WHEN p.discontinued = 1 THEN 'Discontinued'
            WHEN p.quantity_on_hand = 0 THEN 'Out of Stock'
            WHEN p.quantity_on_hand < p.reorder_level THEN 'Low Stock'
            ELSE 'Healthy'
        END AS health_status
    FROM products p
    JOIN categories c ON p.category_id = c.category_id
    JOIN suppliers s ON p.supplier_id = s.supplier_id
    LEFT JOIN valid_sales vs ON p.product_id = vs.product_id
    ORDER BY 
        CASE 
            WHEN p.quantity_on_hand = 0 THEN 1
            WHEN p.quantity_on_hand < p.reorder_level AND COALESCE(vs.units_sold, 0) >= 4 THEN 2
            WHEN p.quantity_on_hand < p.reorder_level THEN 3
            WHEN p.discontinued = 1 THEN 5
            ELSE 4
        END,
        units_sold DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_kpi_summary(df_products: pd.DataFrame) -> dict:
    """
    Computes key performance indicators from master products DataFrame.
    """
    active_df = df_products[df_products['discontinued'] == 0]
    total_active = len(active_df)
    
    zero_stock = int((active_df['quantity_on_hand'] == 0).sum())
    understocked = int((active_df['quantity_on_hand'] < active_df['reorder_level']).sum())
    healthy = int((active_df['quantity_on_hand'] >= active_df['reorder_level']).sum())
    
    health_pct = round((healthy / total_active * 100), 1) if total_active > 0 else 0.0
    deficit_units = int(active_df['deficit_to_min'].sum()) if 'deficit_to_min' in active_df.columns else 0
    capital_needed = round(float(active_df['cost_to_min'].sum()), 2) if 'cost_to_min' in active_df.columns else 0.0
    target_po_capital = round(float(active_df['suggested_po_cost'].sum()), 2) if 'suggested_po_cost' in active_df.columns else 0.0
    
    active_cost_val = round(float((active_df['quantity_on_hand'] * active_df['cost']).sum()), 2) if 'cost' in active_df.columns else 0.0
    active_retail_val = round(float((active_df['quantity_on_hand'] * active_df['price']).sum()), 2) if 'price' in active_df.columns else 0.0
    
    # Revenue at risk: gross revenue of understocked items
    if 'gross_revenue' in active_df.columns and 'reorder_level' in active_df.columns:
        rev_at_risk = round(float(active_df[active_df['quantity_on_hand'] < active_df['reorder_level']]['gross_revenue'].sum()), 2)
    else:
        rev_at_risk = 0.0
    
    # Discontinued metrics
    disc_df = df_products[df_products['discontinued'] == 1]
    disc_cost_val = round(float((disc_df['quantity_on_hand'] * disc_df['cost']).sum()), 2) if 'cost' in disc_df.columns else 0.0
    disc_units = int(disc_df['quantity_on_hand'].sum()) if not disc_df.empty else 0
    
    return {
        "total_active_skus": total_active,
        "inventory_health_pct": health_pct,
        "healthy_skus": healthy,
        "critical_stockouts": zero_stock,
        "understocked_skus": understocked,
        "total_deficit_units": deficit_units,
        "capital_needed_to_rop": capital_needed,
        "target_po_capital": target_po_capital,
        "active_stock_cost_value": active_cost_val,
        "active_stock_retail_value": active_retail_val,
        "revenue_at_risk": rev_at_risk,
        "discontinued_skus": len(disc_df),
        "discontinued_units": disc_units,
        "discontinued_cost_value": disc_cost_val
    }

def export_json_payload(db_path: str = None, output_file: str = None) -> str:
    """Exports structured JSON for zero-server GitHub Pages execution.
    
    The generated payload includes a ``generated_at`` ISO-8601 timestamp so
    the dashboard can display when the data was last refreshed.
    """
    from datetime import datetime, timezone
    df_products = load_products_master(db_path)
    kpis = get_kpi_summary(df_products)
    
    # Categories aggregation
    active_df = df_products[df_products['discontinued'] == 0]
    cat_summary = active_df.groupby('category_name').agg(
        total_products=('product_id', 'count'),
        total_units=('quantity_on_hand', 'sum'),
        cost_value=('quantity_on_hand', lambda s: round(float((s * active_df.loc[s.index, 'cost']).sum()), 2)),
        out_of_stock=('quantity_on_hand', lambda s: int((s == 0).sum())),
        low_stock=('quantity_on_hand', lambda s: int(((s > 0) & (s < active_df.loc[s.index, 'reorder_level'])).sum())),
        healthy_stock=('quantity_on_hand', lambda s: int((s >= active_df.loc[s.index, 'reorder_level']).sum()))
    ).reset_index().to_dict(orient='records')
    
    # Suppliers aggregation
    sup_summary = active_df.groupby(['supplier_name', 'contact_email', 'supplier_state']).agg(
        active_skus_supplied=('product_id', 'count'),
        restock_skus=('deficit_to_min', lambda s: int((s > 0).sum())),
        units_deficit=('deficit_to_min', 'sum'),
        capital_needed=('cost_to_min', lambda s: round(float(s.sum()), 2))
    ).reset_index().to_dict(orient='records')
    
    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "kpis": kpis,
        "categories": cat_summary,
        "suppliers": sup_summary,
        "products": df_products.to_dict(orient='records')
    }
    
    out_path = output_file or os.path.join(os.path.dirname(__file__), 'dashboard_data.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)
    return out_path

if __name__ == '__main__':
    df = load_products_master()
    kpi = get_kpi_summary(df)
    print(f"Loaded {len(df)} products. Health: {kpi['inventory_health_pct']}%, Capital: ${kpi['capital_needed_to_rop']}")
    json_path = export_json_payload()
    print(f"Exported JSON payload to: {json_path}")
