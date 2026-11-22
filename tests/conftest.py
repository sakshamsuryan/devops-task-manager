import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app({"TESTING": True, "WTF_CSRF_ENABLED": False, "SQLALCHEMY_DATABASE_URI": "sqlite://"})
    with app.app_context():
        db.drop_all(); db.create_all()
        yield app
        db.session.remove(); db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user(app):
    with app.app_context():
        u = User(name="Test User", email="test@example.com")
        u.set_password("password123")
        db.session.add(u); db.session.commit()
        return u.id
