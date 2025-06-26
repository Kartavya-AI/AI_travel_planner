from travelcrew import TravelCrew

# Set dynamic input values for the crew tasks
origin = input("Where are you traveling from? (e.g., Bangalore, India): ") or "Bangalore, India"
cities = input("City you're planning to visit (e.g., Delhi, India): ") or "Delhi, India"
date_range = input("Trip date range (e.g., 2025-06-26 to 2025-07-02): ") or "2025-06-26 to 2025-07-02"
interests = input("Your interests (e.g., Street food and local culture): ") or  "Street food and local culture"
accommodation_budget = input("Accommodation Budget (e.g., '1000 INR/night'): ") or "1000 INR/night"
dietary_preferences = input("Dietary Preferences (e.g., 'Both vegetarian and non-vegetarian options'): ") or "Both vegetarian and non-vegetarian options"
food_budget = input("Food Budget (e.g., '500 INR/day'): ") or "500 INR/day"
# Initialize the crew class
crew_instance = TravelCrew()

inputs = {
    "origin": origin,
    "cities": cities,
    "date_range": date_range,
    "interests": interests,
    "accommodation_budget": accommodation_budget,
    "dietary_preferences": dietary_preferences,
    "food_budget": food_budget
}
# Run the crew
result = crew_instance.crew().kickoff(inputs=inputs)

# Print final result
print("\n\n✅ Final Travel Plan Output:\n")
print(result)
