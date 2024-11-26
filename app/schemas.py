from pydantic import BaseModel
from datetime import date
from typing import Optional


class Exam(BaseModel):
    id: int  # `str` schimbat în `int` pentru consistență cu baza de date
    subject: str
    date: date  # `str` schimbat în `date` pentru a reflecta tipul real
    professor_id: int  # Schimbare din `professorId` în `professor_id` pentru consistență
    #student_id: Optional[int] = None  # Adăugare pentru a se alinia cu `ExamRequest`

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
    phone_number: str
    faculty_name: str
    department_name: str


class ExamCreate(BaseModel):
    subject: str
    date: date
    professor_id: int

    class Config:
        orm_mode = True


class ExamRequest(BaseModel):
    id: int
    student_id: int
    professor_id: int
    exam_id: int
    requested_date: date
    subject: str 

    class Config:
        from_attributes = True

class ExamRequestCreate(BaseModel):
    student_id: int
    professor_id: int
    exam_id: int
    classroom_id: int  # Adăugăm acest câmp
    requested_date: date
    subject: str

    class Config:
        from_attributes = True

class SettingsUpdate(BaseModel):
    notificationPreferences: Optional[str] = None
    language: Optional[str] = None
    theme: Optional[str] = None

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
