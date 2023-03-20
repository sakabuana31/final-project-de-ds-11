FROM apache/airflow:2.2.3
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    libqpdf-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow
RUN pip install --upgrade pip==23.0.1 && \
    pip install psycopg2-binary==2.9.1 && \
    pip install Cython numpy wheel setuptools && \
    pip install apache-airflow-providers-google
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir --user -r /requirements.txt

# docker build . --tag extending_airflow:latest
# docker-compose up -d --no-deps --build airflow-webserver airflowd-scheduler