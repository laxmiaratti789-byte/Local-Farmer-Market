from app import app
from models import User, Product
from database import db


def get_product_image(name):
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

    normalized_name = name.lower().strip()






    
    if normalized_name in image_map:
        return image_map[normalized_name]

    for keyword, url in image_map.items():
        if keyword in normalized_name:
            return url

    return ""


EXTRA_PRODUCTS = [
    ("Fresh Cabbage", "Vegetables", 22, 60, "kg", "Dharwad, Karnataka"),
    ("Cauliflower", "Vegetables", 32, 45, "kg", "Belagavi, Karnataka"),
    ("Green Capsicum", "Vegetables", 50, 35, "kg", "Davangere, Karnataka"),
    ("Fresh Spinach", "Vegetables", 20, 30, "bunch", "Gadag, Karnataka"),
    ("Green Chillies", "Vegetables", 55, 25, "kg", "Haveri, Karnataka"),
    ("Fresh Brinjal", "Vegetables", 28, 45, "kg", "Gadag, Karnataka"),
    ("Pumpkin", "Vegetables", 24, 70, "kg", "Dharwad, Karnataka"),
    ("Fresh Okra", "Vegetables", 38, 40, "kg", "Davangere, Karnataka"),
    ("Green Peas", "Vegetables", 65, 25, "kg", "Belagavi, Karnataka"),
    ("Ripe Bananas", "Fruits", 45, 100, "dozen", "Shivamogga, Karnataka"),
    ("Fresh Apples", "Fruits", 140, 35, "kg", "Davangere, Karnataka"),
    ("Sweet Mangoes", "Fruits", 80, 50, "kg", "Dharwad, Karnataka"),
    ("Fresh Oranges", "Fruits", 70, 40, "kg", "Haveri, Karnataka"),
    ("Green Grapes", "Fruits", 90, 30, "kg", "Belagavi, Karnataka"),
    ("Sweet Papaya", "Fruits", 35, 40, "kg", "Gadag, Karnataka"),
    ("Wheat", "Grains", 38, 100, "kg", "Dharwad, Karnataka"),
    ("Ragi", "Grains", 42, 90, "kg", "Davangere, Karnataka"),
    ("Jowar", "Grains", 36, 75, "kg", "Gadag, Karnataka"),
    ("Toor Dal", "Pulses", 120, 45, "kg", "Gadag, Karnataka"),
    ("Green Gram", "Pulses", 110, 40, "kg", "Haveri, Karnataka"),
    ("Groundnuts", "Oilseeds", 85, 60, "kg", "Gadag, Karnataka"),
    ("Sunflower Seeds", "Oilseeds", 75, 45, "kg", "Karnataka"),
    ("Fresh Coconut", "Other", 30, 80, "piece", "Shivamogga, Karnataka"),
    ("Raw Turmeric", "Spices", 95, 35, "kg", "Belagavi, Karnataka"),
    ("Fresh Ginger", "Spices", 100, 25, "kg", "Haveri, Karnataka"),
]


with app.app_context():
    farmer = User.query.filter_by(email="demo-farmer@farmconnect.local").first()

    if farmer is None:
        farmer = User(
            name="FarmConnect Demo Farmer",
            email="demo-farmer@farmconnect.local",
            role="farmer",
            location="Davangere, Karnataka",
        )
        farmer.set_password("DemoFarmer!2026")
        db.session.add(farmer)
        db.session.flush()

    added = 0

    for name, category, price, quantity, unit, location in EXTRA_PRODUCTS:
        existing = Product.query.filter_by(farmer_id=farmer.id, name=name).first()

        if existing:
            continue

        product = Product(
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            unit=unit,
            location=location,
            description=f"Sample {name.lower()} listing for project demonstration.",
            image_url=get_product_image(name),
            available=True,
            farmer_id=farmer.id,
        )
        db.session.add(product)
        added += 1

    db.session.commit()

    print(f"New products added: {added}")
    print(f"Total products in database: {Product.query.count()}")

