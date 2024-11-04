from pydantic import BaseModel
from datetime import date
from typing import Optional

class Exam(BaseModel):
    id: str
    subject: str
    date: str
    professorId: str
    studentId: Optional[str] = None

    class Config:
        orm_mode = True

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    year_of_study: int

class ProfessorCreate(BaseModel):
    first_name: str
    last_name: str
    email: str

class ExamCreate(BaseModel):
    subject: str
    date: date
    professor_id: int

class ExamRequestCreate(BaseModel):
    student_id: int
    professor_id: int
    subject: str
    requested_date: date

class SettingsUpdate(BaseModel):
    notificationPreferences: Optional[str] = None
    language: Optional[str] = None
    theme: Optional[str] = None

    class Config:
        from_attributes = True
