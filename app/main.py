import os
import datetime

from flask import Flask
from flask import jsonify
from flask import request
from flask_mail import Mail, Message
from flask_cors import CORS

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from functools import wraps

import bcrypt
import jwt

app = Flask(__name__)

# CORS(app, resources={r"/*" : {"origins": os.environ.get("CHAT_UI_HOST") + ":" + os.environ.get("CHAT_UI_PORT")}})
CORS(app)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME")

db_string = f'postgresql://{os.environ.get("DB_USER")}:{os.environ.get("DB_USER")}@{os.environ.get("DB_SERVICE")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'

db = create_engine(db_string)
base = declarative_base()

mail = Mail(app)

Session = sessionmaker(db)
session = Session()

class Users(base):
    __tablename__ = 'users'
    user_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_token = None
        bearer = request.headers.get('Authorization')
        if bearer:
            auth_token = bearer.split()[1]
        try:
            payload = jwt.decode(auth_token, app.config["JWT_SECRET_KEY"], algorithms="HS256")
            email = payload["email"]
        except:
            return jsonify({"message": "invalid auth token"}), 400

        user = session.query(Users).filter_by(email=email).one_or_none()
        if not user:
            return jsonify({"message": "invalid auth token"}), 400
        return f(user, *args, **kwargs)
        
    return wrapper


@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if not email or not password:
        return jsonify({"message": "email or password missing"}), 400

    user = session.query(Users).filter_by(email=email).one_or_none()

    if not user:
        return jsonify({"message": "invalid email"})

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"message": "invalid password"}), 400

    token = jwt.encode({"email": email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)}, app.config["JWT_SECRET_KEY"])
    return jsonify({"message": "login successful", "token": token, "username": user.username}), 200


@app.route("/register", methods=["POST"])
def register():
    email = request.json.get("email", None)
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not email or not username or not password:
        return jsonify({"message": "email, username or password missing"}), 400

    if len(username) < 4:
        return jsonify({"message" : "username must be 4 characters or more"}), 400

    if len(password) < 8:
        return jsonify({"message": "password must be 8 characters or more"}), 400

    if session.query(Users).filter_by(username=username).one_or_none():
        return jsonify({"message": "username already in use"}), 400
    
    if session.query(Users).filter_by(email=email).one_or_none():
        return jsonify({"message": "email already in use"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user = Users(email=email, username=username, password=hashed_password.decode('utf-8'))
    session.add(user)
    session.commit()

    return jsonify({"message": "registration successful"}), 200


@app.route("/request-password-reset", methods=["POST"])
def request_password_reset():
    email = request.json.get("email", None)

    if not email:
        return jsonify({"message": "email missing"}), 400
    
    user = session.query(Users).filter_by(email=email).one_or_none()

    if not user:
        return jsonify({"message": "email not registered"}), 400

    token = jwt.encode({"email": email, "password": user.password, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=10)}, app.config["JWT_SECRET_KEY"])
 
    msg = Message()
    msg.recipients = [email]
    msg.subject = "[CAT Chat] Password Reset Link"
    msg.body = "http://localhost:8080/#/change-password/" + token
    mail.send(msg)

    return jsonify({"message": "password reset link sent"}), 200


@app.route("/update-password", methods=["POST"])
def update_password():
    reset_token = request.json.get("reset_token", None)
    new_password = request.json.get("new_password", None)

    if not reset_token or not new_password:
        return jsonify({"message": "reset token or new password missing"}), 400
    
    email = None
    token_password = None
    try:
        payload = jwt.decode(reset_token, app.config["JWT_SECRET_KEY"], algorithms="HS256")
        email = payload["email"]
        token_password = payload["password"]
    except:
        return jsonify({"message": "invalid token"}), 400

    user = session.query(Users).filter_by(email=email).one_or_none()
    if not user:
        return jsonify({"message": "invalid token"}), 400

    if token_password != user.password:
        return jsonify({"message": "invalid token"}), 400

    hashed_new_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    user.password = hashed_new_password.decode('utf-8')
    session.commit()
    
    return jsonify({"message": "password updated succesfully"}), 200

@app.route("/verify-reset-token", methods=["POST"])
def verify_reset_token():
    reset_token = request.json.get("reset_token", None)

    if not reset_token:
        return jsonify({"message": "reset token missing"}), 400
    
    email = None
    token_password = None
    try:
        payload = jwt.decode(reset_token, app.config["JWT_SECRET_KEY"], algorithms="HS256")
        email = payload["email"]
        token_password = payload["password"]
    except:
        return jsonify({"message": "invalid token"}), 400

    user = session.query(Users).filter_by(email=email).one_or_none()
    if not user:
        return jsonify({"message": "invalid token"}), 400

    if token_password != user.password:
        return jsonify({"message": "invalid token"}), 400
    
    return jsonify({"message": "token verification successful"}), 200


@app.route("/user-search", methods=["POST"])
@auth_required
def user_search(current_user):
    search_query = request.json.get("search_query", None)

    if not search_query:
        return jsonify({"message": "no query provided"}), 400
    
    results = session.query(Users).filter(or_(Users.email.like('%' + search_query + '%'), Users.username.like('%' + search_query + '%')))

    usernames = list(map(lambda user: user.username, results))

    return jsonify({"results": usernames}), 200


if __name__ == "__main__":
    app.run()