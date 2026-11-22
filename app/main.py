from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from app.models import Task
from app import db

main_bp = Blueprint("main", __name__)

@main_bp.get("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    return render_template("landing.html")

@main_bp.get("/health")
def health():
    return {"status": "healthy"}, 200

@main_bp.get("/dashboard")
@login_required
def dashboard():
    query = Task.query if current_user.role == "admin" else Task.query.filter_by(user_id=current_user.id)
    counts = {status: query.filter_by(status=status).count() for status in ("todo", "in_progress", "done")}
    recent = query.order_by(Task.created_at.desc()).limit(5).all()
    return render_template("dashboard.html", counts=counts, recent=recent, total=sum(counts.values()))
