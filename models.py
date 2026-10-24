from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from database import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(
        db.String(150),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False, default="customer")

    location = db.Column(db.String(150), default="")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    products = db.relationship(
        "Product",
        backref="farmer",
        lazy=True
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)

    category = db.Column(
        db.String(80),
        nullable=False,
        default="Vegetables"
    )

    price = db.Column(db.Float, nullable=False)

    quantity = db.Column(db.Float, nullable=False, default=1)

    unit = db.Column(db.String(20), nullable=False, default="kg")

    location = db.Column(db.String(150), default="")

    description = db.Column(db.Text, default="")

    image_url = db.Column(db.String(500), default="")

    available = db.Column(db.Boolean, nullable=False, default=True)

    farmer_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )

    quantity = db.Column(db.Float, nullable=False)

    total_price = db.Column(db.Float, nullable=False)

    status = db.Column(
        db.String(30),
        nullable=False,
        default="Pending"
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship(
        "User",
        foreign_keys=[customer_id]
    )

    product = db.relationship("Product")
    