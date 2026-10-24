from app import app
from database import db
from models import Product

products_to_delete = [
    "Fresh Ginger",
    "Raw Turmeric",
    "Fresh Coconut",
    "Groundnuts",
    "Toor Dal",
    "Jowar",
    "Ragi",
    "Fresh Okra",
    "Fresh Brinjal",
    "sunflower seeds",
]

with app.app_context():
    for name in products_to_delete:
        product = Product.query.filter(
            db.func.lower(Product.name) == name.lower()
        ).first()

        if product:
            db.session.delete(product)
            print(f"Deleted: {product.name}")
        else:
            print(f"Not found: {name}")

    db.session.commit()
    print("Finished deleting selected products.")