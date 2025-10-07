from flask import Blueprint, jsonify, request
from .models import db, Task
from .metrics import TASK_CREATED_TOTAL
from .tasks import create_task_async


api_bp = Blueprint('api', __name__)


@api_bp.route('/')
def index():
    return jsonify({'message': 'Taskify API', 'status': 'ok'})


@api_bp.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return jsonify([t.to_dict() for t in tasks])


@api_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    title = data.get('title')
    description = data.get('description')
    if not title:
        return jsonify({'error': 'title required'}), 400


    task = Task(title=title, description=description)
    db.session.add(task)
    db.session.commit()
    TASK_CREATED_TOTAL.inc()


    # enqueue background job (example)
    create_task_async.delay(task.id)


    return jsonify(task.to_dict()), 201


@api_bp.route('/health')
def health():
    return jsonify({'status': 'healthy'})