import os
import datetime
import psycopg2
from celery import Celery
from celery.schedules import crontab
from app.todos_crew.src.todos_crew.crew import TodosCrew


celery_app = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
)

# Beat schedule to check the DB every minute
celery_app.conf.beat_schedule = {
    'check-db-every-minute': {
        'task': 'check_database_task',
        'schedule': crontab(minute='*/1'),  # Every minute
    },
}

@celery_app.task
def add_task(a: int, b: int):
    return a + b

@celery_app.task(name='check_database_task')
def check_database_task():
    try:
        conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        cur = conn.cursor()
        cur.execute("SELECT * FROM todos;")
        result = cur.fetchall()
        
        # Transform the results into a list of dictionaries
        todos_list = []
        for todo in result:
            todo_dict = {
                'id': todo[0],
                'title': todo[1],
                'description': todo[2],
                'completed': todo[3]
            }
            todos_list.append(todo_dict)
        
        print(f"[DB] ✅ Successfully connected. Todos: {todos_list}")

        inputs = {
            'todos': todos_list,
        }
        
        todos_crew = TodosCrew().crew().kickoff(inputs=inputs)
        
        print(f"[Crew] ✅ Successfully kicked off crew: {todos_crew}")
        
        cur.close()
        conn.close()
        return f"DB checked successfully at {todos_list}"
    except Exception as e:
        print(f"❌ DB check failed: {e}")
        return f"DB check failed: {e}"

@celery_app.task
def multiply_task(a: int, b: int):
    return a * b
