from pathlib import Path
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from twilio.rest import Client

# 1. IMPORTS
# Ensure we import schemas so your create_patient route doesn't crash!
from . import models, database, schemas 
from .database import engine
from .routers import donors, patients

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# 2. INITIALIZE APP (Only Once!)
app = FastAPI(
    title="MedLink API",
    description="Backend for the MedLink Healthcare Platform",
    version="1.0.0"
)

# 3. SETUP CORS SECURITY
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. MOUNT STATIC FILES & TEMPLATES
BASE_DIR = Path(__file__).resolve().parent.parent.parent 
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

# Include your separate router files
app.include_router(donors.router)
app.include_router(patients.router)


# --- 5. TWILIO SMS SETUP ---
TWILIO_ACCOUNT_SID = "your_account_sid_here"
TWILIO_AUTH_TOKEN = "your_auth_token_here"
TWILIO_PHONE_NUMBER = "+1234567890" 

def send_confirmation_sms(user_phone: str, user_name: str, role: str):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Hello {user_name}! You have successfully registered with MedLink as a {role}. Thank you for joining our network.",
            from_=TWILIO_PHONE_NUMBER,
            to=user_phone
        )
        print(f"Message sent successfully: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")


# --- 6. ROUTES ---

@app.get("/")
def serve_home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/donor")
def serve_donor_page(request: Request):
    return templates.TemplateResponse(request=request, name="donor.html")

@app.get("/patient")
def serve_patient_page(request: Request):
    return templates.TemplateResponse(request=request, name="patient.html")

@app.get("/api/check-status/{phone_number}")
def check_user_status(phone_number: str, db: Session = Depends(database.get_db)):
    # Search Donor table
    donor = db.query(models.Donor).filter(models.Donor.phone_number == phone_number).first()
    if donor:
        return {"found": True, "type": "Donor", "name": donor.name, "blood_group": donor.blood_group}
    
    # Search Patient table
    patient = db.query(models.Patient).filter(models.Patient.phone_number == phone_number).first()
    if patient:
        return {"found": True, "type": "Patient", "name": patient.name, "blood_group": patient.blood_group}
        
    return {"found": False, "message": "No registration found for this number."}

@app.post("/api/patients/create") 
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(database.get_db)):
    # Save the patient to the database
    new_patient = models.Patient(**patient.dict())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    
    # Trigger the SMS confirmation
    send_confirmation_sms(new_patient.phone_number, new_patient.name, "Patient")
    
    return {"message": "Successfully registered"}