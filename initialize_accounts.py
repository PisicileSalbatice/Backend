from sqlalchemy.orm import Session
from app.models import Student, Professor, User
from app.database import SessionLocal

def create_accounts():
    db: Session = SessionLocal()
    common_password = "student123"

    # Generate student accounts
    student_emails = [f"student{i}@student.usv.ro" for i in range(1, 31)]
    for i, email in enumerate(student_emails, start=1):
        user = User(email=email, password=common_password, role="student")
        db.add(user)
        db.flush()  # Ensure user ID is available

        student = Student(
            first_name=f"StudentFirst{i}",
            last_name=f"StudentLast{i}",
            email=email,
            year_of_study=1,
            user_id=user.id
        )
        db.add(student)

    # Generate professor accounts
    professor_emails = [f"professor{i}@usm.ro" for i in range(1, 21)]
    for i, email in enumerate(professor_emails, start=1):
        user = User(email=email, password=common_password, role="professor")
        db.add(user)
        db.flush()  # Ensure user ID is available

        professor = Professor(
            first_name=f"ProfessorFirst{i}",
            last_name=f"ProfessorLast{i}",
            email=email,
            user_id=user.id
        )
        db.add(professor)

    db.commit()
    db.close()
    print("Accounts have been successfully created!")

if __name__ == "__main__":
    create_accounts()
