# llm_router.py

from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from database import get_session
from models import Ride
from llm_service import generate_reroute_command, get_gemini_response

router = APIRouter()

# --- Endpoint 1: Generate Reroute Command (Delivery Exception) ---

@router.post("/api/llm/reroute_command")
async def handle_delivery_exception(
    awb: str, 
    problem_description: str,
    session: Session = Depends(get_session)
):
    ride = session.get(Ride, awb)
    
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
        
    rider_id = ride.rider_id if ride.rider_id else "UNASSIGNED"
    destination = ride.delivery_address
    
    command = generate_reroute_command(
        awb=awb, 
        current_rider=rider_id, 
        destination=destination, 
        problem=problem_description
    )
    
    return {
        "awb": awb,
        "status": "Exception Handled",
        "llm_command": command,
        "message": "LLM command generated successfully."
    }

# --- Endpoint 2: Automated Rider Reassignment Suggestion ---

@router.post("/api/llm/reassign_suggestion")
async def suggest_reassignment(
    awb: str,
    session: Session = Depends(get_session)
):
    ride = session.get(Ride, awb)
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    if ride.status != "Pending":
        return {"message": f"Ride is already {ride.status}. No reassignment needed."}

    prompt = f"""
    A ride with AWB {awb} from {ride.pickup_address} to {ride.delivery_address} has been pending assignment. 
    There are 5 available riders: RIDER-101 (Rating 4.9), RIDER-102 (Rating 4.1, closer to pickup), 
    RIDER-103 (Rating 4.5), RIDER-104 (Rating 3.5), RIDER-105 (Rating 5.0, furthest away).
    
    **TASK:** Based on standard logistics efficiency (prioritizing proximity and rating), suggest the single best Rider ID to assign this ride to.
    
    **OUTPUT FORMAT:** Provide ONLY the Rider ID (e.g., RIDER-102).
    """

    suggested_rider_id = get_gemini_response(prompt)
    
    return {
        "awb": awb,
        "current_status": ride.status,
        "llm_suggestion": suggested_rider_id,
        "message": "LLM suggested rider for priority assignment."
    }