"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, field_validator


class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    username: str
    password: str
    
    @field_validator('username')
    @classmethod
    def username_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('Username cannot be empty')
        if len(v) < 2:
            raise ValueError('Username must be at least 2 characters')
        return v.strip()
    
    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """Schema for user registration response."""
    id: int
    email: str
    username: str
    access_token: str
    message: str
    
    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    """Schema for login response."""
    access_token: str
    token_type: str = "bearer"
    message: str
