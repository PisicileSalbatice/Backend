from pydantic import BaseModel
from datetime import date
from typing import Optional
import datetime

class UserDetails(BaseModel):
    id: int
    name: str
    email: str
    role: str
    password: Optional[str] = None

    class Config:
        from_attributes = True

class UpdateRequest(BaseModel):
    request_id: int
    status: str
    email: str

class Exam(BaseModel):
    id: int  # `str` schimbat în `int` pentru consistență cu baza de date
    subject: str
    date: date  # `str` schimbat în `date` pentru a reflecta tipul real
    professor_id: int  # Schimbare din `professorId` în `professor_id` pentru consistență
    #student_id: Optional[int] = None 
    student: Optional[UserDetails] = None
    class Config:
        orm_mode = True

class Student(BaseModel):
    id: int
    name: Optional[str]
    role: Optional[str]  
    email: str
    

    class Config:
        from_attributes = True


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    year_of_study: int


class ProfessorCreate(BaseModel):
    id: int
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
    subject: str
    requested_date: datetime.date
    status: str
    professor_id: int
    classroom_id: int

    class Config:
        orm_mode = True


class ExamRequestCreate(BaseModel):
    student_id: int
    professor_id: int
    classroom_id: int
    requested_date: date
    subject: str

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
