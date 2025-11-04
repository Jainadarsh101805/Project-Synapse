# llm_service.py

from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

try:
    # Initialize the client from the environment variable (GEMINI_API_KEY)
    client = genai.Client()
except Exception as e:
    print(f"Error initializing Gemini Client: {e}")
    client = None

def get_gemini_response(prompt: str) -> str:
    """Sends a prompt to the Gemini model and returns the text response."""
    if not client:
        return "LLM Service Unavailable (API Key Missing)"
        
    model = 'gemini-2.5-flash' 
    
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"LLM Error: {e}"


def generate_reroute_command(awb: str, current_rider: str, destination: str, problem: str) -> str:
    """
    Generates a command for a rider based on a delivery exception.
    """
    
    prompt = f"""
    You are an expert Logistics Dispatcher for Vengers Express. Your task is to provide a clear, concise command to the delivery rider.

    **Context:**
    - AWB: {awb}
    - Current Rider ID: {current_rider}
    - Delivery Location: {destination}
    - **Problem:** {problem}
    
    **TASK:** Provide only the command text. Do not use conversational language. The command must be actionable for the rider.

    **If the problem is 'Customer is not answering the phone/door':** Command the rider to deliver the parcel to a designated alternate address (e.g., neighbor's unit, security desk) and capture a photo as proof.
    
    **If the problem is 'Vehicle breakdown/Accident':** Command the rider to securely log their location and wait for a support vehicle, and state that the ride will be reassigned immediately.
    """
    
    return get_gemini_response(prompt)