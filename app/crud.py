from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional
from datetime import datetime
from app.models import ExamRequest
from fastapi import HTTPException

# Login: checks email and password
def login_user(db: Session, email: str, password: str) -> Optional[models.User]:
    return (
        db.query(models.User)
        .filter(models.User.email == email, models.User.password == password)
        .first()
    )


# crud.py

def get_exams(db: Session):
    return db.query(models.Exam).all()

# Fetch all exams associated with a specific student through their requests
def get_student_exams(db: Session, student_id: int) -> List[models.Exam]:
    return (
        db.query(models.Exam)
        .join(models.ExamRequest, models.ExamRequest.exam_id == models.Exam.id)
        .filter(models.ExamRequest.student_id == student_id)
        .all()
    )


# Create an exam request for a student
def create_exam_request(db: Session, request: schemas.ExamRequestCreate):
    try:
        print(f"Received request: {request.dict()}")  # Log payload-ul primit

        # Creăm un nou examen
        new_exam = models.Exam(
            subject=request.subject,
            date=request.requested_date,
            professor_id=request.professor_id
        )
        db.add(new_exam)
        db.commit()
        db.refresh(new_exam)

        # Creăm cererea de examen
        db_request = models.ExamRequest(
            student_id=request.student_id,
            professor_id=request.professor_id,
            exam_id=new_exam.id,  # Folosim ID-ul generat pentru examen
            classroom_id=request.classroom_id,
            requested_date=request.requested_date,
            subject=request.subject
        )
        db.add(db_request)
        db.commit()
        db.refresh(db_request)

        return db_request
    except Exception as e:
        print(f"Error in create_exam_request: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")




def get_exam_requests(db: Session, student_id: int = None, professor_id: int = None):
    query = db.query(models.ExamRequest)
    if student_id:
        query = query.filter(models.ExamRequest.student_id == student_id)
    if professor_id:
        query = query.filter(models.ExamRequest.professor_id == professor_id)
    return query.all()


def update_exam_request_status(db: Session, request_id: int, status: str) -> ExamRequest:
    exam_request = db.query(ExamRequest).filter(ExamRequest.id == request_id).first()
    if exam_request:
        exam_request.status = status
        db.commit()
        db.refresh(exam_request)
    return exam_request

# Fetch all exams registered and managed by a specific professor
def get_professor_exams(db: Session, professor_id: int) -> List[models.Exam]:
    return db.query(models.Exam).filter(models.Exam.professor_id == professor_id).all()


# Fetch all student exam requests for a specific professor
def get_student_requests(db: Session, professor_id: int) -> List[models.ExamRequest]:
    return (
        db.query(models.ExamRequest)
        .filter(models.ExamRequest.professor_id == professor_id)
        .all()
    )


# Update the status of an exam request (e.g., approve or reject)
def update_exam_request_status(
    db: Session, request_id: int, status: str
) -> Optional[models.ExamRequest]:
    db_request = (
        db.query(models.ExamRequest).filter(models.ExamRequest.id == request_id).first()
    )
    if db_request:
        db_request.status = status
        db.commit()
        db.refresh(db_request)
    return db_request


# Retrieve contact information (simulated for backend)
def get_contact_info() -> dict:
    return {
        "email": "support@usv_exam_planner.com",
        "phone": "+1234567890",
        "address": "USV Campus, Room 101",
        "supportHours": "Mon-Fri 9:00-17:00",
    }


# Retrieve user settings (simulated)
def get_user_settings(user_id: int) -> dict:
    # Example of preset settings for testing
    return {
        "userId": user_id,
        "notificationPreferences": "email",
        "language": "en",
        "theme": "light",
    }


# Update user settings
def update_user_settings(
    db: Session, user_id: int, settings: schemas.SettingsUpdate
) -> dict:
    # Find user by ID
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    # Update fields present in `settings`
    if settings.notificationPreferences is not None:
        user.notificationPreferences = settings.notificationPreferences
    if settings.language is not None:
        user.language = settings.language
    if settings.theme is not None:
        user.theme = settings.theme

    # Save changes
    db.commit()
    db.refresh(user)
    return {"message": "Settings updated successfully"}

def create_exam(db: Session, exam: schemas.ExamCreate):
    db_exam = models.Exam(
        subject=exam.subject,
        date=exam.date,
        professor_id=exam.professor_id
    )
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)
    return db_exam




