import csv
from sqlalchemy.orm import Session
from app.models import Student
from app.database import SessionLocal

def import_students(file_path: str):
    db: Session = SessionLocal()
    try:
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                new_student = Student(
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    year_of_study=row['year_of_study'],
                )
                db.add(new_student)
        db.commit()
        print("Studenții au fost importați cu succes!")
    except Exception as e:
        db.rollback()
        print(f"Eroare la importarea studenților: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import_students("students.csv")
