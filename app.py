import streamlit as st
import requests
from g4f.client import Client
from gtts import gTTS
import tempfile

# ---------------------------
# Configuration & API Settings
# ---------------------------
API_KEY = "5b0d498b57a2899ac882b7f6b8544290"  # Replace with your OpenWeather API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

# Initialize the g4f client
client = Client()

# Custom system prompt to guide the AI's behavior
system_prompt = (
    "You are an AI assistant specialized in heritage exploration of Tamil Nadu. "
    "You help users discover cultural landmarks, provide real-time weather updates, "
    "offer voice-assisted feedback, and generate personalized travel itineraries. "
    "Your design is scalable and user-friendly, promoting accessibility, tourism, "
    "and cultural preservation. Your immersive experience caters to history enthusiasts, "
    "researchers, and travelers alike."
)


# ---------------------------
# Streamlit App Layout
# ---------------------------
st.title("AI-Powered Heritage Exploration: Tamil Nadu Cultural Landmarks")
st.markdown(
    "Discover the rich heritage of Tamil Nadu through real-time cultural landmark insights, "
    "weather updates, voice-assisted feedback, and personalized travel plans."
)

# Create tabs for different functionalities
tabs = st.tabs(["AI Chat Assistance", "Real-Time Weather Updates", "Personalized Travel Plans"])

# ---------------------------
# Tab 1: AI Chat Assistance
# ---------------------------
with tabs[0]:
    st.header("AI Chat Assistance")
    user_query = st.text_area("Enter your query:")
    
    if st.button("Get AI Response", key="chat"):
        if user_query.strip():
            # Prepare messages with system prompt and user query
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ]
            with st.spinner("Processing your query..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    web_search=False
                )
                ai_reply = response.choices[0].message.content
            st.markdown("### AI Response")
            st.write(ai_reply)
            
            # Convert AI response to speech
            tts = gTTS(ai_reply, lang='en')
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_file.name)
            st.audio(temp_file.name, format="audio/mp3")
        else:
            st.error("Please enter a query.")

# ---------------------------
# Tab 2: Real-Time Weather Updates
# ---------------------------
with tabs[1]:
    st.header("Real-Time Weather Updates")
    location = st.text_input("Enter a location in Tamil Nadu (e.g., Chennai, Madurai):")
    
    if st.button("Get Weather Update", key="weather"):
        if location.strip():
            complete_url = f"{BASE_URL}appid={API_KEY}&q={location}&units=metric"
            weather_response = requests.get(complete_url)
            if weather_response.status_code == 200:
                weather_data = weather_response.json()
                st.markdown(f"### Weather in {location.capitalize()}")
                st.write(f"**Temperature:** {weather_data['main']['temp']} °C")
                st.write(f"**Condition:** {weather_data['weather'][0]['description'].capitalize()}")
                st.write(f"**Humidity:** {weather_data['main']['humidity']}%")
                st.write(f"**Wind Speed:** {weather_data['wind']['speed']} m/s")
            else:
                st.error("Could not retrieve weather data. Please check the location name.")
        else:
            st.error("Please enter a location.")

# ---------------------------
# Tab 3: Personalized Travel Plans
# ---------------------------
with tabs[2]:
    st.header("Personalized Travel Plans")
    travel_preferences = st.text_area("Describe your travel preferences (e.g., interests, duration, type of activities):")
    
    if st.button("Get Travel Plan", key="travel"):
        if travel_preferences.strip():
            # Prepare messages to generate a travel plan using the system prompt
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Plan a personalized travel itinerary in Tamil Nadu with these preferences: {travel_preferences}"}
            ]
            with st.spinner("Generating your travel plan..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    web_search=False
                )
                travel_plan = response.choices[0].message.content
            st.markdown("### Your Personalized Travel Plan")
            st.write(travel_plan)
            
            # Convert travel plan to speech
            tts = gTTS(travel_plan, lang='en')
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_file.name)
            st.audio(temp_file.name, format="audio/mp3")
        else:
            st.error("Please describe your travel preferences.")
