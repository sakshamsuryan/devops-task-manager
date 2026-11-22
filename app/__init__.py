import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from prometheus_flask_exporter import PrometheusMetrics

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "change-this-development-key"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///taskmanager.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.getenv("COOKIE_SECURE", "false").lower() == "true",
        WTF_CSRF_TIME_LIMIT=None,
    )
    if test_config:
        app.config.update(test_config)
    os.makedirs(app.instance_path, exist_ok=True)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"
    @login_manager.unauthorized_handler
    def unauthorized():
        from flask import request, redirect, url_for, jsonify
        if request.path.startswith("/api/"):
            return jsonify(error="Authentication required"), 401
        return redirect(url_for("auth.login", next=request.url))
    csrf.init_app(app)
    PrometheusMetrics(app, path="/metrics", excluded_paths=["/health"])
    from app.models import User
    from app.auth import auth_bp
    from app.tasks import tasks_bp
    from app.main import main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api")
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    @app.errorhandler(404)
    def not_found(_):
        if _wants_json():
            return jsonify(error="Not found"), 404
        from flask import render_template
        return render_template("errors/404.html"), 404
    @app.errorhandler(500)
    def server_error(_):
        db.session.rollback()
        if _wants_json():
            return jsonify(error="Internal server error"), 500
        from flask import render_template
        return render_template("errors/500.html"), 500
    with app.app_context():
        db.create_all()
        _seed_admin()
    return app

def _wants_json():
    from flask import request
    return request.path.startswith("/api/") or request.is_json

def _seed_admin():
    from app.models import User
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    if email and password and not User.query.filter_by(email=email.lower()).first():
        db.session.add(User(name="Administrator", email=email.lower(), role="admin"))
        user = User.query.filter_by(email=email.lower()).first()
        if user:
            user.set_password(password)
        else:
            db.session.flush()
            User.query.filter_by(email=email.lower()).first().set_password(password)
        db.session.commit()
