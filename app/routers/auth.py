from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/auth", tags=["Authentication"])


ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(email: str, password: str, db: Session):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or user.password != password:
        return None
    return user




@router.post("/login")
def login_for_access_token(form_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(form_data.email, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
        )
    return {"message": "Login successful"}


def get_current_user(
    email: str = Query(..., description="The user's email"),
    password: str = Query(..., description="The user's password"),
    db: Session = Depends(get_db),
):
    user = authenticate_user(email, password, db)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )
    return user

