
# Batch Processing Data Architecture 

A **locally reproducible**, containerised, microservices-based batch data backend designed for a quarterly ML workflow.


## Microservices
- **Ingestion**: Python service that loads timestamped CSV/JSON files from a host `./data_source` into **MinIO** (object storage) under the `raw/` zone.
- **Processing (Batch)**: **Apache Spark** job reading `raw/` from MinIO and writing **curated** and **aggregated** Parquet back to MinIO.
- **Orchestration**: **Apache Airflow** DAG to coordinate ingest → process → validate → publish.
- **Delivery API**: **FastAPI** service that lists/downloads latest aggregated datasets (presigned URLs) for an external ML app.

## Storage
- **MinIO** (S3-compatible) as the data lake (zones: `raw`, `curated`, `aggregated`).

## Frequency
- Example schedule: **monthly ingestion**, **quarterly aggregation/publish** (configurable in the Airflow DAG).

## Quick Start
1. Copy `.env.example` to `.env` and adjust secrets if needed.
2. Create local folders:
   ```bash
   mkdir -p data_source
   mkdir -p volumes/minio volumes/airflow
   ```
3. Put your **timestamped** dataset files (≥1,000,000 rows recommended) into `./data_source` (CSV/JSON/Parquet supported).
4. Start stack:
   ```bash
   docker compose up -d --build
   ```
5. Open services:
   - MinIO console: http://localhost:9001  (user/pass from `.env`)
   - Airflow Web:    http://localhost:8081  (user: `airflow` / pass: `airflow` on first init)
   - Delivery API:   http://localhost:8080/docs

### Airflow init (first run)
```bash
docker compose run --rm airflow-webserver airflow db init
docker compose run --rm airflow-webserver airflow users create \
  --username airflow --password airflow --firstname Data --lastname Engineer --role Admin --email you@example.com
```

## Data Governance & Security (local-friendly)
- **Secrets via `.env`** (never commit real secrets).
- **Network isolation**: services run on a private Docker network; object storage never exposed publicly.
- **MinIO SSE** (server-side encryption) can be enabled later; IAM-style bucket policies are scripted in `config/minio/create-buckets.sh`.
- **Provenance** via Airflow DAG runs and immutable Parquet snapshots by partition timestamp.

## Architecture (Mermaid)
See `docs/architecture.mmd`. Render with [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli):
```bash
npm i -g @mermaid-js/mermaid-cli
mmdc -i docs/architecture.mmd -o docs/architecture.png
```

## What you provide
- **Data only** in `./data_source` (timestamped). Everything else is here.

## Notes
- The code is modular and production-leaning but kept **light** for local assessment.
- Spark uses MinIO via `s3a`. Credentials and endpoint configured via env.
