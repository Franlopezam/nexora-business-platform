import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.database import SessionLocal, init_db
from app.models.user import User
from app.models.product import Product
from app.models.customer import Customer
from app.security.auth import hash_password

init_db()
db = SessionLocal()

if not db.query(User).filter(User.email == "admin@nexora.local").first():
    db.add(User(
        name="Nexora Admin",
        email="admin@nexora.local",
        password_hash=hash_password("Admin123!"),
        role="admin",
    ))

if db.query(Product).count() == 0:
    db.add_all([
        Product(sku="NX-MOU-01", name="Wireless Mouse", description="2.4GHz mouse", price=349, stock=24, min_stock=5),
        Product(sku="NX-KBD-01", name="Mechanical Keyboard", description="Compact keyboard", price=899, stock=12, min_stock=3),
        Product(sku="NX-HDP-01", name="Headset", description="USB gaming headset", price=699, stock=8, min_stock=2),
    ])

if db.query(Customer).count() == 0:
    db.add_all([
        Customer(name="Ana López", email="ana@example.com", phone="555-0101"),
        Customer(name="Carlos Méndez", email="carlos@example.com", phone="555-0102"),
    ])

db.commit()
db.close()
print("Nexora demo data is ready.")
