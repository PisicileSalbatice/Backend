from sqlalchemy.orm import Session
from app import models
import csv

# Parole fixe pentru studenți și profesori
STUDENT_PASSWORD = "student123"
PROFESSOR_PASSWORD = "professor123"

def populate_users_and_students(db: Session, students_csv_path: str):
    try:
        with open(students_csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(f"Procesăm studentul: {row}")
                
                # Creăm un utilizator în tabela `users`
                new_user = models.User(
                    email=row['email'],
                    password=STUDENT_PASSWORD,
                    role="student"
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)

                print(f"Utilizator creat: {new_user}")

                # Creăm un student asociat utilizatorului
                new_student = models.Student(
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                year_of_study=int(row['year_of_study']),  # Asigură-te că este convertit în int
                user_id=new_user.id
)
                db.add(new_student)
                db.commit()  # Asigurăm commit-ul tranzacției
                print(f"Student adăugat: {new_student}")

        print("Studenții și utilizatorii lor au fost creați cu succes.")
    except Exception as e:
        print(f"Eroare la popularea studenților: {e}")




def populate_users_for_professors(db: Session):
    try:
        # Iterăm prin toți profesorii existenți
        professors = db.query(models.Professor).all()
        for professor in professors:
            # Verificăm dacă există deja un utilizator asociat
            existing_user = db.query(models.User).filter(models.User.email == professor.email).first()
            if not existing_user:
                # Creăm un utilizator în tabela `users`
                new_user = models.User(
                    email=professor.email,
                    password=PROFESSOR_PASSWORD,
                    role="professor"
                )
                db.add(new_user)
                db.commit()
                db.refresh(new_user)  # Obținem ID-ul generat

                # Asociem utilizatorul creat cu profesorul
                professor.user_id = new_user.id
                db.commit()
        print("Profesorii și utilizatorii lor au fost creați cu succes.")
    except Exception as e:
        print(f"Eroare la popularea profesorilor: {e}")


# Funcție principală
def main(db: Session):
    students_csv_path = "students.csv"
    print("Începem popularea bazei de date...")

    print("Populăm utilizatorii și studenții...")
    populate_users_and_students(db, students_csv_path)
    print("Populăm utilizatorii pentru profesori...")
    populate_users_for_professors(db)

    print(f"Utilizatori în baza de date: {db.query(models.User).all()}")
    print(f"Studenți în baza de date: {db.query(models.Student).all()}")



# Exemplu de utilizare
if __name__ == "__main__":
    from app.database import SessionLocal

    # Creăm o sesiune de conexiune cu baza de date
    db = SessionLocal()
    try:
        main(db)
    finally:
        db.close()
