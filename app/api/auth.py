from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.auth import LoginRequest
from app.schemas.user import UserCreate, UserOut
from app.core.security import verify_password, create_access_token
from app.crud.user import create_user, get_user_by_username
from app.api.deps import get_db

# ============================================
# MUST BE FIRST NON-IMPORT LINE
# ============================================
router = APIRouter(prefix="/api/auth", tags=["Auth"])


# ============================================
# REGISTER
# ============================================
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(request: UserCreate, db: Session = Depends(get_db)):

    # Check if user already exists
    if get_user_by_username(db, request.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create user correctly
    user = create_user(
        db=db,
        username=request.username,
        email=request.email,
        password=request.password,   # create_user will hash this
        role=request.role
    )

    return user


# ============================================
# LOGIN
# ============================================
@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):

    user = get_user_by_username(db, request.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username")

    if not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_access_token({
        "sub": user.username,
        "role": user.role
    })

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }
