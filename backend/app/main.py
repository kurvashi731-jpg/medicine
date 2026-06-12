from .routers import donors, patients
from . import models
from .database import engine
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
# Make sure your models and database are imported!
from app import models, database 

app = FastAPI()
# Add this new GET route
@app.get("/api/check-status/{phone_number}")
def check_user_status(phone_number: str, db: Session = Depends(database.get_db)):
    
    # 1. First, search the Donor table
    donor = db.query(models.Donor).filter(models.Donor.phone_number == phone_number).first()
    if donor:
        return {
            "found": True, 
            "type": "Donor", 
            "name": donor.name,
            "blood_group": donor.blood_group
        }
    
    # 2. If not a donor, search the Patient table
    patient = db.query(models.Patient).filter(models.Patient.phone_number == phone_number).first()
    if patient:
        return {
            "found": True, 
            "type": "Patient", 
            "name": patient.name,
            "blood_group": patient.blood_group
        }
        
    # 3. If neither, return a not found message
    return {"found": False, "message": "No registration found for this number."}



# This is the security guard giving permission!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows requests from any frontend (Netlify, Live Server, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# 1. Initialize the FastAPI Application
app = FastAPI(
    title="MedLink API",
    description="Backend for the MedLink Healthcare Platform",
    version="1.0.0"
)

app.include_router(donors.router)
app.include_router(patients.router)


# 2. Setup CORS (Cross-Origin Resource Sharing)
# This allows your frontend to talk to your backend without security blocks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Path Configuration
# This dynamically finds the root folder so the backend knows where the frontend is
BASE_DIR = Path(__file__).resolve().parent.parent.parent 
FRONTEND_DIR = BASE_DIR / "frontend"

# 4. Mount Static Files & Templates
# Tells FastAPI where to find your style.css and script.js
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")

# Tells FastAPI where to find your index.html and donor.html
templates = Jinja2Templates(directory=str(FRONTEND_DIR / "templates"))

# 5. Your First Route (Serving the Frontend)
# 5. Your First Route (Serving the Frontend)
@app.get("/")
def serve_home(request: Request):
    # Notice the change inside the parentheses here:
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/donor")
def serve_donor_page(request: Request):
    # And the exact same change here:
    return templates.TemplateResponse(request=request, name="donor.html")

@app.get("/patient")
def serve_patient_page(request: Request):
    """
    Serve the patient page when the user navigates to /patient
    """
    return templates.TemplateResponse(request=request, name="patient.html")