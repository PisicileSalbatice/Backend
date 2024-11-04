from fastapi import APIRouter, Depends, HTTPException
from .. import schemas

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/login")
def login(user: schemas.StudentCreate):
    # Logica de autentificare
    return {"message": "Logged in"}

