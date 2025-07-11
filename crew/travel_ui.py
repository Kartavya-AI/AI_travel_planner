_import_('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
sys.modules["sqlite3.dbapi2"] = sys.modules["pysqlite3.dbapi2"]
import streamlit as st
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


st.set_page_config(page_title="AI Travel Planner", layout="centered")

st.title("✈️ AI Travel Planner")
st.markdown("Plan your perfect trip using AI agents.")

with st.form("travel_form"):
    origin = st.text_input("Where are you traveling from?", "Bangalore, India")
    cities = st.text_input("City you're planning to visit", "Delhi, India")
    date_range = st.text_input("Trip date range", "2025-06-26 to 2025-07-02")
    interests = st.text_input("Your interests", "Street food and local culture")
    accommodation_budget = st.text_input("Accommodation Budget (e.g., '1000 INR/night')", "1000 INR/night")
    dietary_preferences = st.text_input("Dietary Preferences", "Both vegetarian and non-vegetarian options")
    food_budget = st.text_input("Food Budget (e.g., '500 INR/day')", "500 INR/day")
    
    submitted = st.form_submit_button("Generate Travel Plan")

if submitted:
    st.markdown("🚀 Generating your travel plan, please wait...")

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
        with st.expander("Debug Info"):
            st.write(f"Result type: {type(result)}")
            st.write(f"Result attributes: {dir(result)}")

    except Exception as e:
        st.error(f"❌ Error occurred: {e}")
        st.write(f"Error type: {type(e)}")
        st.write(f"Error details: {str(e)}")
