from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, database
from fastapi import APIRouter, Depends, HTTPException
from .. import schemas, crud
from ..database import get_db

router = APIRouter(prefix="/exams", tags=["exams"])


@router.get("/", response_model=list[schemas.ExamCreate])
def get_exams(db: Session = Depends(database.get_db)):
    return db.query(models.Exam).all()

@router.post("/exams/", response_model=schemas.Exam)
def create_exam(exam: schemas.ExamCreate, db: Session = Depends(get_db)):
    return crud.create_exam(db=db, exam=exam)

@router.get("/exams/", response_model=List[schemas.Exam])
def read_exams(db: Session = Depends(get_db)):
    exams = crud.get_exams(db=db)
    return exams

@router.post("/exam_requests/", response_model=schemas.ExamRequest)
def create_exam_request(
    request: schemas.ExamRequestCreate, db: Session = Depends(get_db)
):
    exam_request = crud.create_exam_request(db=db, request=request)
    if not exam_request:
        raise HTTPException(status_code=400, detail="Exam request could not be created")
    return exam_request

@router.get("/exam_requests/", response_model=List[schemas.ExamRequest])
def get_exam_requests(
    student_id: int = None,
    professor_id: int = None,
    db: Session = Depends(get_db)
):
    exam_requests = crud.get_exam_requests(db=db, student_id=student_id, professor_id=professor_id)
    if not exam_requests:
        raise HTTPException(status_code=404, detail="No exam requests found")
    return exam_requests

@router.put("/exam_requests/{request_id}/status")
def update_exam_request_status(
    request_id: int,
    status: str,  # Expected values: "approved" or "rejected"
    db: Session = Depends(get_db)
):
    updated_request = crud.update_exam_request_status(db=db, request_id=request_id, status=status)
    if not updated_request:
        raise HTTPException(status_code=404, detail="Exam request not found")
    return {"message": "Exam request status updated successfully", "status": status}

