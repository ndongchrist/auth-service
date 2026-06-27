import pytest

pytestmark = pytest.mark.django_db


def test_register_returns_tokens(api):
    resp = api.post(
        "/register/", {"username": "alice", "email": "a@x.io", "password": "supersecret"},
        format="json",
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["access"] and body["refresh"]
    assert body["user_id"]


def test_register_rejects_short_password(api):
    resp = api.post("/register/", {"username": "bob", "password": "short"}, format="json")
    assert resp.status_code == 400


def test_register_rejects_duplicate_username(api):
    api.post("/register/", {"username": "carol", "password": "supersecret"}, format="json")
    resp = api.post("/register/", {"username": "carol", "password": "supersecret"}, format="json")
    assert resp.status_code == 400


def test_login_after_register(api):
    api.post("/register/", {"username": "dave", "password": "supersecret"}, format="json")
    resp = api.post("/login/", {"username": "dave", "password": "supersecret"}, format="json")
    assert resp.status_code == 200
    assert "access" in resp.json()


def test_login_wrong_password(api):
    api.post("/register/", {"username": "erin", "password": "supersecret"}, format="json")
    resp = api.post("/login/", {"username": "erin", "password": "wrongpass"}, format="json")
    assert resp.status_code == 401
