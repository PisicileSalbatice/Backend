from sqlalchemy import Column, String, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base


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
    exam_id = Column(Integer, ForeignKey('exams.id'))  # Link to specific exam
    classroom_id = Column(Integer, ForeignKey('classrooms.id'))  # Adăugăm această linie
    requested_date = Column(Date)
    subject = Column(String)  # Am păstrat acest câmp

    student = relationship("Student")
    professor = relationship("Professor")
    exam = relationship("Exam")
    classroom = relationship("Classroom")  # Adăugăm relația către clasă


class Classroom(Base):
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    short_name = Column(String(50), nullable=False)
    building_name = Column(String(50), nullable=False)
