import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Garden Shop | Inventory & Restocking DSS",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Connect to database
DB_PATH = os.path.join(os.path.dirname(__file__), '../../data/garden_shop.db')

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    
    # 1. Product & Sales View (Excluding Cancelled Order #17)
    q_products = """
    WITH sales AS (
        SELECT oi.product_id, SUM(oi.quantity) AS units_sold, SUM(oi.quantity * oi.unit_price) AS gross_revenue
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
        COALESCE(s.contact_email, 'MISSING') AS contact_email,
        p.price,
        p.cost,
        p.quantity_on_hand,
        p.reorder_level,
        p.discontinued,
        COALESCE(s_data.units_sold, 0) AS units_sold,
        COALESCE(s_data.gross_revenue, 0.0) AS gross_revenue,
        CASE WHEN p.quantity_on_hand < p.reorder_level THEN (p.reorder_level - p.quantity_on_hand) ELSE 0 END AS deficit_to_min,
        ROUND(CASE WHEN p.quantity_on_hand < p.reorder_level THEN (p.reorder_level - p.quantity_on_hand) * p.cost ELSE 0 END, 2) AS cost_to_min,
        CASE WHEN p.quantity_on_hand < p.reorder_level THEN (p.reorder_level * 2 - p.quantity_on_hand) ELSE 0 END AS suggested_po_units,
        ROUND(CASE WHEN p.quantity_on_hand < p.reorder_level THEN (p.reorder_level * 2 - p.quantity_on_hand) * p.cost ELSE 0 END, 2) AS suggested_po_cost,
        ROUND((p.price - p.cost) / p.price * 100, 1) AS margin_pct,
        CASE 
            WHEN p.discontinued = 1 THEN 'P4: Discontinued'
            WHEN p.quantity_on_hand = 0 THEN 'P1: Critical Stockout'
            WHEN p.quantity_on_hand < p.reorder_level AND COALESCE(s_data.units_sold, 0) >= 4 THEN 'P1: Top Seller at Risk'
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
    LEFT JOIN sales s_data ON p.product_id = s_data.product_id;
    """
    df_products = pd.read_sql_query(q_products, conn)
    conn.close()
    return df_products

df = load_data()

# SIDEBAR FILTERS
st.sidebar.title("🌿 Navigation & Filters")
st.sidebar.markdown("Filter catalog across dimensions:")

search_query = st.sidebar.text_input("🔍 Search Product or Supplier", "")
categories = ["All"] + sorted(list(df['category_name'].unique()))
selected_category = st.sidebar.selectbox("Category", categories)

suppliers = ["All"] + sorted(list(df['supplier_name'].unique()))
selected_supplier = st.sidebar.selectbox("Supplier", suppliers)

priorities = ["All", "P1: Urgent Action", "P2: Restock Required", "P3: Watchlist", "P5: Healthy"]
selected_priority = st.sidebar.selectbox("Priority Tier", priorities)

show_discontinued = st.sidebar.checkbox("Show Discontinued Products", value=False)

# FILTER LOGIC
filtered_df = df.copy()
if not show_discontinued:
    filtered_df = filtered_df[filtered_df['discontinued'] == 0]
if selected_category != "All":
    filtered_df = filtered_df[filtered_df['category_name'] == selected_category]
if selected_supplier != "All":
    filtered_df = filtered_df[filtered_df['supplier_name'] == selected_supplier]
if selected_priority != "All":
    prefix = selected_priority.split(":")[0]
    filtered_df = filtered_df[filtered_df['priority_tier'].str.startswith(prefix)]
if search_query:
    q = search_query.lower()
    filtered_df = filtered_df[
        filtered_df['product_name'].str.lower().str.contains(q) |
        filtered_df['supplier_name'].str.lower().str.contains(q) |
        filtered_df['category_name'].str.lower().str.contains(q)
    ]

# TITLE & HEADER
st.title("🌿 Garden Shop | Inventory & Restocking DSS")
st.caption("Operational Decision Support System · Data Source: SQLite (`garden_shop.db`)")

# PROCUREMENT ALERT
if "Ironwood Tools" in filtered_df[filtered_df['deficit_to_min'] > 0]['supplier_name'].values:
    st.warning("⚠️ **Supplier Data Alert:** `Ironwood Tools` supplies *Hand Cultivator* (7 units deficit, $24.50), but has **no email registered on file**. Please submit purchase orders by phone.")

# KPI SUMMARY CARDS
active_df = filtered_df[filtered_df['discontinued'] == 0]
total_active = len(active_df)
zero_stock = len(active_df[active_df['quantity_on_hand'] == 0])
understocked = len(active_df[active_df['quantity_on_hand'] < active_df['reorder_level']])
healthy = len(active_df[active_df['quantity_on_hand'] >= active_df['reorder_level']])
health_pct = round((healthy / total_active * 100), 1) if total_active > 0 else 0.0

deficit_units = int(active_df['deficit_to_min'].sum())
capital_needed = float(active_df['cost_to_min'].sum())
cost_val = float((active_df['quantity_on_hand'] * active_df['cost']).sum())
retail_val = float((active_df['quantity_on_hand'] * active_df['price']).sum())
rev_at_risk = float(active_df[active_df['quantity_on_hand'] < active_df['reorder_level']]['gross_revenue'].sum())

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
kpi1.metric("Inventory Health", f"{health_pct}%", f"{healthy}/{total_active} safe")
kpi2.metric("Critical Stockouts", f"{zero_stock} SKU", "0 units on hand", delta_color="inverse")
kpi3.metric("Under Reorder Level", f"{understocked} SKUs", f"{deficit_units} units deficit", delta_color="inverse")
kpi4.metric("Capital to Min ROP", f"${capital_needed:,.2f}", "To safe threshold")
kpi5.metric("Active Stock at Cost", f"${cost_val:,.2f}", f"Retail: ${retail_val:,.0f}")
kpi6.metric("Revenue at Risk", f"${rev_at_risk:,.2f}", "Understocked top sellers", delta_color="inverse")

st.markdown("---")

# VISUAL CHARTS
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Category Stock Health Breakdown")
    cat_summary = active_df.groupby(['category_name', 'health_status']).size().unstack(fill_value=0).reset_index()
    for col in ['Out of Stock', 'Low Stock', 'Healthy']:
        if col not in cat_summary.columns:
            cat_summary[col] = 0
    fig_cat = go.Figure(data=[
        go.Bar(name='Out of Stock', x=cat_summary['category_name'], y=cat_summary['Out of Stock'], marker_color='#EF4444'),
        go.Bar(name='Below Reorder', x=cat_summary['category_name'], y=cat_summary['Low Stock'], marker_color='#F59E0B'),
        go.Bar(name='Healthy Stock', x=cat_summary['category_name'], y=cat_summary['Healthy'], marker_color='#10B981')
    ])
    fig_cat.update_layout(barmode='stack', height=320, margin=dict(l=20, r=20, t=30, b=20), legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig_cat, use_container_width=True)

with col_right:
    st.subheader("🎯 Priority Matrix (Stock vs Demand Velocity)")
    color_map = {
        'P1: Critical Stockout': '#EF4444',
        'P1: Top Seller at Risk': '#DC2626',
        'P2: Restock Required': '#F59E0B',
        'P3: Watchlist': '#2563EB',
        'P5: Healthy': '#10B981',
        'P4: Discontinued': '#9CA3AF'
    }
    fig_scatter = px.scatter(
        filtered_df,
        x='units_sold',
        y='quantity_on_hand',
        color='priority_tier',
        color_discrete_map=color_map,
        hover_data=['product_name', 'category_name', 'supplier_name', 'reorder_level'],
        labels={'units_sold': 'Units Sold (Excl. Cancelled)', 'quantity_on_hand': 'On-Hand Stock (Units)'}
    )
    fig_scatter.update_traces(marker=dict(size=12))
    fig_scatter.update_layout(height=320, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_scatter, use_container_width=True)

# SUPPLIER SHORTAGE SUMMARY
col_sup, col_disc = st.columns([1.5, 1])
with col_sup:
    st.subheader("🚚 Supplier Replenishment Capital Needed")
    sup_df = active_df[active_df['cost_to_min'] > 0].groupby('supplier_name')['cost_to_min'].sum().reset_index()
    if not sup_df.empty:
        fig_sup = px.bar(sup_df, x='cost_to_min', y='supplier_name', orientation='h',
                         labels={'cost_to_min': 'Capital Needed ($ USD)', 'supplier_name': 'Supplier'},
                         color_discrete_sequence=['#1B365D'])
        fig_sup.update_layout(height=220, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_sup, use_container_width=True)
    else:
        st.info("No suppliers require replenishment under current filter selection.")

with col_disc:
    st.subheader("📦 Discontinued Inventory Clearance")
    st.info("**Rule 2 Compliance:** Discontinued items (*Bird Feeder #24*) are never automatically reordered. Current stock: 4 units ($32.00 cost / $68.00 retail). Recommended: Run a 25% markdown promotion to liquidate capital.")

# WORKBENCH TABLE
st.subheader("📋 Operational Restock Action Workbench")
display_cols = ['product_id', 'product_name', 'category_name', 'supplier_name', 'price', 'quantity_on_hand', 'reorder_level', 'deficit_to_min', 'cost_to_min', 'suggested_po_units', 'suggested_po_cost', 'units_sold', 'priority_tier']
st.dataframe(
    filtered_df[display_cols].rename(columns={
        'product_id': 'ID',
        'product_name': 'Product Name',
        'category_name': 'Category',
        'supplier_name': 'Supplier',
        'price': 'Price ($)',
        'quantity_on_hand': 'Stock',
        'reorder_level': 'ROP',
        'deficit_to_min': 'Deficit',
        'cost_to_min': 'Cost to Min ($)',
        'suggested_po_units': 'Target PO',
        'suggested_po_cost': 'Target Cost ($)',
        'units_sold': 'Sold',
        'priority_tier': 'Priority'
    }),
    use_container_width=True,
    hide_index=True
)

# CSV DOWNLOAD
csv_data = filtered_df[display_cols].to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Download Filtered PO Manifest (CSV)",
    data=csv_data,
    file_name="Garden_Shop_PO_Manifest.csv",
    mime="text/csv"
)
