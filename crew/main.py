from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging
from src.crew.travelcrew import TravelCrew

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Travel Planner API",
    description="Plan your perfect trip using AI agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TravelPlanRequest(BaseModel):
    origin: str = Field(..., description="Where you're traveling from", example="Bangalore, India")
    cities: str = Field(..., description="City you're planning to visit", example="Delhi, India")
    date_range: str = Field(..., description="Trip date range", example="2025-06-26 to 2025-07-02")
    interests: str = Field(..., description="Your interests", example="Street food and local culture")
    accommodation_budget: str = Field(..., description="Accommodation budget", example="1000 INR/night")
    dietary_preferences: str = Field(..., description="Dietary preferences", example="Both vegetarian and non-vegetarian options")
    food_budget: str = Field(..., description="Food budget", example="500 INR/day")

class TravelPlanResponse(BaseModel):
    success: bool
    message: str
    itinerary: Optional[str] = None
    formatted_itinerary: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    message: str

# Utility functions
def format_itinerary(text: str) -> str:
    """Format the itinerary text for better readability"""
    lines = text.split("\n")
    formatted_lines = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("**") and stripped.endswith("**"):
            # Convert to h1 (main heading)
            formatted_lines.append("# " + stripped.strip("*"))
        elif stripped.startswith("*   "):
            # Convert to bullet
            formatted_lines.append("- " + stripped[4:])
        elif stripped.startswith("* "):
            formatted_lines.append("- " + stripped[2:])
        elif stripped.startswith("    *"):
            # Sub-bullet
            formatted_lines.append("  - " + stripped.strip("*").strip())
        else:
            formatted_lines.append(line)
    
    return "\n".join(formatted_lines)

def extract_crew_output(result) -> str:
    """Extract string content from CrewOutput object"""
    try:
        # Try different attributes that might contain the output
        if hasattr(result, 'raw'):
            return str(result.raw)
        elif hasattr(result, 'output'):
            return str(result.output)
        elif hasattr(result, 'result'):
            return str(result.result)
        elif hasattr(result, 'content'):
            return str(result.content)
        else:
            # Fallback to string conversion
            return str(result)
    except Exception:
        return str(result)

# API Routes
@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AI Travel Planner API",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="AI Travel Planner API is running"
    )

@app.post("/generate-travel-plan", response_model=TravelPlanResponse)
async def generate_travel_plan(request: TravelPlanRequest):
    """
    Generate a travel plan based on the provided requirements
    """
    try:
        logger.info(f"Generating travel plan for: {request.cities}")
        
        # Prepare inputs for the crew
        inputs = {
            "origin": request.origin,
            "cities": request.cities,
            "date_range": request.date_range,
            "interests": request.interests,
            "accommodation_budget": request.accommodation_budget,
            "dietary_preferences": request.dietary_preferences,
            "food_budget": request.food_budget
        }
        
        # Initialize and run the travel crew
        crew_instance = TravelCrew()
        result = crew_instance.crew().kickoff(inputs=inputs)
        
        # Extract and format the content
        content = extract_crew_output(result)
        formatted_content = content
        
        logger.info("Travel plan generated successfully")
        
        return TravelPlanResponse(
            success=True,
            message="Travel plan generated successfully",
            itinerary=content,
            formatted_itinerary=formatted_content
        )
        
    except Exception as e:
        logger.error(f"Error generating travel plan: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating travel plan: {str(e)}"
        )

@app.get("/sample-request", response_model=TravelPlanRequest)
async def get_sample_request():
    """Get a sample request for testing"""
    return TravelPlanRequest(
        origin="Bangalore, India",
        cities="Delhi, India",
        date_range="2025-06-26 to 2025-07-02",
        interests="Street food and local culture",
        accommodation_budget="1000 INR/night",
        dietary_preferences="Both vegetarian and non-vegetarian options",
        food_budget="500 INR/day"

    )
