#!/usr/bin/env python3
"""
Generate synthetic benchmark datasets (TPC-H lineitem mock, NYC Taxi mock, Clickstream mock)
for testing columnar storage compression against Apache Parquet-zstd.

Usage:
    python scripts/generate_sample.py --dataset tpch --rows 100000 --output sample_tpch.csv
"""

import argparse
import random
import time
from datetime import datetime, timedelta

def generate_tpch(rows: int, output_path: str):
    print(f"Generating {rows} rows of synthetic TPC-H Lineitem schema...")
    ship_modes = ["AIR", "REG AIR", "FOB", "TRUCK", "RAIL", "SHIP", "MAIL"]
    priorities = ["1-URGENT", "2-HIGH", "3-MEDIUM", "4-NOT SPECIFIED", "5-LOW"]
    return_flags = ["R", "A", "N"]
    line_status = ["O", "F"]

    start_date = datetime(1992, 1, 1)

    with open(output_path, "w", encoding="utf-8") as f:
        # Header
        f.write("l_orderkey,l_partkey,l_suppkey,l_linenumber,l_quantity,l_extendedprice,l_discount,l_tax,l_returnflag,l_linestatus,l_shipdate,l_commitdate,l_receiptdate,l_shipinstruct,l_shipmode\n")
        
        for i in range(1, rows + 1):
            orderkey = i // 4 + 1
            partkey = random.randint(1, 200000)
            suppkey = random.randint(1, 10000)
            linenumber = (i % 4) + 1
            quantity = random.randint(1, 50)
            price = round(quantity * random.uniform(900.0, 1100.0), 2)
            discount = round(random.choice([0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10]), 2)
            tax = round(random.choice([0.00, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08]), 2)
            ret_flag = random.choice(return_flags)
            status = random.choice(line_status)
            
            day_offset = random.randint(0, 2400)
            ship_date = start_date + timedelta(days=day_offset)
            commit_date = ship_date + timedelta(days=random.randint(10, 30))
            receipt_date = ship_date + timedelta(days=random.randint(1, 25))
            
            ship_instruct = random.choice(["DELIVER IN PERSON", "TAKE BACK RETURN", "NONE", "COLLECT COD"])
            ship_mode = random.choice(ship_modes)

            f.write(f"{orderkey},{partkey},{suppkey},{linenumber},{quantity},{price},{discount},{tax},{ret_flag},{status},{ship_date.strftime('%Y-%m-%d')},{commit_date.strftime('%Y-%m-%d')},{receipt_date.strftime('%Y-%m-%d')},{ship_instruct},{ship_mode}\n")

    print(f"Done! Written to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate synthetic analytical benchmark datasets.")
    parser.add_argument("--dataset", choices=["tpch", "taxi", "clickstream"], default="tpch", help="Dataset type")
    parser.add_argument("--rows", type=int, default=100000, help="Number of rows to generate")
    parser.add_argument("--output", type=str, default="sample_dataset.csv", help="Output file path")
    args = parser.parse_args()

    generate_tpch(args.rows, args.output)

if __name__ == "__main__":
    main()
