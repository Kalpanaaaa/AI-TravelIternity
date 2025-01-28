import openai
import streamlit as st
from datetime import datetime, date
from PIL import Image

# Set your OpenAI API key
openai.api_key = "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"


# Streamlit UI - Enhanced Design
st.markdown(
    """
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #001f3f;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #0078d4;
            color: white;
            font-size: 18px;
            border-radius: 8px;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #160129;
        }
        .stTextInput>div>input {
            border-radius: 8px;
            padding: 10px;
            border: 1px solid #0078d4;
            background-color: #001f3f;
            color: #ffffff;
        }
        .stMarkdown {
            color: #ffffff;
            font-size: 16px;
        }
        .stForm {
            padding: 20px;
            background-color: #170224;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌍 AI Travel Itinerary Planner")
st.write("Plan your dream trip with ease! 🌟")

# Step 1: Understand the User Context
# Session state to store user inputs
if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "destination": None,
        "budget": None,
        "start_date": None,
        "end_date": None,
        "duration": None,
        "purpose": None,
        "preferences": None,
        "itinerary": None,
        "image": None,
    }

# Gather key user inputs
with st.form("trip_details"):
    st.session_state.user_data["destination"] = st.text_input("Destination", placeholder="Where are you planning to go?")
    st.session_state.user_data["budget"] = st.number_input("Budget (in INR)", min_value=1000, max_value=1000000, step=500)

    # Restrict start and end date selection
    today = date.today()
    st.session_state.user_data["start_date"] = st.date_input("Trip Start Date", min_value=today)
    st.session_state.user_data["end_date"] = st.date_input("Trip End Date", min_value=today)

    # Validate that end date is not before start date
    if st.session_state.user_data["start_date"] and st.session_state.user_data["end_date"]:
        start_date = st.session_state.user_data["start_date"]
        end_date = st.session_state.user_data["end_date"]

        if end_date < start_date:
            st.error("End date cannot be before the start date. Please select a valid range.")
        else:
            st.session_state.user_data["duration"] = (end_date - start_date).days + 1

    st.session_state.user_data["purpose"] = st.selectbox("Purpose of the Trip", ["Leisure", "Adventure", "Cultural", "Business", "Other"])
    st.session_state.user_data["preferences"] = st.text_area("Preferences", placeholder="E.g., food preferences, hidden gems, must-visit places")
    submitted = st.form_submit_button("Generate Itinerary")

# Step 2: Build Your Prompt System
def get_itinerary(destination, budget, duration, purpose, preferences):
    # System prompt for generating an itinerary
    system_prompt = (
        f"Generate a {duration}-day travel itinerary for a trip to {destination} with the following details:\n"
        f"Budget: {budget} INR\n"
        f"Purpose: {purpose}\n"
        f"Preferences: {preferences}\n"
        "Include top-rated attractions, hidden gems, dining options, and timing for activities each day. "
        "Consider the user's budget, mobility concerns, and dietary preferences."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI travel planner that generates detailed travel itineraries."},
            {"role": "user", "content": system_prompt},
        ]
    )
    return response.choices[0].message["content"]

def fetch_image(destination):
    # A placeholder function to fetch destination images
    image_map = {
        "Paris": "https://example.com/paris.jpg",
        "New York": "https://example.com/ny.jpg",
        "Tokyo": "https://example.com/tokyo.jpg",
    }
    return image_map.get(destination, "https://example.com/default.jpg")

# Generate itinerary if the form is submitted
if submitted:
    with st.spinner("Generating your travel itinerary..."):
        try:
            destination = st.session_state.user_data["destination"]
            budget = st.session_state.user_data["budget"]
            duration = st.session_state.user_data["duration"]
            purpose = st.session_state.user_data["purpose"]
            preferences = st.session_state.user_data["preferences"]

            # Generate the travel itinerary
            itinerary = get_itinerary(destination, budget, duration, purpose, preferences)
            st.session_state.user_data["itinerary"] = itinerary

            # Fetch destination image
            image_url = fetch_image(destination)
            st.session_state.user_data["image"] = image_url

            st.success("Itinerary generated successfully!")

        except Exception as e:
            st.error(f"Error: {str(e)}")

# Step 3: Display the Generated Itinerary
if st.session_state.user_data["itinerary"]:
    st.subheader("Your Travel Itinerary")

    if st.session_state.user_data["image"]:
        st.image(st.session_state.user_data["image"], use_container_width=True)

    st.markdown(st.session_state.user_data["itinerary"])

# Navigate to another page for displaying the itinerary
def show_itinerary_page():
    st.title("Your Travel Itinerary")
    if st.session_state.user_data["itinerary"]:
        if st.session_state.user_data["image"]:
            st.image(st.session_state.user_data["image"], use_container_width=True)
        st.markdown(st.session_state.user_data["itinerary"])
    else:
        st.error("No itinerary available. Please go back and generate one.")
