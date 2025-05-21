from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Task, User
from database import db

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed
    } for task in tasks])

@tasks_bp.route('/', methods=['POST'])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        user_id=user_id
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task created"}), 201

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"message": "Task not found"}), 404
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    db.session.commit()
    return jsonify({"message": "Task updated"}), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"message": "Task not found"}), 404
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200
