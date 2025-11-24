from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

# User Schema matching Supabase structure


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: Optional[str] = "user"


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    role: Optional[str] = "user"


class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class PasswordUpdate(BaseModel):
    current_password: str  # Contraseña actual para validar
    new_password: str  # Nueva contraseña


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None
