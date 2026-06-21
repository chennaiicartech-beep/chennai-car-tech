from models import db, User
from flask import Flask
from routes.auth import auth
from routes.customer import customer
from routes.admin import admin_bp

from werkzeug.security import generate_password_hash

import os

app = Flask(__name__)

# ======================
# SECRET KEY
# ======================

app.secret_key = "cartech_secret"

# ======================
# DATABASE
# ======================

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///cartech.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ======================
# FILE UPLOADS
# ======================

UPLOAD_FOLDER = "static/uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# ======================
# INVOICE PDF FOLDER
# ======================

INVOICE_FOLDER = "static/invoices"

app.config["INVOICE_FOLDER"] = INVOICE_FOLDER

os.makedirs(
    INVOICE_FOLDER,
    exist_ok=True
)

# ======================
# DATABASE INIT
# ======================

db.init_app(app)

# ======================
# BLUEPRINTS
# ======================

app.register_blueprint(auth)
app.register_blueprint(customer)
app.register_blueprint(admin_bp)

# ======================
# CREATE DATABASE
# ======================

with app.app_context():

    db.create_all()

    if not User.query.filter_by(
        email="admin@cartech.com"
    ).first():

        admin = User(
            name="Admin",
            email="admin@cartech.com",
            password=generate_password_hash(
                "admin123"
            ),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

# ======================
# RUN APP
# ======================

if __name__ == "__main__":
    app.run(debug=True)