import requests
from sqlalchemy import create_engine, MetaData, Table
from unidecode import unidecode

# URL-ul pentru lista de profesori
URL = "https://orar.usv.ro/orar/vizualizare/data/cadre.php?json"

# Funcție pentru golirea tabelei 'professors'
def clear_professors_table():
    DATABASE_URL = "postgresql://postgres:student123@localhost/usv_exam_db"
    engine = create_engine(DATABASE_URL)
    metadata = MetaData()
    professors_table = Table('professors', metadata, autoload_with=engine)

    with engine.connect() as connection:
        try:
            connection.execute(professors_table.delete())
            print("Tabela 'professors' a fost golită cu succes.")
        except Exception as e:
            print(f"Eroare la golirea tabelei 'professors': {e}")

# Funcție pentru normalizarea textului (îndepărtează caracterele speciale)
def normalize_text(text):
    return unidecode(text).strip() if text else ""

# Descărcare și procesare JSON
def fetch_professors_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Va ridica o excepție pentru erori HTTP
        professors_data = response.json()
        print("JSON-ul descărcat:", professors_data)  # Debugging
        return professors_data
    except Exception as e:
        print(f"Eroare la descărcarea JSON-ului: {e}")
        return []

# Validare date pentru fiecare profesor
def validate_professor(professor):
    # Verificăm dacă toate câmpurile obligatorii sunt prezente și corecte
    if not professor.get('firstName') or not professor.get('lastName'):
        return False, "Nume lipsă"
    if professor.get('emailAddress') and '@' not in professor.get('emailAddress'):
        return False, "Email invalid"
    return True, None

# Inserare profesori în baza de date
def insert_professors_to_db(professors):
    DATABASE_URL = "postgresql://postgres:student123@localhost/usv_exam_db"
    engine = create_engine(DATABASE_URL)
    metadata = MetaData()
    professors_table = Table('professors', metadata, autoload_with=engine)

    with engine.connect() as connection:
        transaction = connection.begin()  # Începe o tranzacție
        try:
            for professor in professors:
                try:
                    # Validăm profesorul
                    is_valid, error_message = validate_professor(professor)
                    if not is_valid:
                        print(f"Profesor invalid: {professor}. Eroare: {error_message}")
                        continue

                    # Normalizăm textul
                    professor_data = {
                        'first_name': normalize_text(professor.get('firstName')),
                        'last_name': normalize_text(professor.get('lastName')),
                        'email': normalize_text(professor.get('emailAddress')),
                        'phone_number': normalize_text(professor.get('phoneNumber')),
                        'faculty_name': normalize_text(professor.get('facultyName')),
                        'department_name': normalize_text(professor.get('departmentName'))
                    }

                    print(f"Inserăm profesorul: {professor_data}")
                    connection.execute(professors_table.insert(), professor_data)
                    print(f"Profesor adăugat: {professor_data['first_name']} {professor_data['last_name']}")
                except Exception as e:
                    print(f"Eroare la adăugarea profesorului {professor.get('firstName', '')} {professor.get('lastName', '')}: {e}")
            
            transaction.commit()  # Confirmăm tranzacția
        except Exception as e:
            transaction.rollback()  # Anulăm tranzacția în caz de eroare
            print(f"Eroare în timpul inserării în baza de date: {e}")

# Integrarea completă
if __name__ == "__main__":
    try:
        # Ștergem conținutul vechi
        clear_professors_table()

        # Descărcăm și inserăm noile date
        professors = fetch_professors_from_url(URL)
        print("Profesori extrași:", professors)  # Debugging
        if professors:
            insert_professors_to_db(professors)
        else:
            print("Nu s-au găsit profesori în JSON.")
    except Exception as e:
        print(f"A apărut o eroare: {e}")
