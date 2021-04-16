import os
import tempfile

import pytest

from app import database
from app import create_app
from dotenv import load_dotenv

@pytest.fixture(scope='session')
def app():
    load_dotenv()
    app = create_app({"TESTING": True}, 'sqlite:///:memory:')

    yield app

@pytest.fixture(scope='session')
def client(app):
    return app.test_client()

@pytest.fixture
def session(app):
    from app.database import session
    yield session
    session.execute("DELETE FROM users")

@pytest.fixture
def auth(client):
    return AuthActions(client)

class AuthActions:
    def __init__(self, client):
        self._client = client
        self.email = "test@email.com"
        self.username = "testuser"
        self.password = "password123"
    
    def register(self, email=None, username=None, password=None):
        if email:
            self.email = email
            self.username = username
            self.password = password

        return self._client.post("/register", json={"email": self.email, "username": self.username, "password": self.password})

    def login(self, email=None, password=None):
        if email:
            self.email = email
            self.password = password
        return self._client.post("/login", json={"email": self.email, "password": self.password})