import os
import tempfile

import pytest

from app import database
from app import create_app
from dotenv import load_dotenv

@pytest.fixture
def app():
    load_dotenv()

    db_fd, db_path = tempfile.mkstemp()
    print(db_path)
    app = create_app({"TESTING": True}, 'sqlite:///' + db_path)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def session(app):
    from app.database import session
    return session

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