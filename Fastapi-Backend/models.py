# models.py

from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
import uuid

# --- Base Models ---

# Location does not need a separate table, it can be embedded as JSON or a field, 
# but for a clean structured project, let's treat it as a dedicated Pydantic model.
class LocationBase(SQLModel):
    address: str
    city: str
    lat: float
    lng: float

# This Base class is used for creating new rides from the Customer API (later)
class RideCreate(SQLModel):
    pickup_address: str
    delivery_address: str
    distance: str
    price: float

# --- Database Models (with Primary Keys) ---

class Rider(SQLModel, table=True):
    # This is the Primary Key for the Rider table
    rider_id: str = Field(default=None, primary_key=True)
    
    # Required Fields
    name: str
    email: str
    phone: str
    
    # Optional Fields
    rating: float = Field(default=0.0)

class Ride(RideCreate, table=True):
    # This is the Primary Key for the Ride table (Auto-generated AWB)
    awb: Optional[str] = Field(default_factory=lambda: "AWB-" + str(uuid.uuid4())[:8], primary_key=True)
    
    # Redefining address/location fields as simple strings for easier SQL integration
    # (We can parse them into LocationBase for API responses)
    pickup_address: str
    delivery_address: str
    
    # Required Fields
    distance: str
    price: float
    
    # Foreign Key/Status Fields
    rider_id: Optional[str] = Field(default=None, foreign_key="rider.rider_id")
    status: str = Field(default="Pending")
    