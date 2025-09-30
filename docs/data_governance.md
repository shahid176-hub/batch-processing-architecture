
# Data Security, Governance & Protection (Local Setup)

- **Buckets per zone**: raw, curated, aggregated.
- **Access**: limit credentials per service (ingest: write raw; spark: rw raw/curated/aggregated; delivery: read aggregated).
- **Encryption**: enable MinIO SSE for production; rotate keys.
- **Lineage**: Airflow DAG run id, task logs, curated/aggregated snapshot folders with dates.
- **Schema**: enforce with Spark expectations (e.g., datatype checks) before writing curated.
- **PII**: if present, pseudonymise or mask in the curated layer; never expose PII in aggregated outputs.
