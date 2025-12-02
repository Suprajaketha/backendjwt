from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import hash_password, verify_password


# --------------------------------------
# GET USER BY USERNAME
# --------------------------------------
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


# --------------------------------------
# GET USER BY EMAIL
# --------------------------------------
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


# --------------------------------------
# CREATE USER (REGISTER)
# --------------------------------------
def create_user(db: Session, username: str, email: str, password: str, role: str = "user"):
    hashed = hash_password(password)
    user = User(
        username=username,
        email=email,
        hashed_password=hashed,
        role=role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# --------------------------------------
# AUTHENTICATE USER (LOGIN)
# --------------------------------------
def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user
