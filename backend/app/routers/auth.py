from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, auth
from app.database import get_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register/user", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        password_hash=hashed_password,
        name=user.name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/register/business", response_model=schemas.BusinessResponse)
def register_business(business: schemas.BusinessCreate, db: Session = Depends(get_db)):
    db_business = db.query(models.Business).filter(models.Business.email == business.email).first()
    if db_business:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(business.password)
    new_business = models.Business(
        email=business.email,
        password_hash=hashed_password,
        business_name=business.business_name,
        description=business.description,
        logo_url=business.logo_url
    )
    db.add(new_business)
    db.commit()
    db.refresh(new_business)
    return new_business

@router.post("/login", response_model=schemas.Token)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    # Check user table
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    if user and auth.verify_password(login_data.password, user.password_hash):
        access_token = auth.create_access_token(data={"sub": user.id, "type": "user"})
        return {"access_token": access_token, "token_type": "bearer"}
    
    # Check business table
    business = db.query(models.Business).filter(models.Business.email == login_data.email).first()
    if business and auth.verify_password(login_data.password, business.password_hash):
        access_token = auth.create_access_token(data={"sub": business.id, "type": "business"})
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")