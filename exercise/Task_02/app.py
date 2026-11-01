import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

# Import our verified data loader
from data_loader import load_products_master, get_kpi_summary

st.set_page_config(
    page_title="Garden Shop | Inventory & Restocking DSS (Task 02)",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data using cached function
@st.cache_data
def get_data():
    return load_products_master()

df = get_data()

# -------------------------------------------------------------
# SIDEBAR FILTERS (Multi-dimensional)
# -------------------------------------------------------------
st.sidebar.title("🌿 Garden Shop DSS")
st.sidebar.markdown("**Interactive Inventory Controls**")

search_term = st.sidebar.text_input("🔍 Search Product or Supplier", "")

category_list = ["All Categories"] + sorted(list(df['category_name'].unique()))
selected_category = st.sidebar.selectbox("Filter by Category", category_list)

supplier_list = ["All Suppliers"] + sorted(list(df['supplier_name'].unique()))
selected_supplier = st.sidebar.selectbox("Filter by Supplier", supplier_list)

priority_options = ["All Priorities", "P1: Critical Stockout / Bestseller at Risk", "P2: Restock Required", "P3: Watchlist", "P5: Healthy"]
selected_priority = st.sidebar.selectbox("Filter by Priority Tier", priority_options)

show_discontinued = st.sidebar.checkbox("Show Discontinued Products (Bird Feeder)", value=False)

# -------------------------------------------------------------
# FILTER LOGIC
# -------------------------------------------------------------
filtered_df = df.copy()

if not show_discontinued:
    filtered_df = filtered_df[filtered_df['discontinued'] == 0]

if selected_category != "All Categories":
    filtered_df = filtered_df[filtered_df['category_name'] == selected_category]

if selected_supplier != "All Suppliers":
    filtered_df = filtered_df[filtered_df['supplier_name'] == selected_supplier]

if selected_priority != "All Priorities":
    prefix = selected_priority.split(":")[0]
    filtered_df = filtered_df[filtered_df['priority_tier'].str.startswith(prefix)]

if search_term:
    q = search_term.lower().strip()
    filtered_df = filtered_df[
        filtered_df['product_name'].str.lower().str.contains(q) |
        filtered_df['supplier_name'].str.lower().str.contains(q) |
        filtered_df['category_name'].str.lower().str.contains(q)
    ]

# -------------------------------------------------------------
# MAIN HEADER & PROCUREMENT ALERT
# -------------------------------------------------------------
st.title("🌿 Garden Shop | Inventory & Restocking Intelligence")
st.caption("Operational Decision Support System · Verified Data Layer (`data_loader.py`) · Preserves Original Data")

# Alert for Ironwood Tools missing email
if "Ironwood Tools" in filtered_df[filtered_df['deficit_to_min'] > 0]['supplier_name'].values:
    st.warning("⚠️ **Procurement Alert:** `Ironwood Tools` supplies *Hand Cultivator* (7 units deficit, $24.50), but has **no email registered on file**. Purchase orders must be placed by telephone.")

# -------------------------------------------------------------
# KPI SCORECARD
# -------------------------------------------------------------
kpis = get_kpi_summary(filtered_df)

c1, c2, c3, c4, c5, c6 = st.columns(6)
c1.metric(
    "Inventory Health Index", 
    f"{kpis['inventory_health_pct']}%", 
    f"{kpis['healthy_skus']}/{kpis['total_active_skus']} safe",
    delta_color="normal" if kpis['inventory_health_pct'] >= 90 else "inverse"
)
c2.metric(
    "Critical Stockouts", 
    f"{kpis['critical_stockouts']} SKU", 
    "0 units on hand", 
    delta_color="inverse"
)
c3.metric(
    "Under Reorder Point", 
    f"{kpis['understocked_skus']} SKUs", 
    f"{kpis['total_deficit_units']} units deficit", 
    delta_color="inverse"
)
c4.metric(
    "Capital to Min ROP", 
    f"${kpis['capital_needed_to_rop']:,.2f}", 
    f"Target PO: ${kpis['target_po_capital']:,.0f}"
)
c5.metric(
    "Active Stock at Cost", 
    f"${kpis['active_stock_cost_value']:,.2f}", 
    f"Retail: ${kpis['active_stock_retail_value']:,.0f}"
)
c6.metric(
    "Revenue at Risk", 
    f"${kpis['revenue_at_risk']:,.2f}", 
    "Understocked top sellers", 
    delta_color="inverse"
)

st.markdown("---")

# -------------------------------------------------------------
# VISUAL DIAGNOSTICS (Stacked Bar & Scatter Matrix)
# -------------------------------------------------------------
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("📊 Category Stock Health Breakdown")
    if not filtered_df.empty:
        active_cat = filtered_df[filtered_df['discontinued'] == 0]
        cat_agg = active_cat.groupby(['category_name', 'health_status']).size().unstack(fill_value=0).reset_index()
        for col in ['Out of Stock', 'Low Stock', 'Healthy']:
            if col not in cat_agg.columns:
                cat_agg[col] = 0
        fig_cat = go.Figure(data=[
            go.Bar(name='Out of Stock (Zero)', x=cat_agg['category_name'], y=cat_agg['Out of Stock'], marker_color='#EF4444'),
            go.Bar(name='Below Reorder Point', x=cat_agg['category_name'], y=cat_agg['Low Stock'], marker_color='#F59E0B'),
            go.Bar(name='Adequate Stock', x=cat_agg['category_name'], y=cat_agg['Healthy'], marker_color='#10B981')
        ])
        fig_cat.update_layout(barmode='stack', height=330, margin=dict(l=20, r=20, t=30, b=20), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig_cat, use_container_width=True)
    else:
        st.info("No categories match current filters.")

with col_chart2:
    st.subheader("🎯 Priority Matrix: Current Stock vs. Sales Velocity")
    if not filtered_df.empty:
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
            hover_data=['product_name', 'category_name', 'supplier_name', 'reorder_level', 'deficit_to_min'],
            labels={'units_sold': 'Units Sold (Excl. Cancelled)', 'quantity_on_hand': 'Current Stock on Hand'}
        )
        fig_scatter.update_traces(marker=dict(size=12))
        fig_scatter.update_layout(height=330, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("No products match current filters.")

# -------------------------------------------------------------
# SUPPLIER REPLENISHMENT & DISCONTINUED CLEARANCE
# -------------------------------------------------------------
col_sup, col_disc = st.columns([1.6, 1])

with col_sup:
    st.subheader("🚚 Supplier Replenishment Capital Breakdown")
    sup_reorder = filtered_df[(filtered_df['discontinued'] == 0) & (filtered_df['cost_to_min'] > 0)].groupby('supplier_name')['cost_to_min'].sum().reset_index()
    if not sup_reorder.empty:
        fig_sup = px.bar(
            sup_reorder,
            x='cost_to_min',
            y='supplier_name',
            orientation='h',
            labels={'cost_to_min': 'Restock Capital to Min ROP ($ USD)', 'supplier_name': 'Supplier'},
            color_discrete_sequence=['#1B365D']
        )
        fig_sup.update_layout(height=220, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig_sup, use_container_width=True)
    else:
        st.info("All products from selected suppliers currently meet safe inventory levels.")

with col_disc:
    st.subheader("📦 Discontinued Inventory Clearance")
    st.info("**Rule BR-002 Compliance:** Discontinued items (*Bird Feeder #24*) are never automatically reordered. Current stock: 4 units ($32.00 cost / $68.00 retail). Recommended: Run a 25% markdown promotion to liquidate capital.")

# -------------------------------------------------------------
# OPERATIONAL RESTOCK ACTION WORKBENCH (DATA GRID)
# -------------------------------------------------------------
st.subheader("📋 Operational Restock Action Workbench")
st.caption(f"Displaying {len(filtered_df)} items matching active filter criteria")

display_cols = [
    'product_id', 'product_name', 'category_name', 'supplier_name', 
    'price', 'cost', 'quantity_on_hand', 'reorder_level', 
    'deficit_to_min', 'cost_to_min', 'suggested_po_units', 
    'units_sold', 'priority_tier'
]

if not filtered_df.empty:
    st.dataframe(
        filtered_df[display_cols].rename(columns={
            'product_id': 'ID',
            'product_name': 'Product Name',
            'category_name': 'Category',
            'supplier_name': 'Supplier',
            'price': 'Price ($)',
            'cost': 'Cost ($)',
            'quantity_on_hand': 'Stock',
            'reorder_level': 'ROP',
            'deficit_to_min': 'Deficit Units',
            'cost_to_min': 'Cost to Min ROP ($)',
            'suggested_po_units': 'Target PO Units',
            'units_sold': 'Units Sold',
            'priority_tier': 'Priority Tier'
        }),
        use_container_width=True,
        hide_index=True
    )

    # 1-Click CSV Download
    csv_bytes = filtered_df[display_cols].to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered PO Manifest (CSV)",
        data=csv_bytes,
        file_name="Garden_Shop_PO_Manifest_Task02.csv",
        mime="text/csv"
    )
else:
    st.warning("No products match the selected filter criteria. Try resetting filters or expanding search.")
