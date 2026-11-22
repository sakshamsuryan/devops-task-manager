from datetime import date
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Task, User

tasks_bp = Blueprint("tasks", __name__)
STATUSES = {"todo", "in_progress", "done"}
PRIORITIES = {"low", "medium", "high"}

def visible_query():
    q = Task.query
    return q if current_user.role == "admin" else q.filter_by(user_id=current_user.id)

def serialize(task):
    return {"id": task.id, "title": task.title, "description": task.description,
            "status": task.status, "priority": task.priority,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "created_at": task.created_at.isoformat(), "user_id": task.user_id}

def validate(payload):
    title = str(payload.get("title", "")).strip()
    status = payload.get("status", "todo")
    priority = payload.get("priority", "medium")
    description = str(payload.get("description", "")).strip()
    if not title or len(title) > 160:
        return None, "Title is required and must be at most 160 characters."
    if status not in STATUSES:
        return None, "Status must be todo, in_progress, or done."
    if priority not in PRIORITIES:
        return None, "Priority must be low, medium, or high."
    due = payload.get("due_date") or None
    try:
        due = date.fromisoformat(due) if due else None
    except (TypeError, ValueError):
        return None, "Due date must use YYYY-MM-DD."
    if len(description) > 5000:
        return None, "Description must be at most 5000 characters."
    return {"title": title, "description": description, "status": status, "priority": priority, "due_date": due}, None

@tasks_bp.get("/tasks")
@login_required
def list_tasks():
    tasks = visible_query().order_by(Task.created_at.desc()).all()
    return jsonify([serialize(t) for t in tasks])

@tasks_bp.post("/tasks")
@login_required
def create_task():
    payload, error = validate(request.get_json(silent=True) or {})
    if error:
        return jsonify(error=error), 400
    task = Task(**payload, user_id=current_user.id)
    db.session.add(task)
    db.session.commit()
    return jsonify(serialize(task)), 201

@tasks_bp.route("/tasks/<int:task_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
@login_required
def task_detail(task_id):
    task = visible_query().filter_by(id=task_id).first()
    if not task:
        return jsonify(error="Task not found"), 404
    if request.method == "GET":
        return jsonify(serialize(task))
    if request.method in ("PUT", "PATCH"):
        payload, error = validate({**serialize(task), **(request.get_json(silent=True) or {})})
        if error:
            return jsonify(error=error), 400
        for key, value in payload.items():
            setattr(task, key, value)
        db.session.commit()
        return jsonify(serialize(task))
    db.session.delete(task)
    db.session.commit()
    return jsonify(message="Task deleted"), 200

@tasks_bp.get("/admin/users")
@login_required
def list_users():
    if current_user.role != "admin":
        return jsonify(error="Administrator access required"), 403
    return jsonify([{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in User.query.order_by(User.id).all()])
