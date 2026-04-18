"""
Run this once to create the admin account:
    python seed_admin.py

Admin credentials:
    Email:    admin@donation.local
    Password: Admin@2026
"""
from app import create_app
from extensions import db, bcrypt
from models import Donor

app = create_app()

with app.app_context():
    db.create_all()

    existing = Donor.query.filter_by(email="admin@donation.local").first()
    if existing:
        print("Admin already exists.")
    else:
        admin = Donor(
            name          = "Admin",
            email         = "admin@donation.local",
            password_hash = bcrypt.generate_password_hash("Admin@2026", rounds=12).decode(),
            is_admin      = True,
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Admin created — ID: {admin.id}")
        print("Email:    admin@donation.local")
        print("Password: Admin@2026")
