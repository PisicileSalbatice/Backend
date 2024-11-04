import sqlalchemy
from sqlalchemy import create_engine

# Înlocuiește 'username', 'password', 'localhost', și 'usv_exam_db' cu informațiile tale reale
DATABASE_URL = "postgresql+psycopg2://postgres:student123@localhost/usv_exam_db"

# Creează un engine pentru a testa conexiunea
engine = create_engine(DATABASE_URL)

try:
    # Încearcă să te conectezi la baza de date
    with engine.connect() as connection:
        print("Conexiunea a reușit!")
except Exception as e:
    print("Conexiunea a eșuat:", e)
