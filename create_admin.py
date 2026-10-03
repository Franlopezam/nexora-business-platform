import getpass
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.database import SessionLocal, init_db
from app.models.user import User
from app.security.auth import hash_password

init_db()
name = input("Name: ").strip()
email = input("Email: ").strip().lower()
password = getpass.getpass("Password: ")

db = SessionLocal()
if db.query(User).filter(User.email == email).first():
    raise SystemExit("A user with that email already exists.")

db.add(User(name=name, email=email, password_hash=hash_password(password), role="admin"))
db.commit()
db.close()
print("Admin created.")
