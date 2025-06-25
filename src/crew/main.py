from travelcrew import TravelCrew

# Set dynamic input values for the crew tasks
origin = "Banglore,India"
cities = "Delhi,India"
date_range = "2025-06-26 to 2025-07-02"
interests = "street food and local culture"
accommodation_budget = "1000 INR/night"
dietary_preferences = "both vegetarian and non-vegetarian options"
food_budget = "500 INR/day"

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
