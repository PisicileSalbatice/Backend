import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
from app.models import ExamRequest

# Gmail SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"  # Gmail SMTP server
SMTP_PORT = 587  # Port for TLS
EMAIL_ADDRESS = "timoteimoscaliucin@gmail.com"  # Your email address
EMAIL_PASSWORD = "mous qbom mkav ipqm"  # App Password (not your regular password)

def send_email(subject: str, body: str, recipient_email: str):
    """
    Trimite un email folosind configurarea SMTP.
    """
    try:
        # Construirea mesajului
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        # Adăugarea conținutului email-ului
        msg.attach(MIMEText(body, 'plain'))
        
        # Conectarea la serverul SMTP
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Activare TLS pentru securitate
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        
        # Trimiterea email-ului
        server.sendmail(EMAIL_ADDRESS, recipient_email, msg.as_string())
        server.quit()
        print(f"Email trimis cu succes către {recipient_email}")
    except Exception as e:
        print(f"Eroare la trimiterea email-ului: {e}")


def notify_exam_request_created(db: Session, request_id: int):
    """
    Trimite notificare atunci când o cerere de examen este creată,
    incluzând numele studentului și profesorului.
    """
    # Interogăm cererea de examen împreună cu relațiile student și profesor
    exam_request = (
    db.query(ExamRequest)
    .filter(ExamRequest.id == request_id)
    .join(ExamRequest.student)
    .join(ExamRequest.professor)
    .first()
    )

    print("Verificăm cererea de examen...")
    print(f"Request ID: {request_id}")

    if not exam_request:
        print("Cererea de examen nu a fost găsită.")
        return
    
    print("Cererea de examen a fost găsită.")


    # Preluăm numele studentului și profesorului
    student_name = f"{exam_request.student.first_name} {exam_request.student.last_name}"
    professor_name = f"{exam_request.professor.first_name} {exam_request.professor.last_name}"

    # Construim subiectul și corpul email-ului
    subject = "New Exam Request Notification"
    body = (
        f"A new exam request has been created:\n\n"
        f"Student: {student_name} (ID: {exam_request.student_id})\n"
        f"Subject: {exam_request.subject}\n"
        f"Date: {exam_request.requested_date}\n"
        f"Classroom ID: {exam_request.classroom_id}\n"
        f"Professor: {professor_name} (ID: {exam_request.professor_id})\n"
    )

    # Trimitem email-ul
    send_email(subject, body, EMAIL_ADDRESS)


def notify_exam_request_status_updated(db: Session, request_id: int, status: str):
    """
    Sends a notification when the status of an exam request is updated.
    """
    exam_request = db.query(ExamRequest).filter(ExamRequest.id == request_id).first()
    if not exam_request:
        print("Exam request not found.")
        return

    subject = "Exam Request Status Updated"
    body = (
        f"The status of the exam request has been updated:\n"
        f"Student ID: {exam_request.student_id}\n"
        f"Subject: {exam_request.subject}\n"
        f"Date: {exam_request.requested_date}\n"
        f"Classroom ID: {exam_request.classroom_id}\n"
        f"New Status: {status}\n"
    )
    send_email(subject, body)
