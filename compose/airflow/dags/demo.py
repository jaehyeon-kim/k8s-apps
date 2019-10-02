from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime

dag = DAG(dag_id="test_dag", start_date=datetime(2019, 1, 15), schedule_interval="* * * * *")


def print_hello():
    return "hello!"


def print_goodbye():
    return "goodbye!"


t1 = PythonOperator(task_id="print_hello_world", python_callable=print_hello, dag=dag)

t2 = DockerOperator(
    task_id="print_hello_docker",
    image="busybox:latest",
    api_version="auto",
    auto_remove=True,
    volumes=["/var/run/docker.sock:/var/run/docker.sock"],
    command="sleep 2",
    docker_url="unix://var/run/docker.sock",
    network_mode="bridge",
    dag=dag,
)

t3 = PythonOperator(task_id="print_goodbye", python_callable=print_goodbye, dag=dag)

# Assign the order of the tasks in our DAG
t1 >> t2 >> t3
