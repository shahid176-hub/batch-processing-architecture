
include .env

.PHONY: up down logs ps spark-submit init airflow-user

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

ps:
	docker compose ps

spark-submit:
	docker compose exec spark spark-submit \
	  --master spark://spark:7077 \
	  --conf spark.hadoop.fs.s3a.endpoint=${S3_ENDPOINT_URL} \
	  --conf spark.hadoop.fs.s3a.path.style.access=${S3A_PATH_STYLE_ACCESS} \
	  --packages org.apache.hadoop:hadoop-aws:3.3.4,software.amazon.awssdk:s3:2.25.80 \
	  /opt/spark-apps/job.py

init:
	mkdir -p data_source volumes/minio volumes/airflow

airflow-user:
	docker compose run --rm airflow-webserver airflow users create \
	 --username airflow --password airflow --firstname Data --lastname Engineer \
	 --role Admin --email you@example.com
