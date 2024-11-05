from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, crud
from app.database import get_db
from app.routers.auth import get_current_user 

router = APIRouter(prefix="/exams", tags=["exams"])

# Obține toate examenele
@router.get("/", response_model=List[schemas.Exam])
def get_exams(db: Session = Depends(get_db)):
    return crud.get_exams(db=db)

# Creare examen nou
@router.post("/", response_model=schemas.Exam)
def create_exam(exam: schemas.ExamCreate, db: Session = Depends(get_db)):
    return crud.create_exam(db=db, exam=exam)

# Creare cerere de examen
@router.post("/requests/", response_model=schemas.ExamRequest)
def create_exam_request(
    request: schemas.ExamRequestCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    # Verifică dacă utilizatorul este student
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can create exam requests")

    # Creează cererea
    exam_request = crud.create_exam_request(db=db, request=request)
    if not exam_request:
        raise HTTPException(status_code=400, detail="Exam request could not be created")
    return exam_request

# Obține cererile de examen
@router.get("/requests/", response_model=List[schemas.ExamRequest])
def get_exam_requests(
    student_id: int = None,
    professor_id: int = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Verifică dacă utilizatorul este profesor
    if current_user.role != "professor":
        raise HTTPException(status_code=403, detail="Only professors can view exam requests")

    exam_requests = crud.get_exam_requests(db=db, professor_id=current_user.id)
    if not exam_requests:
        raise HTTPException(status_code=404, detail="No exam requests found")
    return exam_requests

# Actualizează starea cererii de examen
@router.put("/requests/{request_id}/status")
def update_exam_request_status(
    request_id: int,
    status: str,  # Expected values: "approved" or "rejected"
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Verifică dacă utilizatorul este profesor
    if current_user.role != "professor":
        raise HTTPException(status_code=403, detail="Only professors can approve or reject exam requests")

    updated_request = crud.update_exam_request_status(db=db, request_id=request_id, status=status)
    if not updated_request:
        raise HTTPException(status_code=404, detail="Exam request not found")
    return {"message": "Exam request status updated successfully", "status": status}
