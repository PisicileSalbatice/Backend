from sqlalchemy.orm import Session
from app.database import engine
from app.models import User, Student

def create_users_from_students():
    session = Session(bind=engine)

    # Obține lista tuturor studenților fără utilizator asociat
    students = session.query(Student).filter(Student.user_id == None).all()

    for student in students:
        user = User(
            email=student.email,
            password="default_password",  # Parola implicită (trebuie schimbată ulterior)
            role="student",
        )
        session.add(user)
        session.commit()  # Trebuie să comit pentru a obține ID-ul utilizatorului

        # Asociază utilizatorul cu studentul
        student.user_id = user.id
        session.add(student)

    session.commit()
    session.close()
    print("Utilizatorii au fost creați cu succes din studenți!")

if __name__ == "__main__":
    create_users_from_students()
