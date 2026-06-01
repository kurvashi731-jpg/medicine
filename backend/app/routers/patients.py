from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(
    prefix="/api/patients",
    tags=["Patients"]
)

# CREATE a new patient
@router.post("/", response_model=schemas.PatientResponse)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(database.get_db)):
    existing_patient = db.query(models.Patient).filter(models.Patient.phone_number == patient.phone_number).first()
    if existing_patient:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    new_patient = models.Patient(**patient.model_dump()) 
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

# GET all patients
@router.get("/", response_model=list[schemas.PatientResponse])
def get_all_patients(db: Session = Depends(database.get_db)):
    patients = db.query(models.Patient).all()
    return patients