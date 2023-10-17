from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'klein',
    'start_date': datetime(2023, 10, 17),
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('cron_job_intervalle',
          default_args=default_args,
          schedule_interval='@daily')



def run_script():
    exec(open("../../fast_job/get_job.py").read())

interval = PythonOperator(
    dag=dag,
    task_id='executer_script',
    python_callable= run_script,
    provide_context=True,
    start_date=datetime(2023, 10, 17),
)

interval
