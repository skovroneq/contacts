from unittest.mock import MagicMock
from src.database.models import User
from src.tests.conftest import login_user_confirmed_true_and_hash_password, login_user_token_created


def test_create_user(client, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("routes.auth.send_email", mock_send_email)

    response = client.post("/api/auth/signup", json=user.dict())

    assert response.status_code == 201, response.text
    data = response.json()
    assert data["user"]["email"] == user.email
    assert "id" in data["user"]
    assert data['detail'] == "User successfully created. Check your email for confirmation."


def test_login_user(user, session, client):
    login_user_confirmed_true_and_hash_password(user, session)

    response = client.post(
        "/api/auth/login",
        data={"username": user.email, "password": user.password},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data["token_type"] == "bearer"


def test_refresh_token(user, session, client):
    login_user_token_created(user, session)
    user_authorization: User = session.query(User).filter(User.email == user.email).first()

    response = client.get(
        '/api/auth/refresh_token',
        headers={'Authorization': f"Bearer {user_authorization.refresh_token}"},
    )

    assert response.status_code == 200, response.text
    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data
    assert data["token_type"] == "bearer"
