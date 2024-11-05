from sqlalchemy.orm import Session
from app.models import User, Student, Professor
from app.database import SessionLocal
from app.routers.auth import get_password_hash  # Importă funcția de hash

def create_test_accounts():
    db: Session = SessionLocal()

    # Parolă comună pentru toate conturile de test, hash-uită înainte de salvare
    common_password = "password123"
    hashed_password = get_password_hash(common_password)  # Hash-uiește parola

    # Creare conturi de test pentru studenți
    students_data = [
        {"first_name": "Timotei", "last_name": "Moscaliuc", "email": "timotei@student.usv.ro", "year_of_study": 4},
        
    ]

    for student in students_data:
        # Creăm un utilizator de bază pentru fiecare student
        user = User(email=student["email"], password=hashed_password, role="student")
        db.add(user)
        db.flush()  # Salvează `user` și primește `user.id`

        # Adaugăm intrarea în tabela `students` asociată cu `user.id`
        db_student = Student(
            first_name=student["first_name"],
            last_name=student["last_name"],
            email=student["email"],
            year_of_study=student["year_of_study"],
            user_id=user.id
        )
        db.add(db_student)

    # Creare conturi de test pentru profesori
    professors_data = [
        {"first_name": "George", "last_name": "Mahalu", "email": "mahalu@usm.ro"},
        
    ]

    for professor in professors_data:
        # Creăm un utilizator de bază pentru fiecare profesor
        user = User(email=professor["email"], password=hashed_password, role="professor")
        db.add(user)
        db.flush()  # Salvează `user` și primește `user.id`

        # Adaugăm intrarea în tabela `professors` asociată cu `user.id`
        db_professor = Professor(
            first_name=professor["first_name"],
            last_name=professor["last_name"],
            email=professor["email"],
            user_id=user.id
        )
        db.add(db_professor)

    # Finalizează tranzacțiile
    db.commit()
    db.close()
    print("Conturile de test au fost create cu succes!")

if __name__ == "__main__":
    create_test_accounts()
