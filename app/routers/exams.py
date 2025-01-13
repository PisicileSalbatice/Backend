from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import models, schemas, crud, notifications
from app.database import get_db
from app.routers.auth import get_current_user, authenticate_user
from app.models import ExamRequest
from app.notifications import notify_exam_request_created, notify_exam_request_status_updated
from sqlalchemy.dialects import postgresql
import datetime

import logging
router = APIRouter(prefix="/exams", tags=["exams"])
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),  # Logare într-un fișier
        logging.StreamHandler(),          # Logare în consolă
    ],
)
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
        # Obține utilizatorul curent
        current_user = get_current_user(email, password, db)

        # Creează cererea de examen
        exam_request = ExamRequest.create_request_with_exam(
            db=db,
            student_id=request.student_id,
            professor_id=request.professor_id,
            classroom_id=request.classroom_id,
            requested_date=request.requested_date,
            subject=request.subject,
        )

        # Obține detalii despre student
        student = db.query(models.Student).filter(models.Student.id == request.student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        response = schemas.ExamRequest(
            id=exam_request.id,
            student=schemas.UserDetails(
                id=student.id,
                name=f"{student.first_name} {student.last_name}",
                email=student.email,
                role="student",
            ),
            professor_id=exam_request.professor_id,
            classroom_id=exam_request.classroom_id,
            requested_date=exam_request.requested_date,
            subject=exam_request.subject,
        )

        # Notificări
        notify_exam_request_created(db, exam_request.id)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")




# Obține cererile de examen
@router.get("/requests/", response_model=List[schemas.ExamRequest])
def get_exam_requests(
    student_id: Optional[int] = None,
    professor_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    logger.debug(f"Fetching exam requests for student_id: {student_id}, professor_id: {professor_id}")
    
    # Fetch exam requests
    requests = crud.get_exam_requests(db=db, student_id=student_id, professor_id=professor_id)
    if not requests:
        logger.warning(f"No exam requests found for student_id: {student_id} or professor_id: {professor_id}")
        raise HTTPException(status_code=404, detail="No exam requests found")
    
    # Convert requested_date to string
    formatted_requests = [
        {
            **req.__dict__,
            "requested_date": req.requested_date.isoformat() if isinstance(req.requested_date, datetime.date) else req.requested_date
        }
        for req in requests
    ]
    
    return formatted_requests


@router.get("/exams/student/{student_id}", response_model=List[schemas.ExamRequest])
def get_exams_for_student(student_id: int, db: Session = Depends(get_db)):
    """
    Fetch all exam requests for a given student_id.
    """
    # Query from the `exam_requests` table
    exam_requests = db.query(models.ExamRequest).filter(models.ExamRequest.student_id == student_id).all()
    
    # Debug log to confirm results
    logger.debug(f"Exam requests fetched for student_id {student_id}: {exam_requests}")

    # Handle case when no exam requests are found
    if not exam_requests:
        raise HTTPException(status_code=404, detail="No exam requests found for the given student ID")
    
    return exam_requests




# Actualizează starea cererii de examen
@router.put("/requests/{request_id}/status")
def update_exam_request_status(
    request_id: int,
    status: str = Query(..., description="Status to update (approved/rejected)"),
    email: str = Query(..., description="Email of the professor"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Validăm status-ul
    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status value. Use 'approved' or 'rejected'.")

    # Verificăm că utilizatorul este profesor
    if current_user.role != "professor":
        raise HTTPException(status_code=403, detail="Only professors can update the status of exam requests.")

    # Validăm email-ul utilizatorului
    if current_user.email != email:
        raise HTTPException(status_code=403, detail="Invalid email for the current user.")

    # Actualizăm statusul cererii
    updated_request = crud.update_exam_request_status(db=db, request_id=request_id, status=status)
    if not updated_request:
        raise HTTPException(status_code=404, detail="Exam request not found")

    # Trimitem notificarea către student
    student_email = updated_request.student.email
    notifications.notify_exam_request_status_updated(db, request_id, status)

    return {"message": f"Status of request {request_id} updated to {status}"}

    



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


@router.get("/user/details", response_model=schemas.UserDetails)
def get_user_details(email: str, db: Session = Depends(get_db)):
    """
    Returnează detaliile utilizatorului (student sau profesor) pe baza email-ului.
    """
    student = db.query(models.Student).filter(models.Student.email == email).first()
    if student:
        return {
            "id": student.id,
            "name": f"{student.first_name} {student.last_name}",
            "email": student.email,
            "role": "student",
            "password": student.user.password  # Adaugă parola din relația cu User
        }

    professor = db.query(models.Professor).filter(models.Professor.email == email).first()
    if professor:
        return {
            "id": professor.id,
            "name": f"{professor.first_name} {professor.last_name}",
            "email": professor.email,
            "role": "professor",
            "password": professor.user.password  # Adaugă parola din relația cu User
        }

    raise HTTPException(status_code=404, detail="User not found")

