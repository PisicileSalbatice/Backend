from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional
from datetime import datetime


# Login: checks email and password
def login_user(db: Session, email: str, password: str) -> Optional[models.User]:
    return (
        db.query(models.User)
        .filter(models.User.email == email, models.User.password == password)
        .first()
    )


# Fetch all exams associated with a specific student through their requests
def get_student_exams(db: Session, student_id: int) -> List[models.Exam]:
    return (
        db.query(models.Exam)
        .join(models.ExamRequest, models.ExamRequest.exam_id == models.Exam.id)
        .filter(models.ExamRequest.student_id == student_id)
        .all()
    )


# Create an exam request for a student
def create_exam_request(
    db: Session, request: schemas.ExamRequestCreate
) -> models.ExamRequest:
    db_request = models.ExamRequest(
        student_id=request.student_id,
        professor_id=request.professor_id,
        exam_id=request.exam_id,  # Link to a specific exam
        requested_date=request.requested_date,
        status="pending",
    )
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


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
