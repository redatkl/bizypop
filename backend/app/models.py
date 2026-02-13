from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class DiscountType(enum.Enum):
    percentage = "percentage"
    fixed_amount = "fixed_amount"
    bogo = "bogo"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Business(Base):
    __tablename__ = "businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    business_name = Column(String(150), nullable=False)
    description = Column(Text)
    logo_url = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    promo_codes = relationship("PromoCode", back_populates="business")

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    
    promo_codes = relationship("PromoCode", secondary="promo_categories", back_populates="categories")

class PromoCode(Base):
    __tablename__ = "promo_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey("businesses.id"), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)
    image_url = Column(String(500))
    discount_value = Column(DECIMAL(10, 2))
    discount_type = Column(SQLEnum(DiscountType), nullable=False)
    expiry_date = Column(DateTime(timezone=True))
    max_uses = Column(Integer, default=None)
    current_uses = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    business = relationship("Business", back_populates="promo_codes")
    categories = relationship("Category", secondary="promo_categories", back_populates="promo_codes")

class PromoCategory(Base):
    __tablename__ = "promo_categories"
    
    promo_code_id = Column(Integer, ForeignKey("promo_codes.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"), primary_key=True)