from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

# Database session start karein
db = SessionLocal()

try:
    # Admin user ko email se dhoondein
    user = db.query(User).filter(User.email == "admin@test.com").first()

    if user:
        user.hashed_password = get_password_hash("admin123")
        db.commit()
        print("SUCCESS: Admin password successfully updated to 'admin123'!")
    else:
        print("ERROR: 'admin@test.com' user database mein nahi mila!")
finally:
    db.close()