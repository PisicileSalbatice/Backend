from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(prefix="/professors", tags=["professors"])


@router.get("/", response_model=list[schemas.ProfessorCreate])
def get_professors(db: Session = Depends(database.get_db)):
    return db.query(models.Professor).all()
