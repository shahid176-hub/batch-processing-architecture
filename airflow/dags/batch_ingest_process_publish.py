from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='batch_ingest_process_publish',
    default_args=default_args,
    schedule_interval='@monthly',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['batch', 'spark', 'minio'],
) as dag:

    extract_from_minio = BashOperator(
        task_id='extract_from_minio',
        bash_command='python3 /opt/airflow/scripts/extract_from_minio.py'
    )

    spark_preprocess_job = BashOperator(
        task_id='spark_preprocess_job',
        bash_command="""
        /opt/bitnami/spark/bin/spark-submit \
          --master spark://spark:7077 \
          --jars /opt/bitnami/spark/jars/hadoop-aws-3.3.4.jar,/opt/bitnami/spark/jars/aws-java-sdk-bundle-1.12.262.jar \
          --conf spark.hadoop.fs.s3a.endpoint=http://minio:9000 \
          --conf spark.hadoop.fs.s3a.access.key=minio \
          --conf spark.hadoop.fs.s3a.secret.key=minio123 \
          --conf spark.hadoop.fs.s3a.path.style.access=true \
          --conf spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem \
          /opt/spark-apps/taxi_preprocess.py \
            --input s3a://raw/ingest_dt={{ ds_nodash }}/train.csv \
            --output s3a://curated/taxi_data/
        """
    )

    publish_to_curated = BashOperator(
        task_id='publish_to_curated',
        bash_command='python3 /opt/airflow/scripts/publish_to_curated.py'
    )

    notify_completion = BashOperator(
        task_id='notify_completion',
        bash_command='echo "Batch pipeline completed successfully!"'
    )

    extract_from_minio >> spark_preprocess_job >> publish_to_curated >> notify_completion
