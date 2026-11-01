#!/usr/bin/env python3
"""
Reusable Analytics Engine for Olist E-commerce Database.
Executes queries dynamically against CSV files without hardcoding values.
Uses Python Standard Library only (csv, collections, argparse, json).
"""

import argparse
import csv
import json
import os
import sys
from collections import Counter, defaultdict


def load_customers(data_dir):
    """Loads customer UF mapping: idCliente -> descUF."""
    cust_file = os.path.join(data_dir, "cliente.csv")
    if not os.path.exists(cust_file):
        raise FileNotFoundError(f"Customer file not found at: {cust_file}")
    
    cust_uf = {}
    with open(cust_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            cust_uf[r["idCliente"]] = r.get("descUF", "UNKNOWN").strip().upper()
    return cust_uf


def load_delivered_orders(data_dir, start_date=None, end_date=None, uf_filter=None, cust_uf_map=None):
    """
    Loads delivered orders applying date boundaries and optional UF filter.
    Returns: dict of idPedido -> {idCliente, dtPedido, descUF}
    """
    orders_file = os.path.join(data_dir, "pedido.csv")
    if not os.path.exists(orders_file):
        raise FileNotFoundError(f"Orders file not found at: {orders_file}")

    delivered_orders = {}
    with open(orders_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get("descSituacao") != "delivered":
                continue

            dt_pedido = r.get("dtPedido", "")
            order_date = dt_pedido[:10] if dt_pedido else ""

            # Date filtering
            if start_date and order_date and order_date < start_date:
                continue
            if end_date and order_date and order_date > end_date:
                continue

            # UF filtering
            order_uf = cust_uf_map.get(r["idCliente"], "UNKNOWN") if cust_uf_map else None
            if uf_filter:
                if not order_uf or order_uf != uf_filter.upper():
                    continue

            delivered_orders[r["idPedido"]] = {
                "idCliente": r["idCliente"],
                "dtPedido": dt_pedido,
                "descUF": order_uf
            }

    return delivered_orders


def query_monthly_orders(delivered_orders):
    """Computes monthly delivered order volume."""
    monthly_counts = Counter()
    for o_info in delivered_orders.values():
        dt = o_info.get("dtPedido")
        if dt and len(dt) >= 7:
            month_key = dt[:7]
            monthly_counts[month_key] += 1
    
    # Sort chronologically
    sorted_months = [{"month": m, "order_count": monthly_counts[m]} for m in sorted(monthly_counts.keys())]
    return sorted_months


def query_top_ufs(delivered_orders, top_n=5):
    """Computes top N customer UFs by volume of delivered orders."""
    uf_counts = Counter()
    for o_info in delivered_orders.values():
        uf = o_info.get("descUF") or "UNKNOWN"
        uf_counts[uf] += 1

    top_list = []
    for rank, (uf, count) in enumerate(uf_counts.most_common(top_n), start=1):
        top_list.append({"rank": rank, "uf": uf, "order_count": count})
    return top_list


def query_average_ticket(data_dir, delivered_orders):
    """
    Computes average ticket of item prices per delivered order excluding freight.
    Formula: Total vlPreco for items of delivered orders / Count of distinct delivered orders.
    """
    items_file = os.path.join(data_dir, "item_pedido.csv")
    if not os.path.exists(items_file):
        raise FileNotFoundError(f"Items file not found at: {items_file}")

    total_orders = len(delivered_orders)
    if total_orders == 0:
        return {
            "delivered_orders_count": 0,
            "orders_with_items_count": 0,
            "coverage_percentage": 0.0,
            "total_items_price": 0.0,
            "average_ticket": None,
            "status": "NOT_APPLICABLE"
        }

    delivered_ids = set(delivered_orders.keys())
    orders_with_items = set()
    total_price = 0.0

    with open(items_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            o_id = r.get("idPedido")
            if o_id in delivered_ids:
                orders_with_items.add(o_id)
                price_str = r.get("vlPreco")
                if price_str:
                    try:
                        total_price += float(price_str)
                    except ValueError:
                        pass

    orders_with_items_count = len(orders_with_items)
    coverage_pct = round((orders_with_items_count / total_orders) * 100, 2)
    avg_ticket = round(total_price / total_orders, 2)

    return {
        "delivered_orders_count": total_orders,
        "orders_with_items_count": orders_with_items_count,
        "coverage_percentage": coverage_pct,
        "total_items_price": round(total_price, 2),
        "average_ticket": avg_ticket,
        "status": "OK"
    }


def main():
    parser = argparse.ArgumentParser(description="Olist Analytics Engine")
    parser.add_argument("--data-dir", default="data/olist", help="Path to Olist CSV folder")
    parser.add_argument("--query", required=True, choices=["monthly_orders", "top_ufs", "average_ticket", "all"],
                        help="Analysis metric to execute")
    parser.add_argument("--start-date", default=None, help="Start date filter (YYYY-MM-DD)")
    parser.add_argument("--end-date", default=None, help="End date filter (YYYY-MM-DD)")
    parser.add_argument("--uf", default=None, help="Filter by customer UF (e.g. SP, RJ)")
    parser.add_argument("--top-n", type=int, default=5, help="Number of UFs to return for top_ufs query")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="Output format")

    args = parser.parse_args()

    # Verify directory
    if not os.path.isdir(args.data_dir):
        print(json.dumps({"error": f"Directory not found: {args.data_dir}"}))
        sys.exit(1)

    try:
        cust_uf_map = load_customers(args.data_dir)
        delivered_orders = load_delivered_orders(
            args.data_dir,
            start_date=args.start_date,
            end_date=args.end_date,
            uf_filter=args.uf,
            cust_uf_map=cust_uf_map
        )
    except Exception as e:
        print(json.dumps({"error": f"Failed loading data: {str(e)}"}))
        sys.exit(1)

    result = {
        "metadata": {
            "data_dir": args.data_dir,
            "query": args.query,
            "filters": {
                "start_date": args.start_date,
                "end_date": args.end_date,
                "uf": args.uf
            },
            "delivered_orders_in_scope": len(delivered_orders)
        }
    }

    if args.query in ["monthly_orders", "all"]:
        result["monthly_orders"] = query_monthly_orders(delivered_orders)

    if args.query in ["top_ufs", "all"]:
        result["top_ufs"] = query_top_ufs(delivered_orders, top_n=args.top_n)

    if args.query in ["average_ticket", "all"]:
        result["average_ticket"] = query_average_ticket(args.data_dir, delivered_orders)

    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # Human readable text format
        print("=== Olist Analytics Result ===")
        print(f"Delivered orders in scope: {len(delivered_orders):,}")
        if "monthly_orders" in result:
            print("\nMonthly Delivered Orders:")
            for item in result["monthly_orders"]:
                print(f"  {item['month']}: {item['order_count']:,}")
        if "top_ufs" in result:
            print(f"\nTop {args.top_n} Customer States (UF):")
            for item in result["top_ufs"]:
                print(f"  #{item['rank']} {item['uf']}: {item['order_count']:,} orders")
        if "average_ticket" in result:
            ticket = result["average_ticket"]
            print("\nAverage Ticket per Delivered Order:")
            if ticket["average_ticket"] is not None:
                print(f"  Average Ticket: R$ {ticket['average_ticket']:.2f}")
                print(f"  Total Item Price: R$ {ticket['total_items_price']:,.2f}")
                print(f"  Orders with items coverage: {ticket['coverage_percentage']}%")
            else:
                print("  Average Ticket: Not Applicable (0 delivered orders in period)")


if __name__ == "__main__":
    main()
