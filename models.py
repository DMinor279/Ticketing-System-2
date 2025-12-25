from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("Application", backref="user", lazy=True)


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    #user = db.relationship("User", backref="applications")
    company = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    job_description = db.Column(db.Text)
    status = db.Column(db.String(50), default="Applied")
    deadline = db.Column(db.Date)
    date_applied = db.Column(db.Date, default=datetime.utcnow)


class AIAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey("application.id"), nullable=False)
    jd_summary = db.Column(db.Text)
    match_score = db.Column(db.Float)
    missing_skills = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
