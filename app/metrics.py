from prometheus_client import Gauge, Counter, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

TASK_COUNT = Gauge('taskify_task_count', 'Number of tasks in DB')
TASK_CREATED_TOTAL = Counter('taskify_tasks_total', 'Total number of tasks created')

def register_metrics(app):
    @app.route('/metrics')
    def metrics():
        try:
            from .models import Task, db
            count = Task.query.count()
            TASK_COUNT.set(count)
        except Exception:
            pass
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)