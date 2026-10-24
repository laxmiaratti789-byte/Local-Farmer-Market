import os
import secrets
from pathlib import Path
from datetime import datetime
from functools import wraps


from dotenv import load_dotenv
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, abort
)
from flask_login import (
    LoginManager, login_user, logout_user,
    login_required, current_user
)
from sqlalchemy import func

from database import db
from models import User, Product, Order


# --------------------------------------------------
# APPLICATION SETUP
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "development-key-change-before-deployment"
)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL", "sqlite:///farmer_market.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

MODEL_FILE = BASE_DIR / "ml" / "crop_price_model.pkl"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        @login_required
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:
                flash("You do not have permission to do that.", "error")
                return redirect(url_for("dashboard"))
            return view(*args, **kwargs)
        return wrapped
    return decorator


# --------------------------------------------------
# SAMPLE PRODUCTS
# --------------------------------------------------

def add_sample_products():
    """Add visible demonstration products if the marketplace is empty."""
    if Product.query.first():
        return

    farmer = User.query.filter_by(
        email="demo-farmer@farmconnect.local"
    ).first()

    if not farmer:
        farmer = User(
            name="FarmConnect Demo Farmer",
            email="demo-farmer@farmconnect.local",
            role="farmer",
            location="Davangere, Karnataka"
        )
        farmer.set_password(secrets.token_urlsafe(24))
        db.session.add(farmer)
        db.session.flush()

    samples = [
        {"name": "Fresh Tomatoes", "category": "Vegetables", "price": 30, "quantity": 100, "unit": "kg", "location": "Davangere, Karnataka", "description": "Fresh locally grown tomatoes.", "image_url": "https://images.unsplash.com/photo-1546094096-0df4bcaaa337?auto=format&fit=crop&w=800&q=80"},
        {"name": "Red Onions", "category": "Vegetables", "price": 35, "quantity": 80, "unit": "kg", "location": "Gadag, Karnataka", "description": "Fresh red onions.", "image_url": "https://images.unsplash.com/photo-1508747703725-719777637510?auto=format&fit=crop&w=800&q=80"},
        {"name": "Fresh Potatoes", "category": "Vegetables", "price": 25, "quantity": 120, "unit": "kg", "location": "Haveri, Karnataka", "description": "Good-quality potatoes.", "image_url": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=800&q=80"},
        {"name": "Sweet Carrots", "category": "Vegetables",("name"): 40, ("quantity"): 50, ("unit"): "kg", ("location"): "Davangere, Karnataka", ("description"):("Fresh crunchy carrots."), ("image_url"):("https://images.unsplash.com/photo-1445282768818-728615cc910a?auto=format&fit=crop&w=800&q=80")},
        {"name":("Green Beans"), ("category"):("Vegetables"), ("price"):45, ("quantity"):40, ("unit"):("kg"), ("location"):("Haveri, Karnataka"), ("description"):("Fresh green beans."), ("image_url"):("")},
        {"name": "Fresh Cabbage", "category": "Vegetables", "price": 22, "quantity": 60, "unit": "kg", "location": "Dharwad, Karnataka", "description": "Farm-fresh cabbage.", "image_url": ""},
        {"name": "Cauliflower", "category": "Vegetables", "price": 32, "quantity": 45, "unit": "kg", "location": "Belagavi, Karnataka", "description": "Fresh cauliflower heads.", "image_url": ""},
        {"name": "Green Capsicum", "category": "Vegetables", "price": 50, "quantity": 35, "unit": "kg", "location": "Davangere, Karnataka", "description": "Fresh green capsicum.", "image_url": ""},
        {"name": "Fresh Spinach", "category": "Vegetables", "price": 20, "quantity": 30, "unit": "bunch", "location": "Gadag, Karnataka", "description": "Leafy green spinach.", "image_url": ""},
        {"name": "Green Chillies", "category": "Vegetables", "price": 55, "quantity": 25, "unit": "kg", "location": "Haveri, Karnataka", "description": "Fresh green chillies.", "image_url": ""},
        {"name": "Fresh Brinjal", "category": "Vegetables", "price": 28, "quantity": 45, "unit": "kg", "location": "Gadag, Karnataka", "description": "Locally grown brinjal.", "image_url": ""},
        {"name": "Ripe Pumpkin", "category": "Vegetables", "price": 24, "quantity": 70, "unit": "kg", "location": "Dharwad, Karnataka", "description": "Farm-grown pumpkin.", "image_url": ""},
        {"name": "Fresh Okra", "category": "Vegetables", "price": 38, "quantity": 40, "unit": "kg", "location": "Davangere, Karnataka", "description": "Fresh okra from local farms.", "image_url": ""},
        {"name": "Green Peas", "category": "Vegetables", "price": 65, "quantity": 25, "unit": "kg", "location": "Belagavi, Karnataka", "description": "Fresh green peas.", "image_url": ""},
        {"name": "Ripe Bananas", "category": "Fruits", "price": 45, "quantity": 100, "unit": "dozen", "location": "Shivamogga, Karnataka", "description": "Naturally ripened bananas.", "image_url": ""},
        {"name": "Fresh Apples", "category": "Fruits", "price": 140, "quantity": 35, "unit": "kg", "location": "Davangere, Karnataka", "description": "Crisp apples.", "image_url": ""},
        {"name": "Sweet Mangoes", "category": "Fruits", "price": 80, "quantity": 50, "unit": "kg", "location": "Dharwad, Karnataka", "description": "Sweet seasonal mangoes.", "image_url": ""},
        {"name": "Fresh Oranges", "category": "Fruits", "price": 70, "quantity": 40, "unit": "kg", "location": "Haveri, Karnataka", "description": "Juicy oranges.", "image_url": ""},
        {"name": "Green Grapes", "category": "Fruits", "price": 90, "quantity": 30, "unit": "kg", "location": "Belagavi, Karnataka", "description": "Fresh table grapes.", "image_url": ""},
        {"name": "Sweet Papaya", "category": "Fruits", "price": 35, "quantity": 40, "unit": "kg", "location": "Gadag, Karnataka", "description": "Fresh papaya.", "image_url": ""},
        {"name": "Farm Rice", "category": "Grains", "price": 55, "quantity": 150, "unit": "kg", "location": "Karnataka", "description": "Locally sourced rice.", "image_url": ""},
        {"name": "Wheat", "category": "Grains", "price": 38, "quantity": 100, "unit": "kg", "location": "Dharwad, Karnataka", "description": "Quality wheat grains.", "image_url": ""},
        {"name": "Ragi", "category": "Grains", "price": 42, "quantity": 90, "unit": "kg", "location": "Davangere, Karnataka", "description": "Nutritious finger millet.", "image_url": ""},
        {"name": "Jowar", "category": "Grains", "price": 36, "quantity": 75, "unit": "kg", "location": "Gadag, Karnataka", "description": "Locally grown sorghum.", "image_url": ""},
        {"name": "Toor Dal", "category": "Pulses", "price": 120, "quantity": 45, "unit": "kg", "location": "Gadag, Karnataka", "description": "Quality pigeon peas.", "image_url": ""},
        {"name": "Green Gram", "category": "Pulses", "price": 110, "quantity": 40, "unit": "kg", "location": "Haveri, Karnataka", "description": "Nutritious green gram.", "image_url": ""},
        {"name": "Groundnuts", "category": "Oilseeds", "price": 85, "quantity": 60, "unit": "kg", "location": "Gadag, Karnataka", "description": "Farm-grown groundnuts.", "image_url": ""},
        {"name": "Sunflower Seeds", "category": "Oilseeds", "price": 75, "quantity": 45, "unit": "kg", "location": "Karnataka", "description": "Sunflower seeds from local farms.", "image_url": ""},
        {"name": "Fresh Coconut", "category": "Other", "price": 30, "quantity": 80, "unit": "piece", "location": "Shivamogga, Karnataka", "description": "Fresh coconuts.", "image_url": ""},
        {"name": "Raw Turmeric", "category": "Spices", "price": 95, "quantity": 35, "unit": "kg", "location": "Belagavi, Karnataka", "description": "Locally grown turmeric.", "image_url": ""},
        {"name": "Fresh Ginger", "category": "Spices", "price": 100, "quantity": 25, "unit": "kg", "location": "Haveri, Karnataka", "description": "Fresh ginger roots.", "image_url": ""}
    ]
        

    for item in samples:
        db.session.add(Product(
            **item,
            farmer_id=farmer.id,
            available=True
        ))

    db.session.commit()


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.route("/")
def index():
    products = (
        Product.query.filter_by(available=True)
        .order_by(Product.created_at.desc())
        .limit(6).all()
    )
    return render_template("index.html", products=products)


# --------------------------------------------------
# REGISTER
# --------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "customer").strip().lower()
        location = request.form.get("location", "").strip()

        if not name or not email or len(password) < 8:
            flash(
                "Enter your name and email. Password must be at least 8 characters.",
                "error"
            )
        elif role not in ("farmer", "customer"):
            flash("Please choose farmer or customer.", "error")
        elif User.query.filter_by(email=email).first():
            flash("This email is already registered. Please sign in.", "error")
        else:
            user = User(
                name=name,
                email=email,
                role=role,
                location=location
            )
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            flash("Account created successfully!", "success")
            return redirect(url_for("dashboard"))

    return render_template("register.html")


# --------------------------------------------------
# LOGIN AND LOGOUT
# --------------------------------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash("Welcome back!", "success")
            return redirect(url_for("dashboard"))

        flash("Incorrect email or password.", "error")

    return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    flash("You have signed out successfully.", "success")
    return redirect(url_for("index"))


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/dashboard")
@login_required
def dashboard():
    if current_user.role == "farmer":
        products = (
            Product.query.filter_by(farmer_id=current_user.id)
            .order_by(Product.created_at.desc()).all()
        )
        orders = (
            Order.query.join(Product)
            .filter(Product.farmer_id == current_user.id)
            .order_by(Order.created_at.desc()).all()
        )
        total_sales = (
            db.session.query(func.coalesce(func.sum(Order.total_price), 0))
            .join(Product)
            .filter(
                Product.farmer_id == current_user.id,
                Order.status != "Cancelled"
            ).scalar()
        )
    else:
        products = []
        orders = (
            Order.query.filter_by(customer_id=current_user.id)
            .order_by(Order.created_at.desc()).all()
        )
        total_sales = 0

    available_products = Product.query.filter_by(
        available=True
    ).count()

    return render_template(
        "dashboard.html",
        products=products,
        orders=orders,
        total_sales=total_sales,
        available_products=available_products,
        total_orders=len(orders)
    )


# --------------------------------------------------
# MARKETPLACE
# --------------------------------------------------

@app.route("/products")
def products():
    search = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()

    query = Product.query.filter_by(available=True)

    if search:
        query = query.filter(
            Product.name.ilike(f"%{search}%")
            | Product.description.ilike(f"%{search}%")
            | Product.location.ilike(f"%{search}%")
        )

    if category:
        query = query.filter_by(category=category)

    items = query.order_by(Product.created_at.desc()).all()

    categories = [
        row[0] for row in
        db.session.query(Product.category).distinct().order_by(
            Product.category
        ).all()
        if row[0]
    ]

    return render_template(
        "products.html",
        products=items,
        q=search,
        category=category,
        categories=categories
    )


# --------------------------------------------------
# ADD PRODUCT
# --------------------------------------------------

@app.route("/products/new", methods=["GET", "POST"])
@role_required("farmer")
def product_new():
    if request.method == "POST":
        name = request.form.get("name", "").strip()

        try:
            price = float(request.form.get("price", ""))
            quantity = float(request.form.get("quantity", ""))
        except ValueError:
            flash("Enter a valid price and quantity.", "error")
            return render_template("product_form.html", product=None)

        if not name or price <= 0 or quantity <= 0:
            flash("Enter a name and positive price and quantity.", "error")
        else:
            product = Product(
                name=name,
                category=request.form.get("category", "Vegetables").strip()
                or "Vegetables",
                price=price,
                quantity=quantity,
                unit=request.form.get("unit", "kg").strip() or "kg",
                location=request.form.get("location", "").strip()
                or current_user.location,
                description=request.form.get("description", "").strip(),
                image_url=request.form.get("image_url", "").strip(),
                farmer_id=current_user.id,
                available=True
            )
            db.session.add(product)
            db.session.commit()
            flash("Product added successfully!", "success")
            return redirect(url_for("dashboard"))

    return render_template("product_form.html", product=None)


# --------------------------------------------------
# EDIT PRODUCT
# --------------------------------------------------

@app.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@role_required("farmer")
def product_edit(product_id):
    product = db.get_or_404(Product, product_id)

    if product.farmer_id != current_user.id:
        abort(403)

    if request.method == "POST":
        name = request.form.get("name", "").strip()

        try:
            price = float(request.form.get("price", ""))
            quantity = float(request.form.get("quantity", ""))
        except ValueError:
            flash("Enter a valid price and quantity.", "error")
            return render_template("product_form.html", product=product)

        if not name or price <= 0 or quantity < 0:
            flash("Enter a name, positive price, and valid quantity.", "error")
        else:
            product.name = name
            product.category = request.form.get(
                "category", "Vegetables"
            ).strip() or "Vegetables"
            product.price = price
            product.quantity = quantity
            product.unit = request.form.get("unit", "kg").strip() or "kg"
            product.location = request.form.get("location", "").strip()
            product.description = request.form.get("description", "").strip()
            product.image_url = request.form.get("image_url", "").strip()
            product.available = quantity > 0

            db.session.commit()
            flash("Product updated successfully!", "success")
            return redirect(url_for("dashboard"))

    return render_template("product_form.html", product=product)


# --------------------------------------------------
# DELETE PRODUCT
# --------------------------------------------------

@app.route("/products/<int:product_id>/delete", methods=["POST"])
@role_required("farmer")
def product_delete(product_id):
    product = db.get_or_404(Product, product_id)

    if product.farmer_id != current_user.id:
        abort(403)

    if Order.query.filter_by(product_id=product.id).first():
        product.available = False
        flash("Product marked unavailable because it has order history.", "success")
    else:
        db.session.delete(product)
        flash("Product deleted successfully.", "success")

    db.session.commit()
    return redirect(url_for("dashboard"))


# --------------------------------------------------
# PLACE ORDER
# --------------------------------------------------

@app.route("/products/<int:product_id>/order", methods=["POST"])
@role_required("customer")
def place_order(product_id):
    product = db.get_or_404(Product, product_id)

    try:
        quantity = float(request.form.get("quantity", "1"))
    except ValueError:
        quantity = 0

    if not product.available or quantity <= 0 or quantity > product.quantity:
        flash("Enter a valid quantity that is in stock.", "error")
    elif product.farmer_id == current_user.id:
        flash("You cannot order your own product.", "error")
    else:
        order = Order(
            customer_id=current_user.id,
            product_id=product.id,
            quantity=quantity,
            total_price=round(product.price * quantity, 2),
            status="Pending"
        )

        product.quantity = round(product.quantity - quantity, 2)
        if product.quantity <= 0:
            product.available = False

        db.session.add(order)
        db.session.commit()
        flash("Your order has been placed!", "success")

    return redirect(url_for("orders"))


# --------------------------------------------------
# ORDERS
# --------------------------------------------------

@app.route("/orders")
@login_required
def orders():
    if current_user.role == "farmer":
        items = (
            Order.query.join(Product)
            .filter(Product.farmer_id == current_user.id)
            .order_by(Order.created_at.desc()).all()
        )
    else:
        items = (
            Order.query.filter_by(customer_id=current_user.id)
            .order_by(Order.created_at.desc()).all()
        )

    return render_template("orders.html", orders=items)


@app.route("/orders/<int:order_id>/status", methods=["POST"])
@role_required("farmer")
def update_order_status(order_id):
    order = db.get_or_404(Order, order_id)

    if order.product.farmer_id != current_user.id:
        abort(403)

    status = request.form.get("status", "")
    allowed_statuses = (
        "Pending","Confirmed","Preparing","Delivered","Cancelled"
    )

    if status not in allowed_statuses:
        flash("Please choose a valid order status.", "error")
    else:
        if status == "Cancelled" and order.status != "Cancelled":
            product = order.product
            product.quantity = round(product.quantity + order.quantity, 2)
            product.available = product.quantity > 0

        order.status = status
        db.session.commit()
        flash("Order status updated.", "success")

    return redirect(url_for("orders"))


# --------------------------------------------------
# AI/ML CROP PRICE PREDICTION
# --------------------------------------------------

# --------------------------------------------------
# CROP PRICE ESTIMATION (NO EXTERNAL ML LIBRARIES)
# --------------------------------------------------

@app.route("/price-prediction", methods=["GET", "POST"])
def price_prediction():
    result = None

    # Demonstration prices from the project's sample dataset.
    sample_prices = {
        "tomato": [25, 28, 32, 24, 20, 18, 15, 17, 22, 27, 30, 35],
        "onion": [30, 32, 35, 33, 28, 25, 22, 24, 29, 34, 38, 40],
        "potato": [22, 24, 26, 25, 23, 20, 18, 19, 22, 25, 28, 30],
        "carrot": [35, 37, 40, 38, 34, 30, 27, 29, 34, 39, 42, 45],
    }

    if request.method == "POST":
        crop = request.form.get("crop", "tomato").strip().lower()

        try:
            month = int(request.form.get("month", "1"))
            days = int(request.form.get("days", "7"))
            current_price_text = request.form.get(
                "current_price", ""
            ).strip()
            current_price = (
                float(current_price_text) if current_price_text else None
            )
        except (ValueError, TypeError):
            flash("Enter valid month, days, and current price.", "error")
            return render_template("price_prediction.html", result=None)

        if (
            crop not in sample_prices
            or not 1 <= month <= 12
            or not 1 <= days <= 30
            or (current_price is not None and current_price <= 0)
        ):
            flash(
                "Choose a supported crop and enter valid values.",
                "error"
            )
        else:
            monthly_prices = sample_prices[crop]
            base_price = monthly_prices[month - 1]

            # Estimate a short-term change using the next month's
            # sample price trend. This is a demonstration estimate,
            # not a trained ML prediction or live market quote.
            next_month_price = monthly_prices[month % 12]
            weekly_change = (
                (next_month_price - base_price) / base_price
                if base_price else 0
            )

            reference_price = (
                current_price if current_price is not None else base_price
            )
            estimate = reference_price * (
                1 + weekly_change * min(days / 30, 1)
            )

            result = {
                "crop": crop.title(),
                "current": round(reference_price, 2),
                "days": days,
                "estimate": round(max(0, estimate), 2),
                "change": round(
                    (estimate - reference_price) / reference_price * 100,
                    2
                ),
                "method": "Sample-data estimation",
                "note": (
                    "Demonstration estimate based on sample prices. "
                    "It is not a trained ML model or a live market quote."
                )
            }

    return render_template(
        "price_prediction.html",
        result=result
    )

def update_product_images():
    from app import app
    from models import Product
    from database import db

    image_map = {
        "fresh ginger": "https://images.unsplash.com/photo-1615485500704-8e990f9900f3?w=600",
        "raw turmeric": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=600",
        "fresh coconut": "https://images.unsplash.com/photo-1550989460-0adf9ea622e2?w=600",
        "sunflower seeds": "https://images.unsplash.com/photo-1471943311424-646960669fbc?w=600",
        "groundnuts": "https://images.unsplash.com/photo-1567892737950-30c4db37cd89?w=600",
        "groundnut": "https://images.unsplash.com/photo-1567892737950-30c4db37cd89?w=600",
        "green gram": "https://images.unsplash.com/photo-1515543904379-3d757afe72e4?w=600",
        "toor dal": "https://images.unsplash.com/photo-1515543904379-3d757afe72e4?w=600",
        "jowar": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=600",
        "ragi": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=600",
        "wheat": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=600",
        "sweet papaya": "https://images.unsplash.com/photo-1517282009859-f000ec3b26fe?w=600",
        "green grapes": "https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=600",
        "fresh oranges": "https://images.unsplash.com/photo-1547514701-42782101795e?w=600",
        "sweet mangoes": "https://images.unsplash.com/photo-1553279768-865429fa0078?w=600",
        "fresh apples": "https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=600",
        "ripe bananas": "https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=600",
        "green peas": "https://images.unsplash.com/photo-1587735243615-c03f25aaff15?w=600",
        "fresh okra": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=600",
        "pumpkin": "https://images.unsplash.com/photo-1570586437263-ab629fccc818?w=600",
        "fresh brinjal": "https://images.unsplash.com/photo-1659261200847-2eab1b6b9a1a?w=600",
        "green chillies": "https://images.unsplash.com/photo-1588252303782-cb80119abd6d?w=600",
        "fresh spinach": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=600",
        "green capsicum": "https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?w=600",
        "cauliflower": "https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?w=600",
        "fresh cabbage": "https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=600",
        "farm-fresh rice": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=600",
        "fresh green beans": "https://images.unsplash.com/photo-1567375698348-5d9d5ae99de0?w=600",
        "sweet carrots": "https://images.unsplash.com/photo-1445282768818-728615cc910a?w=600",
        "fresh potatoes": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=600",
        "red onions": "https://images.unsplash.com/photo-1508747703725-719777637510?w=600",
        "fresh tomatoes": "https://images.unsplash.com/photo-1546094096-0df4bcaaa337?w=600",
    }

    with app.app_context():
        for product in Product.query.all():
            if not product.image_url:
                name = product.name.lower().strip()

                if name in image_map:
                    product.image_url = image_map[name]
                else:
                    for keyword, url in image_map.items():
                        if keyword in name:
                            product.image_url = url
                            break

        db.session.commit()

    print("Product image URLs updated.")


if __name__ == "__main__":
    update_product_images()
    app.run(debug=True)

