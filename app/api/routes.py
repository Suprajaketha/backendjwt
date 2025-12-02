from fastapi import APIRouter, Depends
from app.api.auth import router as auth_router
from app.api.deps import get_current_user, require_role

router = APIRouter()

# AUTH ROUTES
# auth_router already has prefix="/api/auth"
router.include_router(auth_router)

# USER ROUTE (JWT REQUIRED)
@router.get("/api/user")
def user_route(user=Depends(get_current_user)):
    return {
        "message": f"Hello {user.username}",
        "role": user.role
    }

# ADMIN ROUTE (JWT + ADMIN ROLE REQUIRED)
@router.get("/api/admin")
def admin_route(user=Depends(require_role("admin"))):
    return {
        "message": f"Welcome Admin {user.username}"
    }
