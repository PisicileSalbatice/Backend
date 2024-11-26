from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Classroom
import requests


# Funcția pentru descărcarea sălilor din API
def fetch_classrooms_from_url():
    URL = "https://orar.usv.ro/orar/vizualizare/data/sali.php?json"
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Aruncă eroare pentru coduri HTTP >= 400
        classrooms_data = response.json()
        return classrooms_data
    except Exception as e:
        print(f"Eroare la descărcarea sălilor din API: {e}")
        return []


# Funcția pentru popularea sălilor în baza de date
def populate_classrooms(db: Session):
    classrooms_data = fetch_classrooms_from_url()
    if not classrooms_data:
        print("Nu s-au găsit săli în API.")
        return

    for classroom in classrooms_data:
        try:
            # Verificăm și normalizăm datele
            classroom_id = int(classroom.get("id", 0))  # Dacă `id` lipsește, folosim 0
            name = classroom.get("name", "").strip() if classroom.get("name") else "Unknown"
            short_name = classroom.get("shortName", "").strip() if classroom.get("shortName") else "Unknown"
            building_name = classroom.get("buildingName", "").strip() if classroom.get("buildingName") else "Unknown"

            # Creăm instanța pentru bază de date
            new_classroom = Classroom(
                id=classroom_id,
                name=name,
                short_name=short_name,
                building_name=building_name
            )
            db.add(new_classroom)

        except Exception as e:
            print(f"Eroare la procesarea sălii: {classroom}. Detalii: {e}")

    try:
        db.commit()
        print("Sălile au fost populate cu succes.")
    except Exception as e:
        print(f"Eroare la salvarea sălilor în baza de date: {e}")
        db.rollback()


# Main-ul scriptului
if __name__ == "__main__":
    # Creăm o sesiune a bazei de date
    db = SessionLocal()
    try:
        populate_classrooms(db)  # Apelăm funcția pentru popularea sălilor
    finally:
        db.close()
