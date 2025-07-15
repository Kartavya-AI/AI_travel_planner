__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
sys.modules["sqlite3.dbapi2"] = sys.modules["pysqlite3.dbapi2"]
import streamlit as st
import os
from src.crew.travelcrew import TravelCrew

def format_itinerary(text: str) -> str:
    lines = text.split("\n")
    formatted_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("**") and stripped.endswith("**"):
            # Convert to h2
            formatted_lines.append("## " + stripped.strip("*"))
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

def set_api_keys(serper_key: str, gemini_key: str):
    """Set API keys as environment variables"""
    if serper_key:
        os.environ['SERPER_API_KEY'] = serper_key
    if gemini_key:
        os.environ['GEMINI_API_KEY'] = gemini_key

def validate_api_keys(serper_key: str, gemini_key: str) -> tuple[bool, str]:
    """Validate that API keys are provided"""
    if not serper_key or not serper_key.strip():
        return False, "Serper API key is required"
    if not gemini_key or not gemini_key.strip():
        return False, "Gemini API key is required"
    return True, ""

# Page configuration
st.set_page_config(page_title="AI Travel Planner", layout="centered")
st.title("✈️ AI Travel Planner")
st.markdown("Plan your perfect trip using AI agents.")

# API Keys Configuration Section
st.sidebar.header("🔑 API Configuration")
st.sidebar.markdown("Enter your API keys to use the travel planner:")

# Check if keys are already in environment (from previous session or .env file)
default_serper = os.environ.get('SERPER_API_KEY', '')
default_gemini = os.environ.get('GEMINI_API_KEY', '')

serper_api_key = st.sidebar.text_input(
    "Serper API Key",
    value=default_serper,
    type="password",
    help="Get your Serper API key from https://serper.dev"
)

gemini_api_key = st.sidebar.text_input(
    "Gemini API Key", 
    value=default_gemini,
    type="password",
    help="Get your Gemini API key from Google AI Studio"
)

# API key validation
api_keys_valid, validation_error = validate_api_keys(serper_api_key, gemini_api_key)

if not api_keys_valid:
    st.sidebar.error(validation_error)
    st.error("⚠️ Please configure your API keys in the sidebar to continue.")
    st.info("""
    **Required API Keys:**
    - **Serper API Key**: Sign up at [serper.dev](https://serper.dev) for web search functionality
    - **Gemini API Key**: Get it from [Google AI Studio](https://makersuite.google.com/app/apikey) for AI processing
    """)
    st.stop()

# Set API keys in environment
set_api_keys(serper_api_key, gemini_api_key)

# Success message for valid keys
st.sidebar.success("✅ API keys configured successfully!")

# Main travel planning form
with st.form("travel_form"):
    st.subheader("🗺️ Trip Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        origin = st.text_input("Where are you traveling from?", "Bangalore, India")
        cities = st.text_input("City you're planning to visit", "Delhi, India")
        date_range = st.text_input("Trip date range", "2025-06-26 to 2025-07-02")
        interests = st.text_input("Your interests", "Street food and local culture")
    
    with col2:
        accommodation_budget = st.text_input("Accommodation Budget (e.g., '1000 INR/night')", "1000 INR/night")
        dietary_preferences = st.text_input("Dietary Preferences", "Both vegetarian and non-vegetarian options")
        food_budget = st.text_input("Food Budget (e.g., '500 INR/day')", "500 INR/day")
    
    submitted = st.form_submit_button("🚀 Generate Travel Plan", use_container_width=True)

# Process form submission
if submitted:
    # Final validation before processing
    if not api_keys_valid:
        st.error("Please configure valid API keys before generating a travel plan.")
        st.stop()
    
    # Show loading state
    with st.spinner("🚀 Generating your travel plan, please wait..."):
        inputs = {
            "origin": origin,
            "cities": cities,
            "date_range": date_range,
            "interests": interests,
            "accommodation_budget": accommodation_budget,
            "dietary_preferences": dietary_preferences,
            "food_budget": food_budget
        }
        
        try:
            crew_instance = TravelCrew()
            result = crew_instance.crew().kickoff(inputs=inputs)
            
            st.success("✅ Your travel plan is ready!")
            
            # Extract string content from CrewOutput
            content = extract_crew_output(result)
            
            # Format and display the content
            formatted_content = format_itinerary(content)
            st.markdown(formatted_content)
            
            # Optional: Show debug info (remove in production)
            with st.expander("🔍 Debug Info"):
                st.write(f"Result type: {type(result)}")
                st.write(f"Result attributes: {dir(result)}")
                
        except Exception as e:
            st.error(f"❌ Error occurred: {e}")
            st.write(f"Error type: {type(e)}")
            st.write(f"Error details: {str(e)}")
            
            # Show troubleshooting tips
            with st.expander("🛠️ Troubleshooting Tips"):
                st.markdown("""
                **Common Issues:**
                - Invalid API keys: Check that your keys are correct and active
                - Rate limits: You might have exceeded API rate limits
                - Network issues: Check your internet connection
                - Invalid input format: Ensure all inputs are properly formatted
                """)

# Footer
st.markdown("---")
st.markdown("**Note**: Your API keys are stored only for this session and are not saved permanently.")
