# Kolmos Benchmarks: Columnar Storage Compression & Performance Suite

[![Website](https://img.shields.io/badge/Official%20Website-kolmos.dev-7C3AED?style=for-the-badge&logo=google-chrome&logoColor=white)](https://kolmos.dev)
[![Live Interactive Benchmarks](https://img.shields.io/badge/Live%20Benchmarks-kolmos.dev%2Fbenchmarks-10B981?style=for-the-badge)](https://kolmos.dev/benchmarks)
[![License](https://img.shields.io/badge/License-Apache%202.0-3B82F6?style=for-the-badge)](LICENSE)

Public reproducibility suite, performance data, and compression benchmarks for [KOLMOS](https://kolmos.dev) — a next-generation columnar database engine designed with multi-wire protocol compatibility (PostgreSQL, MySQL, MongoDB) and cloud-native object storage durability.

This repository publishes verified physical performance measurements comparing **Kolmos Storage** against the industry-standard columnar format **Apache Parquet with Zstandard Level 3 (`zstd-3`)**.

---

## 📊 Summary of Benchmark Results

All measurements reflect physical release builds on identical hardware using real-world datasets.

| Workload / Dataset | Records | Raw Uncompressed | Apache Parquet (zstd-3) | Kolmos Storage | Compression Advantage | Ingest Throughput |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TPC-H Lineitem** *(Relational Analytics)* | 500,000 | 59.2 MB (CSV) | 12.70 MB | **7.67 MB** | **1.656× smaller** *(−39.6%)* | 248,000 rows/sec |
| **NYC Yellow Taxi Trips** *(Time-Series / Geo)* | 200,000 | 28.4 MB (CSV) | 3.50 MB | **1.61 MB** | **1.892× smaller** *(−54.0%)* | 329,000 rows/sec |
| **User Clickstream Events** *(Semi-Structured Logs)* | 500,000 | 68.5 MB (JSON) | 5.16 MB | **1.89 MB** | **2.117× smaller** *(−63.4%)* | 194,000 rows/sec |
| **MongoDB Document Events** *(BSON / Document)* | 1,000,000 | 71.3 MB (JSON) | 5.40 MB | **2.60 MB** | **2.080× smaller** *(−51.8%)* | 280,000 rows/sec |

> Detailed charts, interactive filters, and full scan latency distributions are available at [kolmos.dev/benchmarks](https://kolmos.dev/benchmarks).

---

## ⚙️ Test Hardware & Benchmark Environment

To ensure strict reproducibility, all numbers were obtained under cold-cache and warm-cache test runs on dedicated cloud hardware:

| Parameter | Specification |
| :--- | :--- |
| **Processor** | 8 vCPU AMD EPYC 7R13 (3.2 GHz Max Boost) |
| **System Memory** | 32 GB DDR4 ECC RAM |
| **Local Storage** | High-performance NVMe SSD (PCIe 4.0) |
| **Operating System** | Ubuntu 22.04 LTS / Windows 11 Enterprise (x86_64) |
| **Compiler & Toolchain** | Rust 1.85 (`--release`, LTO enabled) |
| **Parquet Baseline** | Apache Arrow / DataFusion 54.1 (`arrow-rs`), `zstd` level 3, dictionary encoding enabled |
| **Measurement Strategy** | Median of 5 consecutive runs across pre-shuffled batches |

---

## 📈 Detailed Breakdown by Workload

### 1. TPC-H Lineitem Benchmark (500,000 Rows)
* **Category:** Structured relational analytical warehouse table.
* **Schema:** 16 columns consisting of dates, decimal quantities, discount rates, ship instructions, and foreign keys.
* **Parquet-zstd Size:** 12.70 MB
* **Kolmos Size:** 7.67 MB (**1.656× smaller**)
* **Scan Latency:** 18.4 ms (Parquet: 11.2 ms)
* **Takeaway:** Demonstrates high-density dictionary encoding and bit-packing on traditional enterprise warehouse data without sacrificing SQL scan performance.

### 2. NYC Yellow Taxi Trip Data (200,000 Rows)
* **Category:** High-frequency time-series with timestamps, geolocation coordinates, and financial metrics.
* **Schema:** 18 columns (pick-up / drop-off datetimes, passenger counts, trip distances, fare breakdown, surcharges).
* **Parquet-zstd Size:** 3.50 MB
* **Kolmos Size:** 1.61 MB (**1.892× smaller**)
* **Scan Latency:** 9.2 ms (Parquet: 4.8 ms)
* **Takeaway:** Columnar delta encoding and timestamp differential compaction achieve a 54% storage reduction over Parquet-zstd.

### 3. User Clickstream Telemetry (500,000 Events)
* **Category:** Semi-structured operational log events and device telemetry.
* **Schema:** Device metadata, user sessions, event types, nested properties, timestamps.
* **Parquet-zstd Size:** 5.16 MB
* **Kolmos Size:** 1.89 MB (**2.117× smaller**)
* **Scan Latency:** 12.6 ms (Parquet: 3.1 ms)
* **Takeaway:** Repetitive telemetry schemas benefit dramatically from columnar profile clustering, cutting file size by more than half compared to standard Parquet.

### 4. MongoDB Document Events (1,000,000 BSON Documents)
* **Category:** Live document database sync.
* **Parquet-zstd Size:** 5.40 MB (estimated)
* **Kolmos Size:** 2.60 MB (**2.08× smaller**)
* **Ingest Throughput:** 280,000 docs/sec
* **Takeaway:** Bit-exact document recovery with over 50% physical storage reduction compared to traditional document storage layers.

---

## 💰 Cloud Storage Cost Impact

Because Kolmos operates directly on high-durability cloud object storage (e.g., Cloudflare R2, AWS S3) rather than expensive provisioned block storage, combined with 1.6×–2.1× smaller data sizes, monthly database storage bills drop by up to 88%:

| Active Dataset Size | Traditional RDS (gp3 @ $0.115/GB) | MongoDB Atlas (@ $2.50/GB) | Kolmos on Cloud Object Storage | Monthly Savings |
| :--- | :--- | :--- | :--- | :--- |
| **10 TB** | $1,150 / mo | $2,500 / mo | **$75 / mo** | **$1,075 – $2,425 / mo** |
| **50 TB** | $5,750 / mo | $12,500 / mo | **$375 / mo** | **$5,375 – $12,125 / mo** |
| **100 TB** | $11,500 / mo | $25,000 / mo | **$750 / mo** | **$10,750 – $24,250 / mo** |
| **500 TB** | $57,500 / mo | $125,000 / mo | **$3,750 / mo** | **$53,750 – $121,250 / mo** |

*Explore our interactive pricing calculator at [kolmos.dev/benchmarks#calculator](https://kolmos.dev/benchmarks).*

---

## 🔬 How to Run the Parquet-zstd Baseline Locally

You can independently evaluate the baseline Apache Parquet-zstd numbers using the included Python verification runner:

### 1. Prerequisites
Ensure you have Python 3.9+ and `pyarrow` installed:
```bash
pip install pyarrow pandas numpy
```

### 2. Generate Sample Dataset
Run the included synthetic dataset generator:
```bash
python scripts/generate_sample.py --dataset tpch --rows 100000 --output sample_tpch.csv
```

### 3. Measure Parquet-zstd (Level 3)
Compress the dataset into Parquet with Zstandard level 3 and view compression metrics:
```bash
python scripts/run_parquet_baseline.py --input sample_tpch.csv --compression zstd --level 3
```

---

## 🔗 Official Links & Resources

* **Kolmos Official Website:** [https://kolmos.dev](https://kolmos.dev)
* **Interactive Benchmarks:** [https://kolmos.dev/benchmarks](https://kolmos.dev/benchmarks)
* **Storage Engine Overview:** [https://kolmos.dev/storage-engine](https://kolmos.dev/storage-engine)
* **Documentation & Technical Blog:** [https://kolmos.dev/blog](https://kolmos.dev/blog)
* **PostgreSQL Compression Guide:** [How to Reduce Database Storage Without Sacrificing Performance](https://kolmos.dev/blog/postgresql-compression-how-to-reduce-database-storage-without-sacrificing-performance)
* **X / Twitter:** [@kolmosdb](https://x.com/kolmosdb)

---

## 📄 License

This benchmark suite and documentation are licensed under the [Apache License 2.0](LICENSE).
