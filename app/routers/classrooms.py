from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Classroom

router = APIRouter()

@router.get("/classrooms")
def get_classrooms(db: Session = Depends(get_db)):
    classrooms = db.query(Classroom).all()
    return [
        {"name": cls.name, "short_name": cls.short_name, "building_name": cls.building_name}
        for cls in classrooms
    ]
