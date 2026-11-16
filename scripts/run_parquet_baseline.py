#!/usr/bin/env python3
"""
Evaluate Apache Parquet with Zstandard level 3 compression baseline on CSV/JSON datasets.

Prerequisites:
    pip install pyarrow pandas

Usage:
    python scripts/run_parquet_baseline.py --input sample_tpch.csv --compression zstd --level 3
"""

import argparse
import os
import time

def run_benchmark(input_csv: str, compression: str = "zstd", compression_level: int = 3):
    try:
        import pyarrow.csv as pv
        import pyarrow.parquet as pq
    except ImportError:
        print("Error: pyarrow is required. Run 'pip install pyarrow' to install.")
        return

    if not os.path.exists(input_csv):
        print(f"Error: Input file '{input_csv}' not found.")
        return

    raw_bytes = os.path.getsize(input_csv)
    raw_mb = raw_bytes / (1024 * 1024)

    print(f"Reading {input_csv} ({raw_mb:.2f} MB)...")
    start_read = time.perf_counter()
    table = pv.read_csv(input_csv)
    read_elapsed = time.perf_counter() - start_read
    row_count = table.num_rows

    print(f"Loaded {row_count:,} rows and {table.num_columns} columns in {read_elapsed:.2f}s.")

    output_parquet = input_csv + f".{compression}.parquet"
    print(f"Compressing into Parquet ({compression}, level {compression_level})...")

    start_write = time.perf_counter()
    pq.write_table(
        table,
        output_parquet,
        compression=compression,
        compression_level=compression_level,
        use_dictionary=True,
    )
    write_elapsed = time.perf_counter() - start_write

    parquet_bytes = os.path.getsize(output_parquet)
    parquet_mb = parquet_bytes / (1024 * 1024)
    ratio = raw_bytes / parquet_bytes if parquet_bytes > 0 else 0

    print("\n" + "=" * 55)
    print("PARQUET BASELINE MEASUREMENT RESULTS")
    print("=" * 55)
    print(f"Raw Input Size     : {raw_mb:.2f} MB ({raw_bytes:,} bytes)")
    print(f"Parquet Output Size: {parquet_mb:.2f} MB ({parquet_bytes:,} bytes)")
    print(f"Compression Ratio  : {ratio:.2f}x ({(1 - parquet_bytes/raw_bytes)*100:.1f}% space saved)")
    print(f"Ingest Throughput  : {row_count / write_elapsed:,.0f} rows/sec ({write_elapsed*1000:.1f} ms)")
    print(f"Output File        : {output_parquet}")
    print("=" * 55)
    print("\nCompare these baseline numbers with Kolmos columnar results at:")
    print("👉 https://kolmos.dev/benchmarks\n")

def main():
    parser = argparse.ArgumentParser(description="Measure Parquet-zstd baseline performance.")
    parser.add_argument("--input", type=str, required=True, help="Path to input CSV file")
    parser.add_argument("--compression", type=str, default="zstd", choices=["zstd", "snappy", "gzip", "none"])
    parser.add_argument("--level", type=int, default=3, help="Compression level (1-22 for zstd)")
    args = parser.parse_args()

    run_benchmark(args.input, args.compression, args.level)

if __name__ == "__main__":
    main()
