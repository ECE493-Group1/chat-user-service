import os
import datetime

from flask import Flask
from flask import jsonify
from flask import request
from flask_mail import Mail, Message

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import bcrypt
import jwt

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_SSL"] = True
app.config["MAIL_TLS"] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME")

db_string = f'postgresql://{os.environ.get("DB_USER")}:{os.environ.get("DB_USER")}@{os.environ.get("DB_SERVICE")}:{os.environ.get("DB_PORT")}/{os.environ.get("DB_NAME")}'

db = create_engine(db_string)
base = declarative_base()

mail = Mail(app)

class Users(base):
    __tablename__ = 'users'
    user_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

Session = sessionmaker(db)

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if not email or not password:
        return jsonify({"message": "email or password missing"}), 400

    session = Session()
    user = session.query(Users).filter_by(email=email).one_or_none()

    if not user:
        return jsonify({"message": "invalid email"})

    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"message": "invalid password"}), 400

    token = jwt.encode({"email": email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)}, app.config["JWT_SECRET_KEY"])
    return jsonify({"message": "login successful", "token": token}), 200


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

    session = Session()
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
    
    # session = Session()
    # if not session.query(Users).filter_by(email=email).one_or_none():
    #     return jsonify({"message": "email not registered"}), 400


    # Send link to email address
    msg = Message()
    msg.recipients = [email]
    msg.subject = "Password Reset Link"
    msg.body = "link"
    mail.send(msg)

    return jsonify({"message": "password reset link sent"}), 200


@app.route("/update-password", methods=["POST"])
def update_password():
    return ''

if __name__ == "__main__":
    app.run()