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
    __tablename__ = "professors"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
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
    requested_date = Column(Date)
    subject = Column(String)  # Am adăugat acest câmp
    # Am eliminat câmpul `status`

    student = relationship("Student")
    professor = relationship("Professor")
    exam = relationship("Exam")
