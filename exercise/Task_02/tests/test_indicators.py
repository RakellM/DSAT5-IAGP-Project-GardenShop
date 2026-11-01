# tests/test_indicators.py
"""
Test Suite for Task 02 - Verification of Indicators and Business Rules.
Covers:
- TEST-001: Inventory health index calculation on active products.
- TEST-002: Replenishment capital deficit to reach minimum reorder level.
- TEST-003: Cancellation exclusion (Order #17 must not count as sales).
- TEST-004: Discontinued product segregation (Product #24 has 0 restock recommendation).
- TEST-005: Balance deduplication (Total active inventory cost equals $4,731.00).
- TEST-006: Multi-tier priority triage classification (P1 to P5).
- TEST-007: Validation on a small isolated subset (TDD verification).
- TEST-008: Empty filter handling (Graceful zero-state handling).
"""

import unittest
import pandas as pd
import sqlite3
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_loader import load_products_master, get_kpi_summary, get_connection

class TestGardenShopIndicators(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Loads master dataset once for integration tests."""
        cls.df = load_products_master()
        cls.kpis = get_kpi_summary(cls.df)

    def test_total_sku_counts(self):
        """Validates that exactly 24 total products exist: 23 active and 1 discontinued."""
        self.assertEqual(len(self.df), 24)
        active_count = len(self.df[self.df['discontinued'] == 0])
        disc_count = len(self.df[self.df['discontinued'] == 1])
        self.assertEqual(active_count, 23)
        self.assertEqual(disc_count, 1)

    def test_indicator_1_inventory_health_index(self):
        """TEST-001: Verifies the Inventory Health Index equals 78.3% (18 healthy out of 23 active)."""
        self.assertEqual(self.kpis['total_active_skus'], 23)
        self.assertEqual(self.kpis['healthy_skus'], 18)
        self.assertEqual(self.kpis['inventory_health_pct'], 78.3)

    def test_indicator_2_capital_deficit_to_rop(self):
        """TEST-002: Verifies that capital required to reach min ROP equals $152.00 across 60 deficit units."""
        self.assertEqual(self.kpis['total_deficit_units'], 60)
        self.assertEqual(self.kpis['capital_needed_to_rop'], 152.00)
        self.assertEqual(self.kpis['understocked_skus'], 5)

        # Granular verification of the 5 understocked items
        understocked = self.df[(self.df['discontinued'] == 0) & (self.df['deficit_to_min'] > 0)].set_index('product_id')
        self.assertEqual(len(understocked), 5)
        
        # 1. Hanging Basket (#14)
        self.assertEqual(understocked.loc[14, 'deficit_to_min'], 10)
        self.assertEqual(understocked.loc[14, 'cost_to_min'], 60.00)
        # 2. Hand Cultivator (#11)
        self.assertEqual(understocked.loc[11, 'deficit_to_min'], 7)
        self.assertEqual(understocked.loc[11, 'cost_to_min'], 24.50)
        # 3. Tomato Seeds 'Roma' (#7)
        self.assertEqual(understocked.loc[7, 'deficit_to_min'], 35)
        self.assertEqual(understocked.loc[7, 'cost_to_min'], 31.50)
        # 4. Orchid Food (#20)
        self.assertEqual(understocked.loc[20, 'deficit_to_min'], 4)
        self.assertEqual(understocked.loc[20, 'cost_to_min'], 16.00)
        # 5. Pothos 'Golden' (#4)
        self.assertEqual(understocked.loc[4, 'deficit_to_min'], 4)
        self.assertEqual(understocked.loc[4, 'cost_to_min'], 20.00)

    def test_indicator_3_critical_stockout(self):
        """Verifies that exactly 1 SKU has zero stock on hand (Hanging Basket #14)."""
        self.assertEqual(self.kpis['critical_stockouts'], 1)
        zero_items = self.df[self.df['quantity_on_hand'] == 0]
        self.assertEqual(len(zero_items), 1)
        self.assertEqual(zero_items.iloc[0]['product_id'], 14)
        self.assertEqual(zero_items.iloc[0]['product_name'], 'Hanging Basket')

    def test_rule_1_cancelled_order_exclusion(self):
        """TEST-003: Verifies that Order #17 (cancelled) is strictly excluded from sales."""
        conn = get_connection()
        # Query total units sold in valid orders vs all orders
        cur = conn.cursor()
        cur.execute("SELECT SUM(quantity) FROM order_items oi JOIN orders o ON oi.order_id = o.order_id WHERE o.status != 'cancelled'")
        valid_units = cur.fetchone()[0]
        self.assertEqual(valid_units, 86)

        cur.execute("SELECT SUM(quantity) FROM order_items")
        total_raw_units = cur.fetchone()[0]
        self.assertEqual(total_raw_units, 87) # 1 unit in Order #17
        conn.close()

        # Pruning Shears (product_id 9) has 1 cancelled unit and 1 pending unit
        pruning_shears = self.df[self.df['product_id'] == 9].iloc[0]
        self.assertEqual(pruning_shears['units_sold'], 1) # Must be 1, not 2

    def test_rule_2_discontinued_product_segregation(self):
        """TEST-004: Verifies Product #24 (Bird Feeder) receives 0 restock recommendation."""
        bird_feeder = self.df[self.df['product_id'] == 24].iloc[0]
        self.assertEqual(bird_feeder['discontinued'], 1)
        self.assertEqual(bird_feeder['quantity_on_hand'], 4)
        self.assertEqual(bird_feeder['reorder_level'], 6)
        # Must be quarantined from replenishment
        self.assertEqual(bird_feeder['deficit_to_min'], 0)
        self.assertEqual(bird_feeder['suggested_po_units'], 0)
        self.assertEqual(bird_feeder['priority_tier'], 'P4: Discontinued')

    def test_rule_3_balance_join_deduplication(self):
        """TEST-005: Verifies active inventory cost equals $4,731.00 (not duplicated across order lines)."""
        self.assertEqual(self.kpis['active_stock_cost_value'], 4731.00)
        self.assertEqual(self.kpis['active_stock_retail_value'], 10321.25)
        # Verify physical units sum to 933 active
        active_units = self.df[self.df['discontinued'] == 0]['quantity_on_hand'].sum()
        self.assertEqual(active_units, 933)

    def test_priority_tier_assignment(self):
        """TEST-006: Verifies correct assignment of Priority Tiers (P1 to P5)."""
        p_map = self.df.set_index('product_id')['priority_tier'].to_dict()
        
        # P1: Stockout
        self.assertEqual(p_map[14], 'P1: Critical Stockout')
        # P1: Bestseller at risk
        self.assertEqual(p_map[4], 'P1: Top Seller at Risk')   # Pothos (5 sold, 8 on hand)
        self.assertEqual(p_map[7], 'P1: Top Seller at Risk')   # Tomato Seeds (4 sold, 5 on hand)
        # P2: Restock scheduled
        self.assertEqual(p_map[11], 'P2: Restock Required')    # Hand Cultivator
        self.assertEqual(p_map[20], 'P2: Restock Required')    # Orchid Food
        # P4: Discontinued
        self.assertEqual(p_map[24], 'P4: Discontinued')        # Bird Feeder
        # P5: Healthy
        self.assertEqual(p_map[6], 'P5: Healthy')              # Sunflower Seeds (200 on hand)

    def test_calculation_on_isolated_subset(self):
        """TEST-007: TDD calculation validation on a small isolated mock subset of 3 products."""
        mock_data = pd.DataFrame([
            {"product_id": 101, "product_name": "Test Rose", "cost": 10.0, "price": 20.0, "quantity_on_hand": 2, "reorder_level": 5, "discontinued": 0, "units_sold": 6, "gross_revenue": 120.0},
            {"product_id": 102, "product_name": "Test Pot",  "cost": 5.0,  "price": 10.0, "quantity_on_hand": 10, "reorder_level": 5, "discontinued": 0, "units_sold": 2, "gross_revenue": 20.0},
            {"product_id": 103, "product_name": "Old Rake",  "cost": 8.0,  "price": 15.0, "quantity_on_hand": 1, "reorder_level": 4, "discontinued": 1, "units_sold": 0, "gross_revenue": 0.0}
        ])
        
        # Calculate derived fields using exact SPEC rules
        mock_data['deficit_to_min'] = mock_data.apply(
            lambda r: 0 if r['discontinued'] == 1 else max(0, r['reorder_level'] - r['quantity_on_hand']), axis=1
        )
        mock_data['cost_to_min'] = mock_data['deficit_to_min'] * mock_data['cost']

        kpis = get_kpi_summary(mock_data)

        # Expected:
        # Active SKUs: 2 (101, 102)
        # Healthy: 1 (102), Understocked: 1 (101)
        # Health Index = 1/2 = 50.0%
        # Deficit = (5 - 2) = 3 units of Rose; Cost = 3 * $10 = $30.00
        # Discontinued Old Rake (103) is excluded from restock deficit
        self.assertEqual(kpis['total_active_skus'], 2)
        self.assertEqual(kpis['inventory_health_pct'], 50.0)
        self.assertEqual(kpis['total_deficit_units'], 3)
        self.assertEqual(kpis['capital_needed_to_rop'], 30.00)
        self.assertEqual(kpis['discontinued_skus'], 1)

    def test_empty_filter_handling(self):
        """TEST-008: Verifies that filtering down to an empty DataFrame produces 0-state metrics without crashing."""
        empty_df = self.df[self.df['category_name'] == 'NonExistentCategory']
        self.assertEqual(len(empty_df), 0)
        kpis = get_kpi_summary(empty_df)
        self.assertEqual(kpis['total_active_skus'], 0)
        self.assertEqual(kpis['inventory_health_pct'], 0.0)
        self.assertEqual(kpis['total_deficit_units'], 0)
        self.assertEqual(kpis['capital_needed_to_rop'], 0.0)

if __name__ == '__main__':
    unittest.main()
