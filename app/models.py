from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship, Session
from .database import Base
from datetime import date


# Base User Model for Authentication
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)  # "student" or "professor"


class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    year_of_study = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class Professor(Base):
    __tablename__ = 'professors'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)  # Asigură-te că acest câmp există
    faculty_name = Column(String, nullable=True)
    department_name = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


# Exam Model
class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String)
    date = Column(Date)
    professor_id = Column(Integer, ForeignKey("professors.id"))

    professor = relationship("Professor")


# ExamRequest Model
class ExamRequest(Base):
    __tablename__ = 'exam_requests'

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    professor_id = Column(Integer, ForeignKey('professors.id'))
    classroom_id = Column(Integer, ForeignKey('classrooms.id'))
    requested_date = Column(Date)
    subject = Column(String)

    student = relationship("Student")
    professor = relationship("Professor")
    classroom = relationship("Classroom")

    @staticmethod
    def create_request_with_exam(db: Session, student_id: int, professor_id: int, classroom_id: int, requested_date: date, subject: str):
        # Creăm un nou examen
        new_exam = Exam(
            subject=subject,
            date=requested_date,
            professor_id=professor_id
        )
        db.add(new_exam)
        db.commit()
        db.refresh(new_exam)

        # Creăm un request folosind `exam_id` generat
        new_request = ExamRequest(
            student_id=student_id,
            professor_id=professor_id,
            classroom_id=classroom_id,
            requested_date=requested_date,
            subject=subject
        )
        db.add(new_request)
        db.commit()
        db.refresh(new_request)

        return new_request

class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    short_name = Column(String(50), nullable=False)
    building_name = Column(String(50), nullable=False)
