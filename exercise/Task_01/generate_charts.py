import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Configure clean aesthetic
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

conn = sqlite3.connect('data/garden_shop.db')

# -------------------------------------------------------------
# Chart 1: Inventory Health by Category
# -------------------------------------------------------------
df_cat = pd.read_sql_query("""
SELECT 
    c.category_name,
    SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand = 0 THEN 1 ELSE 0 END) AS out_of_stock,
    SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand > 0 AND p.quantity_on_hand < p.reorder_level THEN 1 ELSE 0 END) AS low_stock,
    SUM(CASE WHEN p.discontinued = 0 AND p.quantity_on_hand >= p.reorder_level THEN 1 ELSE 0 END) AS healthy_stock
FROM categories c
LEFT JOIN products p ON c.category_id = p.category_id
GROUP BY c.category_id, c.category_name
ORDER BY (out_of_stock + low_stock) DESC, healthy_stock DESC;
""", conn)

fig, ax = plt.subplots(figsize=(8, 4.5), dpi=300)
categories = df_cat['category_name']
ax.bar(categories, df_cat['out_of_stock'], label='Out of Stock (Zero)', color='#d9534f', width=0.55)
ax.bar(categories, df_cat['low_stock'], bottom=df_cat['out_of_stock'], label='Below Reorder Level', color='#f0ad4e', width=0.55)
ax.bar(categories, df_cat['healthy_stock'], bottom=df_cat['out_of_stock'] + df_cat['low_stock'], label='Adequate / Healthy', color='#5cb85c', width=0.55)

ax.set_title('Product Inventory Health Status by Category', fontsize=13, fontweight='bold', pad=15, color='#2c3e50')
ax.set_ylabel('Number of Active Products (SKUs)', fontsize=10, fontweight='bold', color='#333333')
ax.set_xlabel('Product Category', fontsize=10, fontweight='bold', color='#333333', labelpad=10)
ax.set_xticklabels(categories, rotation=25, ha='right', fontsize=9)
ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.legend(frameon=True, facecolor='white', edgecolor='#e0e0e0', loc='upper right')
plt.tight_layout()
fig.savefig('exercise/Task_01/fig1_inventory_health_by_category.png')
plt.close(fig)
print("Saved fig1_inventory_health_by_category.png")

# -------------------------------------------------------------
# Chart 2: Priority Matrix: Stock Availability vs Sales Demand
# -------------------------------------------------------------
df_matrix = pd.read_sql_query("""
WITH sales AS (
    SELECT oi.product_id, SUM(oi.quantity) AS sold_qty
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
    COALESCE(s.sold_qty, 0) AS units_sold,
    CASE 
        WHEN p.discontinued = 1 THEN 'Discontinued'
        WHEN p.quantity_on_hand = 0 THEN 'P1: Stockout'
        WHEN p.quantity_on_hand < p.reorder_level AND COALESCE(s.sold_qty, 0) >= 4 THEN 'P1: Bestseller at Risk'
        WHEN p.quantity_on_hand < p.reorder_level THEN 'P2: Restock Needed'
        WHEN p.quantity_on_hand < p.reorder_level * 1.5 THEN 'P3: Watchlist'
        ELSE 'P5: Healthy Stock'
    END AS priority_tier
FROM products p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN sales s ON p.product_id = s.product_id;
""", conn)

fig, ax = plt.subplots(figsize=(8.5, 5), dpi=300)
color_map = {
    'P1: Stockout': '#d9534f',
    'P1: Bestseller at Risk': '#d9534f',
    'P2: Restock Needed': '#f0ad4e',
    'P3: Watchlist': '#337ab7',
    'P5: Healthy Stock': '#5cb85c',
    'Discontinued': '#999999'
}

for tier, group in df_matrix.groupby('priority_tier'):
    ax.scatter(group['units_sold'], group['quantity_on_hand'], 
               label=tier, color=color_map.get(tier, '#333333'), s=70, alpha=0.85, edgecolors='none')

# Annotate critical items
for _, row in df_matrix.iterrows():
    if row['priority_tier'] in ['P1: Stockout', 'P1: Bestseller at Risk', 'P2: Restock Needed']:
        ax.annotate(f"{row['product_name']}\n(Stock: {row['quantity_on_hand']})", 
                    (row['units_sold'], row['quantity_on_hand']),
                    textcoords="offset points", xytext=(8, -5), fontsize=8, fontweight='bold',
                    bbox=dict(boxstyle="round,pad=0.2", fc="yellow", alpha=0.3, ec="gray", lw=0.5))

ax.axhline(15, color='#e74c3c', linestyle='--', linewidth=1, alpha=0.6, label='Typical Reorder Threshold (~15)')
ax.set_title('Inventory Priority Matrix: Current Stock vs. Sales Velocity', fontsize=13, fontweight='bold', pad=15, color='#2c3e50')
ax.set_xlabel('Historical Units Sold (Excl. Cancelled)', fontsize=10, fontweight='bold', color='#333333')
ax.set_ylabel('Current Quantity on Hand (Units)', fontsize=10, fontweight='bold', color='#333333')
ax.legend(frameon=True, facecolor='white', edgecolor='#e0e0e0', loc='upper right')
plt.tight_layout()
fig.savefig('exercise/Task_01/fig2_priority_quadrant_matrix.png')
plt.close(fig)
print("Saved fig2_priority_quadrant_matrix.png")

# -------------------------------------------------------------
# Chart 3: Supplier Restock Capital Required & Deficit
# -------------------------------------------------------------
df_sup_restock = pd.read_sql_query("""
SELECT 
    s.supplier_name,
    COUNT(p.product_id) AS products_to_restock,
    SUM(p.reorder_level - p.quantity_on_hand) AS units_deficit,
    ROUND(SUM((p.reorder_level - p.quantity_on_hand) * p.cost), 2) AS capital_needed
FROM suppliers s
JOIN products p ON s.supplier_id = p.supplier_id
WHERE p.discontinued = 0 AND p.quantity_on_hand < p.reorder_level
GROUP BY s.supplier_name
ORDER BY capital_needed ASC;
""", conn)

fig, ax1 = plt.subplots(figsize=(8, 4), dpi=300)
y_pos = range(len(df_sup_restock))
bars = ax1.barh(y_pos, df_sup_restock['capital_needed'], color='#2b5797', height=0.45, label='Capital Required ($)')
ax1.set_yticks(y_pos)
ax1.set_yticklabels(df_sup_restock['supplier_name'], fontsize=9, fontweight='bold')
ax1.set_xlabel('Restock Capital to Minimum Reorder Point ($ USD)', fontsize=10, fontweight='bold', color='#2b5797')
ax1.set_title('Restocking Capital and Shortage Units by Supplier', fontsize=13, fontweight='bold', pad=15, color='#2c3e50')

# Add data labels
for i, bar in enumerate(bars):
    val = bar.get_width()
    units = df_sup_restock['units_deficit'].iloc[i]
    skus = df_sup_restock['products_to_restock'].iloc[i]
    ax1.text(val + 1.5, bar.get_y() + bar.get_height()/2, f"${val:.2f} ({units} units, {skus} SKU{'s' if skus>1 else ''})", 
             va='center', fontsize=8.5, fontweight='bold', color='#333333')

ax1.set_xlim(0, max(df_sup_restock['capital_needed']) * 1.35)
plt.tight_layout()
fig.savefig('exercise/Task_01/fig3_supplier_restock_capital.png')
plt.close(fig)
print("Saved fig3_supplier_restock_capital.png")

# -------------------------------------------------------------
# Chart 4: Capital Allocation by Category (Donut Chart)
# -------------------------------------------------------------
df_val_cat = pd.read_sql_query("""
SELECT 
    c.category_name,
    ROUND(SUM(p.quantity_on_hand * p.cost), 2) AS stock_cost_value
FROM categories c
JOIN products p ON c.category_id = p.category_id
WHERE p.discontinued = 0
GROUP BY c.category_name
ORDER BY stock_cost_value DESC;
""", conn)

fig, ax = plt.subplots(figsize=(6.5, 4.5), dpi=300)
colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#9467bd']
wedges, texts, autotexts = ax.pie(
    df_val_cat['stock_cost_value'], 
    labels=df_val_cat['category_name'],
    autopct='%1.1f%%',
    startangle=140,
    colors=colors[:len(df_val_cat)],
    wedgeprops=dict(width=0.45, edgecolor='white', linewidth=1.5),
    pctdistance=0.75,
    textprops=dict(fontsize=8.5)
)
for autotext in autotexts:
    autotext.set_fontsize(8)
    autotext.set_weight('bold')

ax.set_title('Active Inventory Capital Allocation by Category (Total: $4,731.00)', 
             fontsize=11.5, fontweight='bold', pad=12, color='#2c3e50')
plt.tight_layout()
fig.savefig('exercise/Task_01/fig4_inventory_capital_allocation.png')
plt.close(fig)
print("Saved fig4_inventory_capital_allocation.png")

conn.close()
