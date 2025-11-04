# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uuid

# Initialize the FastAPI app
app = FastAPI()

# Configure CORS to allow your frontend to connect
origins = [
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database to simulate a real database for now
rides_db = {}
riders_db = {}

# Pydantic models to define the data structure
class Location(BaseModel):
    address: str
    city: str
    lat: float
    lng: float

class RideStatus(BaseModel):
    status: str
    eta: Optional[int] = None

class RideDetails(BaseModel):
    awb: str
    pickup: Location
    delivery: Location
    rider_id: Optional[str] = None
    status: str = "Pending"
    distance: str
    price: float

class RiderProfile(BaseModel):
    rider_id: str
    name: str
    email: str
    phone: str
    rating: float = 0.0

# Initial "dummy" data to start with
mock_ride_id = "AWB-" + str(uuid.uuid4())[:8]
rides_db[mock_ride_id] = RideDetails(
    awb=mock_ride_id,
    pickup=Location(address="15 Some Rd", city="Central District", lat=34.0522, lng=-118.2437),
    delivery=Location(address="789 Another St", city="Hollywood", lat=34.0983, lng=-118.3256),
    status="Pending",
    distance="15.2 km",
    price=12.50
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Vengers Express API!"}

@app.post("/api/rider/login")
async def rider_login(rider_id: str):
    rider_info = {
        "rider_id": rider_id,
        "name": "Alex Rider",
        "email": "alex@vengers.com",
        "phone": "+65 9123 4567",
        "rating": 4.8
    }
    riders_db[rider_id] = RiderProfile(**rider_info)
    return {"message": "Login successful", "rider_id": rider_id, "rider_profile": rider_info}

@app.get("/api/rides/pending")
async def get_pending_ride():
    for ride_id, ride in rides_db.items():
        if ride.status == "Pending":
            return ride
    return {"message": "No pending rides available."}

@app.post("/api/rides/{awb}/accept")
async def accept_ride(awb: str, rider_id: str):
    if awb not in rides_db:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    ride = rides_db[awb]
    if ride.status != "Pending":
        raise HTTPException(status_code=400, detail=f"Ride status is already '{ride.status}'")

    ride.status = "Accepted"
    ride.rider_id = rider_id
    return {"message": "Ride accepted", "ride": ride}

@app.post("/api/rides/{awb}/pass")
async def pass_ride(awb: str):
    if awb not in rides_db:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    ride = rides_db[awb]
    ride.status = "Passed"
    return {"message": "Ride passed"}

@app.post("/api/rides/{awb}/collect")
async def collect_parcel(awb: str):
    if awb not in rides_db:
        raise HTTPException(status_code=404, detail="Ride not found")

    ride = rides_db[awb]
    ride.status = "Parcel Collected"
    return {"message": "Parcel collected successfully"}

@app.post("/api/rides/{awb}/deliver")
async def deliver_parcel(awb: str):
    if awb not in rides_db:
        raise HTTPException(status_code=404, detail="Ride not found")

    ride = rides_db[awb]
    ride.status = "Delivered"
    return {"message": "Parcel delivered successfully"}