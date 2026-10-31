import os
import sys
import sqlite3
import pandas as pd

# Add local python-docx to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'pylib'))
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

print("Starting generation of comprehensive proposal docx...")

conn = sqlite3.connect('data/garden_shop.db')
doc = docx.Document()

# -------------------------------------------------------------
# PAGE SETUP & STYLES
# -------------------------------------------------------------
for s in doc.sections:
    s.top_margin = Inches(0.85)
    s.bottom_margin = Inches(0.85)
    s.left_margin = Inches(0.85)
    s.right_margin = Inches(0.85)
    s.page_width = Inches(8.5)
    s.page_height = Inches(11.0)

# Colors
COLOR_NAVY = RGBColor(27, 54, 93)       # #1B365D - Primary Executive Navy
COLOR_SLATE = RGBColor(46, 107, 158)    # #2E6B9E - Secondary Slate
COLOR_AMBER = RGBColor(217, 130, 43)    # #D9822B - Accent Warm Amber
COLOR_CHARCOAL = RGBColor(44, 62, 80)   # #2C3E50 - Dark Body Text
COLOR_MUTED = RGBColor(110, 110, 110)
COLOR_WHITE = RGBColor(255, 255, 255)

HEX_NAVY = "1B365D"
HEX_SLATE = "2E6B9E"
HEX_LIGHT_BLUE = "EBF3FA"
HEX_ROW_ALT = "F8F9FA"
HEX_AMBER_BG = "FEF9E7"
HEX_RED_BG = "FDEDEC"
HEX_GREEN_BG = "EAFAF1"
HEX_BORDER = "D3D3D3"

# Configure Normal Style
normal_style = doc.styles['Normal']
normal_style.font.name = 'Calibri'
normal_style.font.size = Pt(9.5)
normal_style.font.color.rgb = COLOR_CHARCOAL

# Styling Helpers
def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('shd'):
            tcPr.remove(child)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=90, bottom=90, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_header(text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.bold = True
    if level == 1:
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(5)
        run.font.size = Pt(14)
        run.font.color.rgb = COLOR_NAVY
    elif level == 2:
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(3)
        run.font.size = Pt(11.5)
        run.font.color.rgb = COLOR_SLATE
    elif level == 3:
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        run.font.size = Pt(10)
        run.font.color.rgb = COLOR_CHARCOAL
    return p

def add_p(text, bold_prefix="", space_after=4, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(9.5)
        r_pre.bold = True
        r_pre.font.color.rgb = COLOR_NAVY
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(9.5)
    r.italic = italic
    r.font.color.rgb = COLOR_CHARCOAL
    return p

def add_bullet(text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(9.5)
        r_pre.bold = True
        r_pre.font.color.rgb = COLOR_NAVY
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(9.5)
    r.font.color.rgb = COLOR_CHARCOAL
    return p

def add_callout(text, title="STRATEGIC INSIGHT", alert_type="info"):
    colors = {
        "info": ("1B365D", HEX_LIGHT_BLUE),
        "warning": ("D9822B", HEX_AMBER_BG),
        "danger": ("C0392B", HEX_RED_BG),
        "success": ("27AE60", HEX_GREEN_BG)
    }
    border_color, fill_color = colors.get(alert_type, ("1B365D", HEX_LIGHT_BLUE))
    
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_background(cell, fill_color)
    set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="32" w:space="0" w:color="{border_color}"/>
            <w:top w:val="none"/>
            <w:right w:val="none"/>
            <w:bottom w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    
    run_t = p.add_run(f"[{title}] ")
    run_t.bold = True
    run_t.font.name = 'Calibri'
    run_t.font.size = Pt(9)
    run_t.font.color.rgb = RGBColor.from_string(border_color)
    
    run_body = p.add_run(text)
    run_body.font.name = 'Calibri'
    run_body.font.size = Pt(9)
    run_body.font.color.rgb = RGBColor(40, 40, 40)
    
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(3)

def format_table(table, col_widths, headers, data, alignments=None):
    set_table_borders(table)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    # Header row
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        hdr_cells[i].width = Inches(col_widths[i])
        set_cell_background(hdr_cells[i], HEX_NAVY)
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=90, right=90)
        p = hdr_cells[i].paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        if alignments:
            p.alignment = alignments[i]
        r = p.add_run(h)
        r.font.name = 'Calibri'
        r.font.size = Pt(8)
        r.bold = True
        r.font.color.rgb = COLOR_WHITE
        
    # Data rows
    for r_idx, row_data in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        fill_hex = HEX_ROW_ALT if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            row_cells[c_idx].width = Inches(col_widths[c_idx])
            set_cell_background(row_cells[c_idx], fill_hex)
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=90, right=90)
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            if alignments:
                p.alignment = alignments[c_idx]
            r = p.add_run(str(val))
            r.font.name = 'Calibri'
            r.font.size = Pt(8)
            r.font.color.rgb = COLOR_CHARCOAL
            
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(4)

# -------------------------------------------------------------
# TITLE & COVER BANNER
# -------------------------------------------------------------
title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(10)
title_p.paragraph_format.space_after = Pt(2)
r_title = title_p.add_run("EXECUTIVE PROPOSAL & SPECIFICATION BLUEPRINT:\nINTERACTIVE INVENTORY MONITORING & RESTOCKING DECISION SUPPORT SYSTEM")
r_title.bold = True
r_title.font.name = 'Calibri'
r_title.font.size = Pt(16)
r_title.font.color.rgb = COLOR_NAVY

sub_p = doc.add_paragraph()
sub_p.paragraph_format.space_before = Pt(0)
sub_p.paragraph_format.space_after = Pt(12)
r_sub = sub_p.add_run("Operational Intelligence, Demand Velocity Analysis, and Strategic Purchasing Framework for Garden Shop E-Commerce")
r_sub.font.name = 'Calibri'
r_sub.font.size = Pt(11)
r_sub.font.color.rgb = COLOR_SLATE

# Meta Table
meta_table = doc.add_table(rows=4, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_headers = ["Project Deliverable", "Task 01 - Interactive Inventory Dashboard Proposal"]
meta_data = [
    ["Target Database", "Garden Shop Relational Database (data/garden_shop.db - SQLite 3, 6 Tables, 130 Records)"],
    ["Intended Audience", "Executive Leadership, Operations Director, Warehouse & Merchandising Managers"],
    ["Analytical Version & Status", "Version 1.0 (Production-Ready Technical Specification & Empirical Audit)"]
]
format_table(meta_table, [2.2, 4.6], meta_headers, meta_data)

# -------------------------------------------------------------
# SECTION 1: EXECUTIVE SUMMARY & STRATEGIC BUSINESS OBJECTIVE
# -------------------------------------------------------------
add_header("1. Executive Summary & Strategic Business Objective", level=1)

add_p("An online retail business specializing in gardening supplies, houseplants, seeds, and outdoor tools faces a classical operational dilemma in inventory management: balancing customer order fulfillment against working capital lockup. Currently, operations staff experience substantial friction identifying which SKUs require immediate replenishment, evaluating stock adequacy against customer purchase frequency, and managing supplier ordering workflows. This document presents an exhaustive, data-grounded dashboard proposal engineered to transform the Garden Shop's operational decision-making.")

add_header("1.1 Core Mission & Value Proposition", level=2)
add_p("The proposed Interactive Inventory & Restocking Decision Support System (DSS) will serve as the single source of truth for inventory health, stock depletion risks, and supplier procurement actions. The system bridges raw transactional records and strategic warehouse execution by delivering:")
add_bullet("Transforming static inventory levels into dynamic stockout risk tiers (P1 Urgent to P5 Healthy) based on sales velocity and safety thresholds.", "Automated Inventory Triage: ")
add_bullet("Calculating exact unit replenishment deficits and required purchasing capital to prevent stockouts while preventing over-ordering.", "Capital Optimization: ")
add_bullet("Aggregating purchase order line items by vendor, highlighting supplier communication bottlenecks, and consolidating order logistics.", "Supplier Purchasing Orchestration: ")
add_bullet("Enforcing automated segregation of cancelled transactions and non-replenishable discontinued lines.", "Business Rule Compliance: ")

add_header("1.2 Direct Resolution of Core Management Inquiries", level=2)
add_p("Based on empirical SQL audit of the provided dataset (data/garden_shop.db), the dashboard directly resolves the seven core operational inquiries defined by executive leadership:")

q_answers = [
    ["Q1: Products below recommended reorder level?", "Exactly 5 active SKUs are currently below their safety reorder thresholds: Hanging Basket (Pots & Planters), Hand Cultivator (Tools), Tomato Seeds 'Roma' (Seeds & Bulbs), Orchid Food (Fertilizer), and Pothos 'Golden' (Houseplants). Note: Discontinued SKU #24 (Bird Feeder) is below reorder point (4 on hand vs 6 reorder) but is strictly filtered out per business rules."],
    ["Q2: Products with zero or critically low stock?", "1 SKU has ZERO stock (Stockout): Hanging Basket (0 units on hand vs. 10 reorder level). 4 SKUs have critically depleted stock: Tomato Seeds 'Roma' (5 on hand vs 40 reorder level - extreme 35-unit shortage), Hand Cultivator (3 on hand vs 10 reorder level), Orchid Food (6 vs 10), and Pothos 'Golden' (8 vs 12)."],
    ["Q3: High-volume sellers requiring availability protection?", "Top volume drivers are Sunflower Seeds (12 units sold, 200 on hand), Terracotta Pot 8in (9 units sold, 90 on hand), and a cluster of high-demand items with 5 units sold each (Fiddle-Leaf Fig, Monstera, Snake Plant, Pothos 'Golden', Tulip Bulbs, Potting Soil 20L, Compost Mix 10L). CRITICAL ALERT: Pothos 'Golden' (5 units sold) and Tomato Seeds 'Roma' (4 units sold) are top-tier bestsellers actively operating below safety reorder points!"],
    ["Q4: Categories concentrating restock needs?", "Restock requirements are distributed across 5 categories (1 SKU each). However, operational impact is highly uneven: Pots & Planters contains the store's ONLY zero-stockout item; Seeds & Bulbs represents 58.3% of the total unit deficit (35 units shortage); and Houseplants contains the highest revenue-generating understocked item (Pothos 'Golden') and holds 37% of active inventory capital."],
    ["Q5: Estimated value of available stock at cost?", "Total Active Inventory Value at Registered Cost is $4,731.00 (933 physical units across 23 active SKUs), with a potential retail value of $10,321.25 (overall potential gross profit of $5,590.25; 54.16% gross margin). Discontinued inventory accounts for $32.00 at cost (4 units of Bird Feeder; $68.00 retail value). Total warehouse inventory is $4,763.00 (937 physical units)."],
    ["Q6: Products requiring priority management monitoring?", "A 5-tier triage priority matrix classifies products into actionable queues: Priority 1 (P1 - Urgent Action: Hanging Basket [Stockout], Pothos 'Golden' [Top Seller Deficit], Tomato Seeds 'Roma' [Top Seller Deficit]); Priority 2 (P2 - Restock Scheduled: Hand Cultivator, Orchid Food); Priority 3 (P3 - Watchlist / Near Reorder: Solar Lantern, Fiddle-Leaf Fig, Cactus Mix Soil); Priority 4 (P4 - Discontinued Liquidation: Bird Feeder); Priority 5 (P5 - Healthy Stock: 15 SKUs)."],
    ["Q7: Suppliers associated with products needing restock?", "4 of the 6 registered suppliers require active purchase orders: Terra Pots Co (Hanging Basket - 10 units deficit, $60.00 capital); SunGrow Nurseries (Pothos 'Golden' & Orchid Food - 8 units deficit, $36.00 capital); Bloomfield Seeds (Tomato Seeds 'Roma' - 35 units deficit, $31.50 capital); and Ironwood Tools (Hand Cultivator - 7 units deficit, $24.50 capital). CRITICAL RISK: Ironwood Tools has NO email address on file!"]
]

t_q_ans = doc.add_table(rows=8, cols=2)
format_table(t_q_ans, [2.3, 4.5], ["Management Inquiry", "Data-Grounded Empirical Finding & Resolution"], q_answers)

add_callout("The store faces an immediate capital requirement of only $152.00 to eliminate all active stockouts and bring the 5 at-risk products back to their minimum safety reorder thresholds. The primary operational failure is not capital constraint, but lack of visibility and timely purchase order execution.", "KEY STRATEGIC TAKEAWAY", "warning")

# -------------------------------------------------------------
# SECTION 2: EMPIRICAL EXPLORATORY DATA ANALYSIS (EDA)
# -------------------------------------------------------------
add_header("2. Empirical Exploratory Data Analysis & Baseline Audit", level=1)
add_p("To ensure the proposed dashboard is grounded in operational reality rather than theoretical abstraction, a comprehensive SQL audit of data/garden_shop.db was executed. The dataset encompasses 6 relational tables containing 130 records.")

add_header("2.1 Inventory Health & Capital Valuation Baseline", level=2)
add_p("The catalog consists of 24 unique products across 8 categories, supplied by 6 vendors. Of these, 23 products are active and 1 product is discontinued. The active stock represents 933 physical units with an aggregate replacement cost of $4,731.00 and retail market value of $10,321.25.")

# Table: Category breakdown
cat_summary_data = [
    ["Houseplants", "5", "1", "0", "147", "$1,747.00", "$3,374.00", "37.0%"],
    ["Seeds & Bulbs", "3", "1", "0", "325", "$664.50", "$1,673.75", "14.0%"],
    ["Soil & Compost", "3", "0", "0", "143", "$599.00", "$1,365.00", "12.7%"],
    ["Tools", "3", "1", "0", "81", "$448.50", "$990.00", "9.5%"],
    ["Pots & Planters", "3", "1", "1", "112", "$401.00", "$1,003.00", "8.5%"],
    ["Watering", "2", "0", "0", "45", "$351.00", "$780.00", "7.4%"],
    ["Fertilizer", "2", "1", "0", "46", "$264.00", "$594.00", "5.6%"],
    ["Outdoor Decor", "3", "0", "0", "34", "$256.00", "$541.50", "5.4%"],
    ["TOTAL (Active)", "23", "5", "1", "933", "$4,731.00", "$10,321.25", "100.0%"]
]
t_cat_sum = doc.add_table(rows=10, cols=8)
align_r = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT]
format_table(t_cat_sum, [1.4, 0.6, 0.7, 0.7, 0.7, 0.9, 0.9, 0.9], 
             ["Category", "SKUs", "Below ROP", "Zero Stock", "Units", "Cost Value", "Retail Value", "Share (%)"], 
             cat_summary_data, align_r)

if os.path.exists('exercise/Task_01/fig4_inventory_capital_allocation.png'):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture('exercise/Task_01/fig4_inventory_capital_allocation.png', width=Inches(5.5))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 1: Active Inventory Capital Allocation by Category (Total Warehouse Cost: $4,731.00)")
    r_cap.italic = True
    r_cap.font.size = Pt(8.5)
    r_cap.font.color.rgb = COLOR_MUTED

add_header("2.2 Deep-Dive Restocking Diagnostic (The 5 Understocked SKUs)", level=2)
add_p("A strict filter evaluating active products where quantity_on_hand < reorder_level identifies exactly 5 SKUs requiring immediate purchasing attention:")

restock_table_data = [
    ["#14", "Hanging Basket", "Pots & Planters", "Terra Pots Co", "$14.00", "$6.00", "0", "10", "10", "$60.00", "20", "$120.00", "P1 (Stockout)"],
    ["#11", "Hand Cultivator", "Tools", "Ironwood Tools", "$8.00", "$3.50", "3", "10", "7", "$24.50", "17", "$59.50", "P2 (Low Stock)"],
    ["#7", "Tomato Seeds 'Roma'", "Seeds & Bulbs", "Bloomfield Seeds", "$2.75", "$0.90", "5", "40", "35", "$31.50", "75", "$67.50", "P1 (Top Seller)"],
    ["#20", "Orchid Food", "Fertilizer", "SunGrow Nurseries", "$9.00", "$4.00", "6", "10", "4", "$16.00", "14", "$56.00", "P2 (Low Stock)"],
    ["#4", "Pothos 'Golden'", "Houseplants", "SunGrow Nurseries", "$12.00", "$5.00", "8", "12", "4", "$20.00", "16", "$80.00", "P1 (Top Seller)"],
    ["TOTAL", "5 Products", "5 Categories", "4 Suppliers", "--", "--", "22", "82", "60", "$152.00", "142", "$383.00", "--"]
]
t_restock_det = doc.add_table(rows=7, cols=13)
format_table(t_restock_det, [0.35, 1.1, 0.9, 0.9, 0.45, 0.45, 0.4, 0.4, 0.4, 0.55, 0.4, 0.55, 0.75],
             ["ID", "Product Name", "Category", "Supplier", "Price", "Cost", "Stock", "ROP", "Deficit", "Cost to ROP", "Target PO", "Target Cost", "Priority"],
             restock_table_data)

add_callout("Product #14 (Hanging Basket) has zero units in stock. It has 0 recorded sales because customers cannot purchase an unavailable item. The system must flag this as an active stockout rather than a low-velocity SKU. Furthermore, Tomato Seeds 'Roma' is 87.5% below its safety reorder point (deficit of 35 units).", "CRITICAL STOCKOUT & SHORTAGE ALERT", "danger")

add_header("2.3 Sales Demand Velocity & Pipeline Verification", level=2)
add_p("The database contains 24 customer orders across 20 registered customers spanning January 15, 2024 to June 14, 2024. A rigorous evaluation of order statuses reveals:")
add_bullet("17 orders (70.8%) successfully fulfilled and delivered, representing 66 units sold and $863.00 in gross revenue.", "Shipped Orders: ")
add_bullet("6 orders (25.0%) representing 20 units and $244.00 in confirmed customer demand currently moving through warehouse fulfillment.", "Processing (3) & Pending (3): ")
add_bullet("1 order (Order #17 - customer #9, placed 2024-04-03) containing 1 unit of Pruning Shears (product #9, $22.00). In accordance with core business rules, this order is completely excluded from sales velocity, gross revenue, and restock prioritization.", "Cancelled Order (1): ")

add_p("Across all 23 valid orders, total demand reached 86 units, generating $1,107.00 in total revenue and $583.00 in realized gross profit (52.66% realized gross margin). Evaluating individual product sales volumes confirms that the top volume leaders are Sunflower Seeds (12 units) and Terracotta Pot 8in (9 units), followed by an 8-way tie at 5 units sold. Alarmingly, Pothos 'Golden' (5 units sold) and Tomato Seeds 'Roma' (4 units sold) are in the top volume decile yet severely depleted in stock.")

add_header("2.4 Supplier Fulfillment & Channel Exposure", level=2)
add_p("Purchasing operations rely on 6 regional suppliers. A cross-tabulation of supplier catalog assignments and current stock health indicates significant vendor concentration:")

sup_table_data = [
    ["Terra Pots Co", "OH", "hello@terrapots.example", "6", "1", "10", "$60.00", "Hanging Basket (#14 - Stockout)"],
    ["SunGrow Nurseries", "FL", "sales@sungrow.example", "4", "2", "8", "$36.00", "Pothos 'Golden' (#4) & Orchid Food (#20)"],
    ["Bloomfield Seeds", "OR", "contact@bloomfield.example", "3", "1", "35", "$31.50", "Tomato Seeds 'Roma' (#7)"],
    ["Ironwood Tools", "PA", "[MISSING - NO EMAIL]", "4", "1", "7", "$24.50", "Hand Cultivator (#11)"],
    ["GreenLeaf Wholesale", "CA", "orders@greenleaf.example", "6", "0", "0", "$0.00", "Fully Stocked (Fiddle-Leaf Fig, Monstera, ZZ, etc.)"],
    ["RootWorks Supply", "PA", "[MISSING - NO EMAIL]", "0", "0", "0", "$0.00", "Inactive (0 assigned products in catalog)"]
]
t_sup = doc.add_table(rows=7, cols=8)
format_table(t_sup, [1.3, 0.45, 1.4, 0.45, 0.5, 0.5, 0.7, 1.5],
             ["Supplier Name", "State", "Contact Email", "SKUs", "Restock", "Deficit", "Capital", "Affected SKUs & Operational Notes"],
             sup_table_data)

if os.path.exists('exercise/Task_01/fig3_supplier_restock_capital.png'):
    p_img = doc.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture('exercise/Task_01/fig3_supplier_restock_capital.png', width=Inches(5.8))
    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap = p_cap.add_run("Figure 2: Supplier Restock Capital Requirements and Replenishment Unit Deficits")
    r_cap.italic = True
    r_cap.font.size = Pt(8.5)
    r_cap.font.color.rgb = COLOR_MUTED

add_callout("Ironwood Tools supplies Hand Cultivator (#11) which needs restocking, but has NO contact email registered. Operations cannot transmit automated purchase orders. The dashboard must display a prominent operational alert prompting staff to update supplier credentials.", "SUPPLIER DATA QUALITY RISK", "danger")

# -------------------------------------------------------------
# SECTION 3: AI BRAINSTORMING & CRITICAL EVALUATION
# -------------------------------------------------------------
add_header("3. AI Brainstorming, Critical Evaluation & Trade-off Analysis", level=1)
add_p("In alignment with the core assignment objectives, artificial intelligence was leveraged during the design phase to brainstorm potential indicators, visualizations, and advanced analytics. Crucially, each AI suggestion was subjected to rigorous empirical evaluation against business pertinence, computational viability, and database constraints.")

add_header("3.1 Evaluation Matrix of AI Suggestions", level=2)
add_p("The following evaluation matrix documents the proposed analytical features, their evaluation against the available schema, and the final architectural decision:")

ai_eval_data = [
    ["Dynamic Safety Stock / Lead Time ROP", "Calculate dynamic Reorder Points (ROP = d * L + z * sigma_L) based on supplier transit variation.", "REJECTED", "The database lacks supplier delivery lead times and stock movement dates. Implementing dynamic ROP would require fabricated assumptions, producing dangerous false precision."],
    ["ML Time-Series Sales Forecasting", "Deploy Prophet/ARIMA to forecast SKU demand 30 days forward using order timestamps.", "REJECTED", "Dataset contains only 24 orders across 5 months (~0.16 orders/day). Statistical time-series algorithms fail on ultra-sparse data, risking massive over-fitting."],
    ["Economic Order Quantity (EOQ) Optimization", "Calculate mathematical batch size minimizing annual holding cost vs. fixed order cost.", "DEFERRED", "Requires annual holding cost percentage (H) and fixed order placement cost (S), neither of which exist in the schema. Replaced with heuristic Par-Level multiplier (2x ROP)."],
    ["Stock-to-Sales Velocity Ratio & Matrix", "Plot Current Stock against Sales Volume on a 4-quadrant scatter chart to isolate high-risk SKUs.", "ADOPTED", "Highly viable. Immediately distinguishes Bestsellers at Risk from Healthy Surplus, giving operations intuitive visual prioritization."],
    ["Multi-Tier Operational Triage (P1-P5)", "Categorize inventory into 5 distinct action tiers combining stockout status, ROP gap, and sales volume.", "ADOPTED", "Provides clear decision rules for purchasing staff rather than presenting an undifferentiated list of numbers."],
    ["Supplier PO Rollup & Data Alerting", "Aggregate required reorder units and capital by vendor, highlighting missing contact emails.", "ADOPTED", "Directly addresses purchasing workflow bottlenecks and exposes data governance issues (Ironwood Tools missing email)."]
]
t_ai_eval = doc.add_table(rows=7, cols=4)
format_table(t_ai_eval, [1.4, 2.3, 0.8, 2.3],
             ["AI Feature Suggestion", "Proposed Analytical Capability", "Decision", "Critical Evaluation & Business Rationale"],
             ai_eval_data)

add_header("3.2 Deep Justification of Rejected Proposals", level=2)
add_p("A critical responsibility in business analytics is knowing what NOT to build. Incorporating unviable algorithms creates deceptive artifacts that erode operational trust:")
add_bullet("Why Dynamic Reorder Points Were Rejected: Theoretical inventory models dictate that safety stock depends on demand variance during supplier lead time. However, garden_shop.db contains neither supplier lead times nor delivery history. Attempting to calculate dynamic ROP by hallucinating lead times would misguide purchasing staff and compromise warehouse reliability.", "Rejection 1 - Dynamic ROP: ")
add_bullet("Why Predictive Time-Series Models Were Rejected: 24 customer transactions over 152 days represent extreme data sparsity. Machine learning models require hundreds of regular seasonal observations to extract signal from noise. Applying forecasting algorithms here would produce arbitrary trend lines disguised as advanced AI.", "Rejection 2 - Machine Learning Demand Forecasting: ")
add_bullet("Why Classical EOQ Was Deferred: EOQ requires quantifiable holding costs (capital cost of money, warehouse rent, insurance, spoilage) and administrative PO processing costs. In their absence, a practical 2x Reorder Level replenishment heuristic provides immediate, robust safety buffering.", "Rejection 3 - Theoretical EOQ: ")

# -------------------------------------------------------------
# SECTION 4: KEY PERFORMANCE INDICATORS (KPIS)
# -------------------------------------------------------------
add_header("4. Key Performance Indicators (KPIs) & Information Architecture", level=1)
add_p("The dashboard organizes indicators into three logical tiers: Strategic Executive KPIs (warehouse capital and health overview), Operational Triage Metrics (immediate reorder urgency), and Commercial Risk Indicators (revenue exposure).")

kpi_catalog_data = [
    ["Inventory Health Index", "% of active SKUs meeting or exceeding their safety reorder level.", "COUNT(Active SKUs >= ROP) / COUNT(Active SKUs)", "78.3%", "> 90.0%", "Primary barometer of overall catalog fulfillment readiness."],
    ["Stockout SKU Count", "Number of active products with zero physical units in stock.", "COUNT(Active SKUs where Stock = 0)", "1 SKU", "0 SKUs", "Immediate operational failure indicator (Hanging Basket #14)."],
    ["SKUs Below Reorder Level", "Active products requiring replenishment purchase orders.", "COUNT(Active SKUs where Stock < ROP)", "5 SKUs", "0 SKUs", "Core reorder queue size for purchasing specialists."],
    ["Replenishment Capital Needed", "Total cost required to bring all understocked SKUs back to ROP.", "SUM((ROP - Stock) * Cost) for Stock < ROP", "$152.00", "$0.00", "Immediate working capital required for warehouse procurement."],
    ["Active Stock Value at Cost", "Total acquisition cost of active physical inventory on hand.", "SUM(Stock * Cost) for Active SKUs", "$4,731.00", "Monitored", "Total warehouse working capital committed to active catalog."],
    ["Potential Retail Valuation", "Expected gross revenue from full sell-through of current stock.", "SUM(Stock * Price) for Active SKUs", "$10,321.25", "Monitored", "Maximum gross revenue potential of current on-hand units."],
    ["Catalog Gross Margin %", "Potential gross profit margin across active warehouse inventory.", "SUM(Stock * (Price - Cost)) / SUM(Stock * Price)", "54.16%", "> 50.0%", "Commercial profitability baseline of inventory investments."],
    ["Revenue at Immediate Risk", "Gross revenue generated by SKUs currently below reorder point.", "SUM(Sold Units * Price) for Understocked SKUs", "$71.00", "$0.00", "Measures financial downside of imminent stockouts (Pothos, Roma)."],
    ["Discontinued Capital Lockup", "Warehouse capital trapped in discontinued products.", "SUM(Stock * Cost) for Discontinued SKUs", "$32.00", "$0.00", "Identifies stagnant capital requiring liquidation (Bird Feeder #24)."]
]
t_kpi_cat = doc.add_table(rows=10, cols=6)
format_table(t_kpi_cat, [1.4, 1.8, 1.6, 0.6, 0.6, 1.8],
             ["Metric Name", "Business Definition", "SQL Formulation", "Current", "Target", "Operational Rationale"],
             kpi_catalog_data)

# -------------------------------------------------------------
# SECTION 5: DASHBOARD ARCHITECTURE & USER EXPERIENCE
# -------------------------------------------------------------
add_header("5. Dashboard Visual Layout, User Interface & Interactions", level=1)
add_p("The dashboard employs a 3-Tier Progressive Disclosure Architecture designed to guide users from high-level strategic awareness down to transactional execution without cognitive overload.")

add_header("5.1 Conceptual Wireframe Blueprint", level=2)
add_p("The user interface layout is structured as follows:")

wireframe_text = """
+----------------------------------------------------------------------------------------------------+
|  GARDEN SHOP | INVENTORY MONITORING & RESTOCKING DECISION SUPPORT SYSTEM             [Status: LIVE] |
+----------------------------------------------------------------------------------------------------+
| FILTERS: [Category: All (8)]  [Supplier: All (6)]  [Health: All]  [Show Discontinued: OFF] [RESET] |
+----------------------------------------------------------------------------------------------------+
|  [ INVENTORY HEALTH ]  |  [ ACTIVE STOCKOUTS ]  |  [ UNDER REORDER ]  |  [ REORDER CAPITAL ]       |
|         78.3%          |        1 SKU           |       5 SKUs        |       $152.00              |
|  Target: >90% (AMBER)  |   Hanging Basket (RED) |  Deficit: 60 Units  |  Target PO: $383.00        |
+----------------------------------------------------------------------------------------------------+
|  [ TOTAL ACTIVE COST ] |  [ RETAIL POTENTIAL ]  |  [ REALIZED MARGIN ]|  [ REVENUE AT RISK ]       |
|       $4,731.00        |      $10,321.25        |       52.66%        |        $71.00              |
|  933 Physical Units    |  Potential Margin: 54% |  Gross Profit: $583 |  Pothos & Tomato Seeds     |
+----------------------------------------------------------------------------------------------------+
| CHART 1: INVENTORY HEALTH BY CATEGORY            | CHART 2: PRIORITY SCATTER MATRIX                |
| (Stacked Bar: Out of Stock | Low | Healthy)      | (Current Stock vs. Valid Units Sold)            |
| [Embedded Figure 3 below]                        | [Embedded Figure 4 below]                       |
+--------------------------------------------------+-------------------------------------------------+
| CHART 3: SUPPLIER REORDER CAPITAL & SHORTAGE     | COMPONENT 4: DISCONTINUED CLEARANCE DRAWER      |
| (Horizontal Bar: Capital by Vendor)              | Bird Feeder (#24) - 4 Units ($32 Cost / $68 Ret)|
| [Embedded Figure 2 above]                        | Recommended Action: Run 25% Promo to Liquidate  |
+----------------------------------------------------------------------------------------------------+
| COMPONENT 5: OPERATIONAL RESTOCK ACTION WORKBENCH (Interactive Data Grid)                          |
| [P1-RED] #14 Hanging Basket     | Terra Pots Co     | Stock: 0  | ROP: 10 | Deficit: 10 | [$60.00] [PO]|
| [P1-RED] #4  Pothos 'Golden'    | SunGrow Nurseries | Stock: 8  | ROP: 12 | Deficit:  4 | [$20.00] [PO]|
| [P1-RED] #7  Tomato Seeds 'Roma'| Bloomfield Seeds  | Stock: 5  | ROP: 40 | Deficit: 35 | [$31.50] [PO]|
| [P2-AMB] #11 Hand Cultivator    | Ironwood Tools    | Stock: 3  | ROP: 10 | Deficit:  7 | [$24.50] [PO]|
| [P2-AMB] #20 Orchid Food        | SunGrow Nurseries | Stock: 6  | ROP: 10 | Deficit:  4 | [$16.00] [PO]|
+----------------------------------------------------------------------------------------------------+
"""
p_wire = doc.add_paragraph()
r_wire = p_wire.add_run(wireframe_text)
r_wire.font.name = 'Consolas'
r_wire.font.size = Pt(7)
r_wire.font.color.rgb = COLOR_NAVY

add_header("5.2 Analytical Visualizations", level=2)
add_p("The visual layer features two primary diagnostic charts that instantly communicate stock concentration and operational urgency:")

if os.path.exists('exercise/Task_01/fig1_inventory_health_by_category.png'):
    p_img1 = doc.add_paragraph()
    p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture('exercise/Task_01/fig1_inventory_health_by_category.png', width=Inches(5.8))
    p_cap1 = doc.add_paragraph()
    p_cap1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap1 = p_cap1.add_run("Figure 3: Product Inventory Health Distribution across Categories")
    r_cap1.italic = True
    r_cap1.font.size = Pt(8.5)
    r_cap1.font.color.rgb = COLOR_MUTED

if os.path.exists('exercise/Task_01/fig2_priority_quadrant_matrix.png'):
    p_img2 = doc.add_paragraph()
    p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_picture('exercise/Task_01/fig2_priority_quadrant_matrix.png', width=Inches(5.8))
    p_cap2 = doc.add_paragraph()
    p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cap2 = p_cap2.add_run("Figure 4: Inventory Priority Matrix: Current Stock vs. Historical Sales Velocity")
    r_cap2.italic = True
    r_cap2.font.size = Pt(8.5)
    r_cap2.font.color.rgb = COLOR_MUTED

add_header("5.3 Interactive Filters & Slicers", level=2)
add_bullet("Allows filtering the entire dashboard by single or multiple categories to assess department-level health.", "Category Multi-Select: ")
add_bullet("Isolates orders and replenishment actions by specific vendor to streamline purchasing meetings and PO creation.", "Supplier Filter: ")
add_bullet("Enables 1-click filtering for 'Out of Stock Only', 'Below Reorder Point', 'Watchlist', or 'Healthy'.", "Stock Health Slicer: ")
add_bullet("Defaults to OFF in restock views (preventing accidental reorders) and ON in inventory audit views to monitor capital clearance.", "Discontinued Toggle: ")

# -------------------------------------------------------------
# SECTION 6: BUSINESS RULES & CALCULATION LOGIC
# -------------------------------------------------------------
add_header("6. Business Rules, Cleansing Logic & Algorithmic Definitions", level=1)
add_p("To safeguard data integrity, the dashboard enforces strict business rules at the SQL ingestion and transformation layers:")

add_header("6.1 Handling of Order Statuses & Cancelled Orders", level=2)
add_p("The database records 4 order statuses: shipped, processing, pending, and cancelled. A core business requirement states that cancelled orders must not be treated as effective sales.")
add_bullet("Order #17 was cancelled by customer #9 on April 3, 2024. It contains 1 unit of Pruning Shears (product #9) at $22.00. The reporting layer enforces a strict predicate: WHERE orders.status != 'cancelled'. This prevents artificial inflation of sales volume, gross revenue, and depletion velocity.", "Cancellation Filtration: ")
add_bullet("Orders in 'processing' (3 orders, 11 units) and 'pending' (3 orders, 9 units) represent valid, committed customer demand that has not yet shipped. They are included in historical sales velocity and committed warehouse allocation.", "Pipeline Demand Treatment: ")

add_header("6.2 Governance of Discontinued SKUs", level=2)
add_p("Product #24 (Bird Feeder) is marked discontinued = 1. It currently holds 4 physical units in warehouse storage, which is below its legacy reorder level of 6.")
add_bullet("Discontinued products are programmatically excluded from all automated replenishment queues, PO recommendations, and supplier deficit calculations (WHERE products.discontinued = 0).", "Restock Exclusion: ")
add_bullet("Discontinued SKUs are routed to a dedicated 'Clearance & Liquidation Drawer'. Management is presented with an action recommendation to discount the item by 25-30% to liquidate the $32.00 of locked capital.", "Liquidation Routing: ")

add_header("6.3 Multi-Tier Restock Priority Algorithm", level=2)
add_p("The dashboard classifies all catalog items into 5 operational tiers using an explicit decision-tree algorithm:")
add_p("Priority = CASE\n  WHEN discontinued = 1 THEN 'P4: Discontinued (Do Not Restock)'\n  WHEN quantity_on_hand = 0 THEN 'P1: Critical Stockout (Immediate PO)'\n  WHEN quantity_on_hand < reorder_level AND total_sold_units >= 4 THEN 'P1: Top Seller at Risk (Immediate PO)'\n  WHEN quantity_on_hand < reorder_level THEN 'P2: Restock Required (Standard PO)'\n  WHEN quantity_on_hand < (reorder_level * 1.5) THEN 'P3: Watchlist (Near Threshold)'\n  ELSE 'P5: Healthy Inventory'\nEND", italic=True)

add_header("6.4 Replenishment Order Quantity Engine", level=2)
add_p("The dashboard provides two distinct replenishment quantity calculations:")
add_bullet("Minimum Units to reach Reorder Level: Deficit = MAX(0, reorder_level - quantity_on_hand). Capital Required = Deficit * cost. (Current store total: 60 units, $152.00).", "1. Minimum Safety Deficit: ")
add_bullet("Optimal Safety Buffer Order (2x ROP): Suggested PO = MAX(0, (2 * reorder_level) - quantity_on_hand). Capital Required = Suggested PO * cost. (Current store total: 142 units, $383.00). This provides operational breathing room and accounts for vendor shipment cycles.", "2. Target Par Order: ")

# -------------------------------------------------------------
# SECTION 7: DATABASE LIMITATIONS & MITIGATIONS
# -------------------------------------------------------------
add_header("7. Database Limitations, Operational Risks & Mitigations", level=1)
add_p("To establish realistic expectations and guide future IT roadmap investments, management must be aware of the inherent structural limitations of garden_shop.db:")

lim_table_data = [
    ["No Stock Movement History / Audit Ledger", "Database records only static quantity_on_hand. There are no timestamped receiving logs, cycle counts, or shrinkage entries.", "HIGH", "Current system relies on point-in-time snapshots. Mitigation: Implement an audit logging trigger in SQLite/PostgreSQL to capture daily inventory delta snapshots."],
    ["Absence of Supplier Delivery Lead Times", "No transit times, order dates to suppliers, or fulfillment punctuality records exist.", "HIGH", "Cannot dynamically adjust safety stock or predict days-to-stockout with precision. Mitigation: Base reorders on existing calibrated reorder_level thresholds and capture lead-time metrics in procurement."],
    ["Transaction Volume Sparsity (24 Orders)", "Dataset contains only 24 orders across 5 months, resulting in intermittent purchase intervals.", "MEDIUM", "Prevents statistical forecasting. Mitigation: Use aggregate volume ranking and relative velocity rather than daily run-rate extrapolations."],
    ["Missing Supplier Contact Email (Ironwood)", "Ironwood Tools has NULL contact email, preventing electronic purchase order transmission.", "HIGH", "Procurement delays on Hand Cultivator. Mitigation: Dashboard surfaces prominent visual warning banner with direct phone contact placeholder."],
    ["Lack of Product Physical Dimensions & Perishability", "No cube volume, pallet space, soil moisture shelf-life, or plant perishability data.", "LOW", "Limits warehouse bin and rack allocation planning. Mitigation: Incorporate physical attributes during phase 2 WMS expansion."]
]
t_lim = doc.add_table(rows=6, cols=4)
format_table(t_lim, [1.6, 2.2, 0.7, 2.3],
             ["Database Limitation", "Operational Manifestation", "Risk", "Impact & Strategic Mitigation"],
             lim_table_data)

# -------------------------------------------------------------
# SECTION 8: TECHNICAL ARCHITECTURE & SEMANTIC SQL MODEL
# -------------------------------------------------------------
add_header("8. Technical Architecture, Tool Selection & Semantic SQL Model", level=1)
add_p("To ensure seamless implementation, the system is architected as a modular 3-tier application consisting of the SQLite storage engine, a semantic SQL reporting view layer, and an interactive front-end dashboard.")

add_header("8.1 Front-End BI Platform Evaluation", level=2)
add_p("A comparative evaluation was performed across standard enterprise BI tools:")
add_bullet("Streamlit (Python): Highly recommended for rapid, agile deployment. Enables direct, lightweight integration with Python, SQLite, and custom alerting logic with zero enterprise licensing cost.", "Platform 1 - Streamlit: ")
add_bullet("Power BI / Tableau: Recommended if the organization has an existing Microsoft 365 or Salesforce enterprise footprint, providing robust drag-and-drop drill-downs and role-based access control.", "Platform 2 - Power BI / Tableau: ")
add_bullet("Metabase: Excellent open-source self-service SQL visualization tool for operational teams.", "Platform 3 - Metabase: ")

add_header("8.2 Production SQL Semantic Views", level=2)
add_p("To decouple front-end presentation from database schema details, the following production-grade SQL views are specified for deployment:")

sql_view_1 = """-- View 1: Executive KPI Summary View
CREATE VIEW vw_kpi_summary AS
SELECT 
    COUNT(CASE WHEN discontinued = 0 THEN 1 END) AS active_skus,
    SUM(CASE WHEN discontinued = 0 AND quantity_on_hand >= reorder_level THEN 1 ELSE 0 END) * 100.0 / 
        COUNT(CASE WHEN discontinued = 0 THEN 1 END) AS inventory_health_pct,
    SUM(CASE WHEN discontinued = 0 AND quantity_on_hand = 0 THEN 1 ELSE 0 END) AS zero_stock_skus,
    SUM(CASE WHEN discontinued = 0 AND quantity_on_hand < reorder_level THEN 1 ELSE 0 END) AS understocked_skus,
    SUM(CASE WHEN discontinued = 0 AND quantity_on_hand < reorder_level 
             THEN (reorder_level - quantity_on_hand) * cost ELSE 0 END) AS capital_needed_to_rop,
    ROUND(SUM(CASE WHEN discontinued = 0 THEN quantity_on_hand * cost ELSE 0 END), 2) AS active_stock_cost_value,
    ROUND(SUM(CASE WHEN discontinued = 0 THEN quantity_on_hand * price ELSE 0 END), 2) AS active_stock_retail_value
FROM products;"""

p_sql1 = doc.add_paragraph()
r_sql1 = p_sql1.add_run(sql_view_1)
r_sql1.font.name = 'Consolas'
r_sql1.font.size = Pt(7.5)
r_sql1.font.color.rgb = COLOR_NAVY

sql_view_2 = """-- View 2: Operational Restock Action Workbench
CREATE VIEW vw_restock_workbench AS
WITH sales_rollup AS (
    SELECT oi.product_id, SUM(oi.quantity) AS total_sold, SUM(oi.quantity * oi.unit_price) AS total_rev
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
    s.contact_email,
    p.price,
    p.cost,
    p.quantity_on_hand,
    p.reorder_level,
    (p.reorder_level - p.quantity_on_hand) AS deficit_to_min,
    ROUND((p.reorder_level - p.quantity_on_hand) * p.cost, 2) AS cost_to_min,
    ((p.reorder_level * 2) - p.quantity_on_hand) AS suggested_po_units,
    ROUND(((p.reorder_level * 2) - p.quantity_on_hand) * p.cost, 2) AS suggested_po_cost,
    COALESCE(sr.total_sold, 0) AS units_sold,
    CASE 
        WHEN p.discontinued = 1 THEN 'P4: Discontinued'
        WHEN p.quantity_on_hand = 0 THEN 'P1: Critical Stockout'
        WHEN p.quantity_on_hand < p.reorder_level AND COALESCE(sr.total_sold, 0) >= 4 THEN 'P1: Top Seller at Risk'
        WHEN p.quantity_on_hand < p.reorder_level THEN 'P2: Restock Required'
        WHEN p.quantity_on_hand < (p.reorder_level * 1.5) THEN 'P3: Watchlist'
        ELSE 'P5: Healthy'
    END AS priority_tier
FROM products p
JOIN categories c ON p.category_id = c.category_id
JOIN suppliers s ON p.supplier_id = s.supplier_id
WHERE p.discontinued = 0 AND p.quantity_on_hand < p.reorder_level
ORDER BY p.quantity_on_hand ASC;"""

p_sql2 = doc.add_paragraph()
r_sql2 = p_sql2.add_run(sql_view_2)
r_sql2.font.name = 'Consolas'
r_sql2.font.size = Pt(7.5)
r_sql2.font.color.rgb = COLOR_NAVY

# -------------------------------------------------------------
# SECTION 9: IMPLEMENTATION ROADMAP & SIGN-OFF
# -------------------------------------------------------------
add_header("9. Operational Implementation Roadmap & Sign-Off Checklist", level=1)
add_p("To ensure a smooth transition from proposal to live operational execution, a 6-week phased implementation plan is outlined:")

roadmap_data = [
    ["Week 1: Data Modeling & SQL Views", "Deploy reporting views (vw_kpi_summary, vw_restock_workbench) to SQLite/PostgreSQL. Validate automated exclusion of cancelled orders and discontinued SKUs."],
    ["Week 2: Front-End BI Dashboard Build", "Construct interactive UI in Streamlit/Power BI with KPI cards, stacked bar charts, scatter matrix, and operational data grid."],
    ["Week 3: User Acceptance Testing (UAT)", "Conduct pilot testing with warehouse operations staff and merchandising buyers. Refine filter interactions and PO recommendation formulas."],
    ["Week 4: Supplier Contact Remediation", "Contact Ironwood Tools via phone to establish a registered procurement email address in the database."],
    ["Week 5: PO Automation & Email Integration", "Integrate automated 'One-Click PO Draft' functionality linking restock quantities to pre-formatted supplier order emails."],
    ["Week 6: Production Cutover & Daily Cadence", "Transition dashboard to live daily production refresh. Establish daily 9:00 AM inventory triage routine for operations team."]
]
t_road = doc.add_table(rows=7, cols=2)
format_table(t_road, [2.2, 4.6], ["Implementation Phase", "Target Deliverables & Milestones"], roadmap_data)

add_header("9.1 Operations Decision Support Sign-Off Checklist", level=2)
add_bullet("[X] All 7 core executive questions thoroughly analyzed and empirically resolved with hard numbers.", "Requirement 1: ")
add_bullet("[X] Cancelled orders (Order #17) strictly filtered from sales velocity and revenue models.", "Requirement 2: ")
add_bullet("[X] Discontinued products (Bird Feeder #24) isolated from restock queues and routed to clearance.", "Requirement 3: ")
add_bullet("[X] Database limitations (missing lead times, static inventory, missing supplier emails) documented with mitigations.", "Requirement 4: ")
add_bullet("[X] AI feature suggestions critically evaluated, with unviable models rejected and viable innovations adopted.", "Requirement 5: ")
add_bullet("[X] Production-ready SQL views specified for automated reporting pipeline integration.", "Requirement 6: ")

add_p("Conclusion: The proposed Interactive Inventory Monitoring & Restocking Dashboard addresses all current operational bottlenecks, mitigates imminent stockout risks on high-velocity items, and establishes a rigorous foundation for modern supply chain execution at Garden Shop.", italic=True)

# -------------------------------------------------------------
# SAVE DOCUMENT
# -------------------------------------------------------------
output_path = os.path.join(os.path.dirname(__file__), 'Garden_Shop_Inventory_Dashboard_Proposal.docx')
doc.save(output_path)
print(f"Document successfully created and saved to: {output_path}")

conn.close()
