# main.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

# **CRITICAL FIX:** Ensure ALL database components are imported correctly, especially 'engine'.
from database import create_db_and_tables, get_session, engine 

# LLM Feature Imports (Assuming llm_router.py is saved)
from models import Rider, Ride, LocationBase, RideCreate
from llm_router import router as llm_router 

import uuid

# --- 1. Initialization ---

app = FastAPI()

# Include the LLM router to make those endpoints available
app.include_router(llm_router) 

# Configure CORS (Important for your frontend)
origins = [
    "http://127.0.0.1:5500", 
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 2. Database Startup Event ---

@app.on_event("startup")
def on_startup():
    """Ensure the database tables are created and seeded when the application starts."""
    create_db_and_tables()
    
    # Session must be initialized with the 'engine' object
    with Session(engine) as session:
        # Check if the mock rider exists
        existing_rider = session.get(Rider, "RIDER-001")
        if not existing_rider:
            mock_rider = Rider(
                rider_id="RIDER-001",
                name="Alex Rider",
                email="alex@vengers.com",
                phone="+65 9123 4567",
                rating=4.8
            )
            session.add(mock_rider)
        
        # Check if a pending ride exists
        existing_ride_query = select(Ride).where(Ride.status == "Pending")
        existing_ride = session.exec(existing_ride_query).first()
        if not existing_ride:
            mock_ride = Ride(
                pickup_address="15 Some Rd, Central District",
                delivery_address="789 Another St, Hollywood",
                distance="15.2 km",
                price=12.50
            )
            session.add(mock_ride)
        
        session.commit()
        print("Database seeded with mock data.")


# --- 3. Core API Endpoints (Rider and Customer) ---

@app.get("/")
async def read_root():
    """Simple health check endpoint."""
    return {"message": "Welcome to the Vengers Express API! (SQLModel Active)"}

# --- CUSTOMER ENDPOINT (This is the one you need to see!) ---
@app.post("/api/customer/create_ride", status_code=201)
async def create_ride(ride_data: RideCreate, session: Session = Depends(get_session)):
    """Allows a customer to create a new delivery request."""
    
    db_ride = Ride.model_validate(ride_data)
    db_ride.status = "Pending"
    
    session.add(db_ride)
    session.commit()
    session.refresh(db_ride)
    
    return {"message": "Ride successfully created and pending assignment", "awb": db_ride.awb}
# --- END CUSTOMER ENDPOINT ---


@app.post("/api/rider/login")
async def rider_login(rider_id: str, session: Session = Depends(get_session)):
    """Authenticates a rider and retrieves their profile from the database."""
    rider = session.get(Rider, rider_id)
    
    if not rider:
        # If rider doesn't exist, create a new one (simulating auto-registration)
        rider = Rider(
            rider_id=rider_id,
            name=f"New Rider {rider_id}",
            email=f"{rider_id.lower()}@vengers.com",
            phone="N/A",
            rating=5.0
        )
        session.add(rider)
        session.commit()
        session.refresh(rider)

    return {"message": "Login successful", "rider_id": rider.rider_id, "rider_profile": rider.model_dump()}

@app.get("/api/rides/pending")
async def get_pending_ride(session: Session = Depends(get_session)):
    """Returns the first ride with status 'Pending' using a database query."""
    
    ride = session.exec(
        select(Ride).where(Ride.status == "Pending")
    ).first()
    
    if ride:
        return ride.model_dump()
    
    return {"message": "No pending rides available."}

@app.post("/api/rides/{awb}/accept")
async def accept_ride(awb: str, rider_id: str, session: Session = Depends(get_session)):
    """Updates a ride status to 'Accepted' in the database."""
    
    ride = session.get(Ride, awb)
    
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    if ride.status != "Pending":
        raise HTTPException(status_code=400, detail=f"Ride status is already '{ride.status}'")

    ride.status = "Accepted"
    ride.rider_id = rider_id
    
    session.add(ride)
    session.commit()
    session.refresh(ride)
    
    return {"message": "Ride accepted", "ride": ride.model_dump()}

@app.post("/api/rides/{awb}/collect")
async def collect_parcel(awb: str, session: Session = Depends(get_session)):
    """Updates a ride status to 'Parcel Collected'."""
    ride = session.get(Ride, awb)
    
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")

    ride.status = "Parcel Collected"
    session.add(ride)
    session.commit()
    session.refresh(ride)
    
    return {"message": "Parcel collected successfully", "ride": ride.model_dump()}

@app.post("/api/rides/{awb}/deliver")
async def deliver_parcel(awb: str, session: Session = Depends(get_session)):
    """Finalizes a delivery by setting status to 'Delivered'."""
    ride = session.get(Ride, awb)
    
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")

    ride.status = "Delivered"
    session.add(ride)
    session.commit()
    session.refresh(ride)
    
    return {"message": "Parcel delivered successfully", "ride": ride.model_dump()}