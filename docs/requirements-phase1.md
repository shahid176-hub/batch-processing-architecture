
# Conception Phase Justifications

## Ingestion Microservice
**Choice**: Python container with `boto3` + `pandas` to push raw files into MinIO under zone `raw/` (partitioned by `ingest_dt`).
**Why**: Simple, auditable, resilient retries; keeps batch scope (no Kafka needed for Phase 1).

## Storage
**Choice**: MinIO (S3-compatible) object storage as the data lake; Parquet files for columnar analytics.
**Why**: Open, local-friendly, scalable; Parquet reduces storage & I/O, preserves schema evolution.

## Pre-processing & Aggregation
**Choice**: Apache Spark (3.5) for scalable batch ETL → `curated/` and `aggregated/` zones.
**Why**: Mature ecosystem, fault tolerance, great with Parquet on S3-compatible stores.

## Delivery to ML App
**Choice**: FastAPI service providing a catalog of latest aggregates (with presigned URLs).
**Why**: Lightweight, language-agnostic ML consumers, avoids coupling.

## Reliability, Scalability, Maintainability
- Orchestration with Airflow (idempotent tasks, retries, SLA).
- Immutable data lake zones (raw/curated/aggregated) with timestamp partitions.
- Containerised microservices with healthchecks; stateless services for horizontal scale.

## Data Security, Governance, Protection
- Secrets via `.env`; principle of least privilege.
- MinIO buckets per zone; optional SSE & bucket policies (scriptable).
- Lineage via Airflow task metadata & job logs; schema checks in Spark job.

## Docker Images
- `minio/minio`, `minio/mc`, `postgres`, `apache/airflow`, `bitnami/spark`, custom `ingest` and `delivery` (Python 3.12 slim).
- Only thin wrappers needed for Python services.

## Data for Project
**Requirement**: ≥ 1,000,000 time-stamped records. Place your files in `./data_source`. Examples: web logs, IoT sensor dumps, stock ticks, NYC TLC trips, etc.

## Frequency
- Ingest **monthly** (configurable), aggregate/publish **quarterly** (Airflow DAG cron).

## Visual Architecture
See `docs/architecture.mmd` + `docs/flowchart.mmd`.
