from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum

class DiscountType(str, Enum):
    percentage = "percentage"
    fixed_amount = "fixed_amount"
    bogo = "bogo"

# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Business Schemas
class BusinessCreate(BaseModel):
    email: EmailStr
    password: str
    business_name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None

class BusinessResponse(BaseModel):
    id: int
    email: str
    business_name: str
    description: Optional[str]
    logo_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# PromoCode Schemas
class PromoCodeCreate(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    discount_value: float
    discount_type: DiscountType
    expiry_date: Optional[datetime] = None
    max_uses: Optional[int] = None
    category_ids: Optional[List[int]] = []

class PromoCodeResponse(BaseModel):
    id: int
    business_id: int
    code: str
    name: str
    description: Optional[str]
    image_url: Optional[str]
    discount_value: float
    discount_type: DiscountType
    expiry_date: Optional[datetime]
    max_uses: Optional[int]
    current_uses: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str