from pydantic import BaseModel, EmailStr, field_validator

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str | None = "user"

    @field_validator("password")
    def validate_password_length(cls, v):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password cannot exceed 72 bytes for bcrypt.")
        return v

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    # Pydantic v2: allow reading ORM models
    model_config = {"from_attributes": True}
