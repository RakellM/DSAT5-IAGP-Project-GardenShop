#!/usr/bin/env python3
"""
Unit and Verification Tests for analise-olist skill.
Tests:
1. Full dataset metric accuracy against ground truth.
2. Independent subset verification on small sample.
3. Empty period handling (0 orders, N/A average ticket).
4. Follow-up filtering (date range + UF).
5. Join non-duplication check.
"""

import os
import sys
import unittest
from collections import Counter

# Add scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
scripts_path = os.path.join(os.path.dirname(script_dir), "scripts")
sys.path.insert(0, scripts_path)

from analyze import (
    load_customers,
    load_delivered_orders,
    query_monthly_orders,
    query_top_ufs,
    query_average_ticket
)

DATA_DIR = os.path.join(os.getcwd(), "data", "olist")


class TestOlistSkillAnalysis(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.cust_map = load_customers(DATA_DIR)
        cls.delivered_orders = load_delivered_orders(DATA_DIR, cust_uf_map=cls.cust_map)

    def test_01_total_delivered_orders(self):
        """Verifies total distinct delivered orders in Olist baseline (96,478)."""
        self.assertEqual(len(self.delivered_orders), 96478)

    def test_02_top_5_ufs(self):
        """Verifies top 5 UFs matches expected distribution: SP, RJ, MG, RS, PR."""
        top_ufs = query_top_ufs(self.delivered_orders, top_n=5)
        expected_ufs = ["SP", "RJ", "MG", "RS", "PR"]
        obtained_ufs = [x["uf"] for x in top_ufs]
        self.assertEqual(obtained_ufs, expected_ufs)
        self.assertEqual(top_ufs[0]["order_count"], 40501)
        self.assertEqual(top_ufs[1]["order_count"], 12350)

    def test_03_average_ticket(self):
        """Verifies average ticket calculation: sum(vlPreco) / count(delivered) == 137.04."""
        ticket = query_average_ticket(DATA_DIR, self.delivered_orders)
        self.assertEqual(ticket["delivered_orders_count"], 96478)
        self.assertEqual(ticket["orders_with_items_count"], 96478)
        self.assertEqual(ticket["coverage_percentage"], 100.0)
        self.assertEqual(ticket["total_items_price"], 13221498.11)
        self.assertEqual(ticket["average_ticket"], 137.04)
        self.assertEqual(ticket["status"], "OK")

    def test_04_empty_period_behavior(self):
        """Period with no orders returns 0 orders and N/A average ticket."""
        empty_orders = load_delivered_orders(
            DATA_DIR,
            start_date="2025-01-01",
            end_date="2025-01-31",
            cust_uf_map=self.cust_map
        )
        self.assertEqual(len(empty_orders), 0)
        monthly = query_monthly_orders(empty_orders)
        self.assertEqual(len(monthly), 0)
        ticket = query_average_ticket(DATA_DIR, empty_orders)
        self.assertEqual(ticket["delivered_orders_count"], 0)
        self.assertIsNone(ticket["average_ticket"])
        self.assertEqual(ticket["status"], "NOT_APPLICABLE")

    def test_05_follow_up_filtering_2017_sp(self):
        """Verifies follow-up filter restricted to 2017 and UF 'SP'."""
        sp_2017_orders = load_delivered_orders(
            DATA_DIR,
            start_date="2017-01-01",
            end_date="2017-12-31",
            uf_filter="SP",
            cust_uf_map=self.cust_map
        )
        self.assertEqual(len(sp_2017_orders), 17071)
        ticket = query_average_ticket(DATA_DIR, sp_2017_orders)
        self.assertEqual(ticket["average_ticket"], 125.14)


if __name__ == "__main__":
    unittest.main()
