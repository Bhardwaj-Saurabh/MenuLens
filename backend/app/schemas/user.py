"""
Pydantic schemas for user-related requests and responses
"""
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class AllergenBase(BaseModel):
    """Base schema for allergen"""
    name: str
    description: Optional[str] = None


class AllergenResponse(AllergenBase):
    """Schema for allergen response"""
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str = Field(..., min_length=8)


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = None
    is_vegetarian: Optional[bool] = None
    is_vegan: Optional[bool] = None
    is_halal: Optional[bool] = None
    is_kosher: Optional[bool] = None
    avoid_pork: Optional[bool] = None
    avoid_beef: Optional[bool] = None
    allergen_ids: Optional[List[int]] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    is_vegetarian: bool
    is_vegan: bool
    is_halal: bool
    is_kosher: bool
    avoid_pork: bool
    avoid_beef: bool
    created_at: datetime
    allergens: List[AllergenResponse] = []

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload"""
    username: Optional[str] = None
