from datetime import datetime, timedelta

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator


default_args = {
    'owner': 'sakabuana31',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}


with DAG(
    dag_id='to_posgrest_v4.9',
    default_args=default_args,
    description='Raw to postgress connection',
    start_date=datetime(2023, 3, 18, 2),
    schedule_interval=None
) as dag:
    task1 = PostgresOperator(
        task_id='create_postgres_table',
        postgres_conn_id='postgres_localhost',
        sql="""
            create table if not exists temperature (
                date DATE PRIMARY KEY,
                min DECIMAL(5, 2),
                max DECIMAL(5, 2),
                normal_min DECIMAL(5, 2),
                normal_max DECIMAL(5, 2),
                mean DECIMAL(5, 2),
                status_temp int
            ) 
        """
    )

    task2 = PostgresOperator(
        task_id='read_and_load_temperature',
        postgres_conn_id='postgres_localhost',
        sql="""
            CREATE TEMPORARY TABLE temp_temperature (
                date DATE PRIMARY KEY,
                min DECIMAL(5, 2),
                max DECIMAL(5, 2),
                normal_min DECIMAL(5, 2),
                normal_max DECIMAL(5, 2),
                mean DECIMAL(5, 2),
                status_temp int
            );

            COPY temp_temperature FROM '/opt/airflow/data/output-csv/dataclean-temperature-lasvegas.csv' DELIMITER ',' CSV HEADER;
            INSERT INTO temperature (date, min, max, normal_min, normal_max, mean, status_temp)
            SELECT date, min, max, normal_min, normal_max, mean, status_temp
            FROM temp_temperature
            ON CONFLICT (date) DO NOTHING;
        """
    )

    task3 = PostgresOperator(
        task_id='create_postgres_table_precipitation',
        postgres_conn_id='postgres_localhost',
        sql="""
            create table if not exists precipitation (
                date DATE PRIMARY KEY,
                precipitation DECIMAL(5, 2),
                precipitation_normal DECIMAL(5, 2),
                status_preci int
            )
        """
    )

    task4 = PostgresOperator(
        task_id='read_and_load_precipitation',
        postgres_conn_id='postgres_localhost',
        sql="""
            CREATE TEMPORARY TABLE temp_precipitation (
                date DATE PRIMARY KEY,
                precipitation DECIMAL(5, 2),
                precipitation_normal DECIMAL(5, 2),
                status_preci int
            );

            COPY temp_precipitation FROM '/opt/airflow/data/output-csv/dataclean-precipitation-lasvegas.csv' DELIMITER ',' CSV HEADER;
            INSERT INTO precipitation (date, precipitation, precipitation_normal, status_preci)
            SELECT date, precipitation, precipitation_normal, status_preci
            FROM temp_precipitation
            ON CONFLICT (date) DO NOTHING;
        """
    )

    task5 = PostgresOperator(
        task_id='create_postgres_table_business',
        postgres_conn_id='postgres_localhost',
        sql="""
            create table if not exists business (
                business_id text PRIMARY KEY,
                name text,
                address text,
                city text,
                state text,
                postal_code text,
                latitude float,
                longitude float,
                stars float,
                review_count int,
                is_open int,
                attributes text,
                categories text,
                hours text
            ) 
        """
    )

    task6 = PostgresOperator(
        task_id='read_and_load_business',
        postgres_conn_id='postgres_localhost',
        sql="""
            CREATE TEMPORARY TABLE temp_business (
                business_id text PRIMARY KEY,
                name text,
                address text,
                city text,
                state text,
                postal_code text,
                latitude float,
                longitude float,
                stars float,
                review_count int,
                is_open int,
                attributes text,
                categories text,
                hours text
            );

            COPY temp_business FROM '/opt/airflow/data/output-csv/business_restaurant.csv' DELIMITER ',' CSV HEADER;
            INSERT INTO business (business_id, name, address, city, state, postal_code, latitude, stars, review_count, is_open, attributes, categories, hours)
            SELECT business_id, name, address, city, state, postal_code, latitude, stars, review_count, is_open, attributes, categories, hours
            FROM temp_business
            ON CONFLICT (business_id) DO NOTHING;
        """
    )

    task7 = PostgresOperator(
        task_id='create_postgres_table_user',
        postgres_conn_id='postgres_localhost',
        sql="""
            create table if not exists user1 (
                user_id text PRIMARY KEY,
                name text,
                review_count text,
                useful int,
                funny int,
                cool int,
                elite text,
                friends text,
                fans text,
                average_stars float,
                yelping_since_values date
            ) 
        """
    )

    task8 = PostgresOperator(
        task_id='read_and_load_user',
        postgres_conn_id='postgres_localhost',
        sql="""
            CREATE TEMPORARY TABLE temp_user1 (
                user_id text PRIMARY KEY,
                name text,
                review_count text,
                useful int,
                funny int,
                cool int,
                elite text,
                friends text,
                fans text,
                average_stars float,
                yelping_since_values date
            );

            COPY temp_user1 FROM '/opt/airflow/data/output-csv/user_restaurant.csv' DELIMITER ',' CSV HEADER;
            INSERT INTO user1 (user_id, name, review_count, useful, funny, cool, elite, friends, fans, average_stars, yelping_since_values)
            SELECT user_id, name, review_count, useful, funny, cool, elite, friends, fans, average_stars, yelping_since_values
            FROM temp_user1
            ON CONFLICT (user_id) DO NOTHING;
        """
    )

    task9 = PostgresOperator(
        task_id='create_postgres_table_checkin',
        postgres_conn_id='postgres_localhost',
        sql="""
            create table if not exists checkin (
                business_id text,
                date_values date PRIMARY KEY
            ) 
        """
    )

    task10 = PostgresOperator(
        task_id='read_and_load_checkin',
        postgres_conn_id='postgres_localhost',
        sql="""
            CREATE TEMPORARY TABLE temp_checkin (
                business_id text,
                date_values date PRIMARY KEY
            );

            COPY temp_checkin FROM '/opt/airflow/data/output-csv/checkin_restaurant1.csv' DELIMITER ',' CSV HEADER;
            INSERT INTO checkin (business_id, date_values)
            SELECT DISTINCT ON (date_values) business_id, date_values
            FROM temp_checkin
            ORDER BY date_values
            ON CONFLICT (date_values) DO NOTHING;
        """
    )

    task11 = PostgresOperator(
        task_id='create_postgres_table_tip',
        postgres_conn_id='postgres_localhost',
        sql="""
            create table if not exists tip (
                user_id text not null PRIMARY KEY,
                business_id text not null,
                text text not null,
                compliment_count int not null,
                date_values date not null
            ) 
        """
    )

    task12 = PostgresOperator(
        task_id='read_and_load_tip',
        postgres_conn_id='postgres_localhost',
        sql="""
            CREATE TEMPORARY TABLE temp_tip (
                user_id text not null,
                business_id text not null,
                text text not null,
                compliment_count int not null,
                date_values date not null
            );

            COPY temp_tip FROM '/opt/airflow/data/output-csv/tip_restaurant.csv' DELIMITER ',' CSV HEADER NULL 'NA';
            INSERT INTO tip (user_id, business_id, text, compliment_count, date_values)
            SELECT user_id, business_id, text, compliment_count, date_values
            FROM temp_tip
            ON CONFLICT (user_id) DO NOTHING;
        """
    )

    task13 = PostgresOperator(
        task_id='create_postgres_table_review',
        postgres_conn_id='postgres_localhost',
        sql="""
            create table if not exists review (
                review_id text PRIMARY KEY,
                user_id text,
                business_id text,
                stars int,
                useful int,
                funny int,
                cool int,
                text text,
                date_values date
            ) 
        """
    )

    task14 = PostgresOperator(
        task_id='read_and_load_review',
        postgres_conn_id='postgres_localhost',
        sql="""
            CREATE TEMPORARY TABLE temp_review (
                review_id text not null PRIMARY KEY,
                user_id text not null,
                business_id text not null,
                stars int not null,
                useful int not null,
                funny int not null,
                cool int not null,
                text text not null,
                date_values date not null
            );

            COPY temp_review FROM '/opt/airflow/data/output-csv/review_restaurant.csv' DELIMITER ',' CSV HEADER NULL 'NA';
            INSERT INTO review (review_id, user_id, business_id, stars, useful, funny, cool, text, date_values)
            SELECT review_id, user_id, business_id, stars, useful, funny, cool, text, date_values
            FROM temp_review;
        """
    )    

    task1 >> task2 >> task3 >> task4 >> task5 >> task6 >> task7 >> task8 >> task9 >> task10 >> task11 >> task12 >> task13 >> task14
    