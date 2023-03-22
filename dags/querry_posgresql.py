from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook

default_args = {
    'owner': 'sakabuana31',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='querry_postgres_v1.6',
    default_args=default_args,
    description='Querry to postgress connection',
    start_date=datetime(2023, 3, 18, 2),
    schedule_interval=None
) as dag:
    task1 = PostgresOperator(
        task_id='create_querry_postgres_table',
        postgres_conn_id='postgres_localhost',
        sql="""
            CREATE TABLE IF NOT EXISTS serving.serving_table_review (
            date DATE,
            mean_temp DECIMAL(5, 2),
            status_temp INT,
            precipitation DECIMAL(5, 2),
            status_preci INT,
            business_id TEXT,
            business_name TEXT,
            stars INT,
            date_values DATE
        );
        """
    )
    
    task2 = PostgresOperator(
        task_id='get_querry_postgres_table',
        postgres_conn_id='postgres_localhost',
        sql="""
            INSERT INTO serving.serving_table_review (
                date, mean_temp, status_temp, precipitation, status_preci, business_id, business_name, stars, date_values
            )
            SELECT 
                fact_review.date_values,
                dim_temperature.mean,
                dim_temperature.status_temp,
                dim_precipitation.precipitation,
                dim_precipitation.status_preci, 
                fact_review.business_id, 
                dim_business.name, 
                fact_review.stars, 
                fact_review.date_values
            FROM 
                fact_review
                LEFT JOIN dim_precipitation ON (fact_review.date_values = dim_precipitation.date)
                LEFT JOIN dim_temperature ON (fact_review.date_values = dim_temperature.date)
                LEFT JOIN dim_business ON (fact_review.business_id = dim_business.business_id)
            ORDER BY 
                fact_review.date_values;

        """
    )

    task1 >> task2

    # # set up XComArg for task1 to pass query results to task2
    # task2_xcom_arg = '{{ task_instance.xcom_pull(task_ids="get_querry_postgres_table") }}'

    # # pass query results from task1 to task2 using XCom
    # task3.set_upstream(task2)
    # task3.op_args = [task2_xcom_arg]