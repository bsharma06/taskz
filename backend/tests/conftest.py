"""Pytest configuration and fixtures."""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from uuid import uuid4

# Set environment variables before importing app modules
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["JWT_SECRET"] = "test-secret-key-for-testing-only"
os.environ.setdefault("PASSLIB_BCRYPT_BACKEND", "bcrypt")

# Use bcrypt directly in tests to avoid passlib initialization issues
import bcrypt
def hash_password_for_test(password: str) -> str:
    """Hash password using bcrypt directly for tests."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

from app.main import app
from app.db.session import SessionLocal
from app.models.base import Base
from app.models.user import User
from app.models.task import Task


# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database session for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with database override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    # Override get_db in all route modules
    from app.api.routes import users, tasks, auth
    app.dependency_overrides[users.get_db] = override_get_db
    app.dependency_overrides[tasks.get_db] = override_get_db
    app.dependency_overrides[auth.get_db] = override_get_db

    # Override password functions to use bcrypt directly to avoid passlib issues
    from app.core import security
    from app.api.routes import auth as auth_module
    from app.api.routes import users as users_module
    
    original_verify = security.verify_password
    original_hash = security.get_password_hash
    
    def verify_password_override(plain: str, hashed: str) -> bool:
        """Override verify_password to use bcrypt directly."""
        try:
            return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))
        except Exception:
            return False
    
    def get_password_hash_override(password: str) -> str:
        """Override get_password_hash to use bcrypt directly."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    security.verify_password = verify_password_override
    security.get_password_hash = get_password_hash_override
    auth_module.verify_password = verify_password_override
    users_module.get_password_hash = get_password_hash_override

    with TestClient(app) as test_client:
        yield test_client
    
    # Restore original functions
    security.verify_password = original_verify
    security.get_password_hash = original_hash
    if hasattr(auth_module, 'verify_password'):
        auth_module.verify_password = original_verify
    if hasattr(users_module, 'get_password_hash'):
        users_module.get_password_hash = original_hash
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        id=str(uuid4()),
        user_email="test@example.com",
        user_name="Test User",
        pwd=hash_password_for_test("testpassword123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user2(db_session):
    """Create a second test user."""
    user = User(
        id=str(uuid4()),
        user_email="test2@example.com",
        user_name="Test User 2",
        pwd=hash_password_for_test("testpassword123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(client, test_user):
    """Get authentication token for test user."""
    response = client.post(
        "/auth/login",
        data={
            "username": test_user.user_email,
            "password": "testpassword123"
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(auth_token):
    """Get authorization headers with token."""
    return {"Authorization": f"Bearer {auth_token}"}

