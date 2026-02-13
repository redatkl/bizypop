from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/promo-codes", tags=["promo-codes"])

@router.post("/", response_model=schemas.PromoCodeResponse)
def create_promo_code(
    promo: schemas.PromoCodeCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    # Only businesses can create promo codes
    if not isinstance(current_user, models.Business):
        raise HTTPException(status_code=403, detail="Only businesses can create promo codes")
    
    # Check if code already exists
    existing = db.query(models.PromoCode).filter(models.PromoCode.code == promo.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Promo code already exists")
    
    new_promo = models.PromoCode(
        business_id=current_user.id,
        code=promo.code,
        name=promo.name,
        description=promo.description,
        discount_value=promo.discount_value,
        discount_type=promo.discount_type,
        expiry_date=promo.expiry_date,
        max_uses=promo.max_uses
    )
    
    # Add categories
    if promo.category_ids:
        categories = db.query(models.Category).filter(models.Category.id.in_(promo.category_ids)).all()
        new_promo.categories = categories
    
    db.add(new_promo)
    db.commit()
    db.refresh(new_promo)
    return new_promo

@router.get("/", response_model=List[schemas.PromoCodeResponse])
def get_all_promo_codes(db: Session = Depends(get_db)):
    promo_codes = db.query(models.PromoCode).filter(models.PromoCode.is_active == True).all()
    return promo_codes

@router.get("/my-promo-codes", response_model=List[schemas.PromoCodeResponse])
def get_my_promo_codes(
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    if not isinstance(current_user, models.Business):
        raise HTTPException(status_code=403, detail="Only businesses can access this")
    
    promo_codes = db.query(models.PromoCode).filter(
        models.PromoCode.business_id == current_user.id
    ).all()
    return promo_codes

@router.get("/{promo_id}", response_model=schemas.PromoCodeResponse)
def get_promo_code(promo_id: int, db: Session = Depends(get_db)):
    promo = db.query(models.PromoCode).filter(models.PromoCode.id == promo_id).first()
    if not promo:
        raise HTTPException(status_code=404, detail="Promo code not found")
    return promo

@router.delete("/{promo_id}")
def delete_promo_code(
    promo_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):
    if not isinstance(current_user, models.Business):
        raise HTTPException(status_code=403, detail="Only businesses can delete promo codes")
    
    promo = db.query(models.PromoCode).filter(
        models.PromoCode.id == promo_id,
        models.PromoCode.business_id == current_user.id
    ).first()
    
    if not promo:
        raise HTTPException(status_code=404, detail="Promo code not found")
    
    db.delete(promo)
    db.commit()
    return {"message": "Promo code deleted"}