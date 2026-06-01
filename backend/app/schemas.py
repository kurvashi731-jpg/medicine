from pydantic import BaseModel
from typing import Optional

# 1. The Base Schema: Shared properties for a Donor
class DonorBase(BaseModel):
    name: str
    blood_group: str
    phone_number: str
    
    # Location fields (Optional, in case they don't share location immediately)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = "Ranchi"

# 2. The Create Schema: Used when the frontend sends a new donor to be saved
class DonorCreate(DonorBase):
    pass # It inherits everything exactly as it is in DonorBase

# 3. The Response Schema: Used when the backend sends a donor BACK to the frontend
class DonorResponse(DonorBase):
    id: int # The database will generate this ID, so we add it here

    class Config:
        # This tells Pydantic to understand our SQLAlchemy database models
        from_attributes = True
        
# (Make sure 'from pydantic import BaseModel' is at the top of your file too!)

# ... your Donor schemas should be up here ...

class PatientBase(BaseModel):
    name: str
    age: int
    blood_group: str
    phone_number: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    city: Optional[str] = "Ranchi"
    symptoms: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int

    class Config:
        from_attributes = True