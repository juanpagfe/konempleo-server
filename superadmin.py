from datetime import datetime
from sqlalchemy.orm import Session

from app.auth import authService
from db.session import SessionLocal
from models.user import UserEnum, Users

def create_superadmin(username: str, email: str, password: str,):
    db: Session = SessionLocal()

    # Check if a superadmin with the given email or username already exists
    existing_superadmin = db.query(Users).filter(
        (Users.role == UserEnum.super_admin) | (Users.email == email) | (Users.username == username)
    ).first()
    if existing_superadmin:
        print("A user with these credentials already exists!")
        return

    # Create the new superadmin user
    new_superadmin = Users(
        username=username,
        email=email,
        firstname= "admin",
        lastname= "user",
        password= authService.get_password_hash(password),
        role=UserEnum.super_admin,  # Set the role to super_admin
        created_at= datetime.utcnow(),
        updated_at= datetime.utcnow(),
        active=True,
    )
    db.add(new_superadmin)
    db.commit()
    db.refresh(new_superadmin)
    print("Superadmin created successfully!")

if __name__ == "__main__":
    # Example usage:
    create_superadmin("adminuser", "admin@example.com", "supersecretpassword")
