from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user
from datetime import datetime
from models import Application

from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password_hash=hashed_password)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("auth/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("dashboard"))

    return render_template("auth/login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    applications = Application.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", user=current_user, applications=applications)


@app.route("/applications/new", methods=["GET", "POST"])
@login_required
def add_application():
    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]
        status = request.form["status"]
        deadline = request.form["deadline"]

        application = Application(
            user_id=current_user.id,
            company=company,
            role=role,
            status=status,
            deadline=datetime.strptime(deadline, "%Y-%m-%d")
        )

        db.session.add(application)
        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("add_application.html")


@app.route("/applications/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_application(id):
    application = Application.query.get_or_404(id)
    if application.user_id != current_user.id:
        return "Unauthorized", 403

    if request.method == "POST":
        application.company = request.form["company"]
        application.role = request.form["role"]
        application.status = request.form["status"]
        application.deadline = datetime.strptime(request.form["deadline"], "%Y-%m-%d")
        db.session.commit()
        return redirect(url_for("dashboard"))

    return render_template("edit_application.html", application=application)


@app.route("/applications/<int:id>/delete", methods=["POST"])
@login_required
def delete_application(id):
    application = Application.query.get_or_404(id)
    if application.user_id != current_user.id:
        return "Unauthorized", 403

    db.session.delete(application)
    db.session.commit()
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
