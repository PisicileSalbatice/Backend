from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas, crud, notifications
from app.database import get_db
from app.routers.auth import get_current_user, authenticate_user
from app.models import ExamRequest
from app.notifications import notify_exam_request_created, notify_exam_request_status_updated

import logging
router = APIRouter(prefix="/exams", tags=["exams"])
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
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
    request: schemas.ExamRequestCreate,
    email: str,
    password: str,
    db: Session = Depends(get_db),
):
    try:
        current_user = get_current_user(email, password, db)

        exam_request = ExamRequest.create_request_with_exam(
            db=db,
            student_id=request.student_id,
            professor_id=request.professor_id,
            classroom_id=request.classroom_id,
            requested_date=request.requested_date,
            subject=request.subject,
        )

        # Trimitere notificare pe email la cerere nouă
        notify_exam_request_created(db, exam_request.id)

        return exam_request
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")


# Obține cererile de examen
@router.get("/requests/", response_model=List[schemas.ExamRequest])
def get_exam_requests(
    student_id: int = None,
    professor_id: int = None,
    db: Session = Depends(get_db),
):
    print(f"Student ID: {student_id}, Professor ID: {professor_id}")
    requests = crud.get_exam_requests(db=db, student_id=student_id, professor_id=professor_id)
    if not requests:
        raise HTTPException(status_code=404, detail="No exam requests found")
    return requests

# Actualizează starea cererii de examen
@router.put("/requests/{request_id}/status")
def update_exam_request_status(
    request_id: int,
    status: str,  # "approved" sau "rejected"
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Verificăm dacă utilizatorul este profesor
    if current_user.role != "professor":
        raise HTTPException(status_code=403, detail="Doar profesorii pot actualiza statusul cererilor")

    # Actualizăm statusul cererii de examen
    updated_request = crud.update_exam_request_status(db=db, request_id=request_id, status=status)
    if not updated_request:
        raise HTTPException(status_code=404, detail="Cererea de examen nu a fost găsită")

    # Trimitem notificare studentului și pe email către admin
    notifications.notify_student_of_status(updated_request.student.email, status)
    notify_exam_request_status_updated(db, request_id, status)

    return {"message": f"Statusul cererii a fost actualizat la {status}", "status": status}


@router.delete("/requests/{request_id}", status_code=204)
def delete_exam_request(
    request_id: int,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    # Obține profesorul curent
    user = authenticate_user(email, password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if user.role != "professor":
        raise HTTPException(status_code=403, detail="Only professors can delete exam requests")

    # Verifică dacă cererea de examen există
    exam_request = db.query(models.ExamRequest).filter(models.ExamRequest.id == request_id).first()
    if not exam_request:
        raise HTTPException(status_code=404, detail="Exam request not found")

    # Verifică dacă profesorul curent este asociat cu cererea de examen
    if exam_request.professor_id != user.id:
        raise HTTPException(status_code=403, detail="You do not have permission to delete this request")

    # Șterge cererea din baza de date
    db.delete(exam_request)
    db.commit()

    return {"detail": "Exam request deleted successfully"}



