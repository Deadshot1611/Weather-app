import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get OpenWeatherMap API key from environment variables
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

# Function to get weather data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to get the appropriate weather icon
def get_weather_icon(weather_description):
    if 'rain' in weather_description:
        return 'fa-cloud-showers-heavy'
    elif 'clear' in weather_description:
        return 'fa-sun'
    elif 'cloud' in weather_description:
        return 'fa-cloud'
    elif 'thunderstorm' in weather_description:
        return 'fa-bolt'
    elif 'snow' in weather_description:
        return 'fa-snowflake'
    else:
        return 'fa-smog'

# Streamlit UI
def main():
    st.set_page_config(page_title="Current Weather App", page_icon=":sun_behind_rain_cloud:", layout="wide")

    st.markdown(
        """
        <style>
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css');
        .main {
            text-align: center;
        }
        .stButton button {
            width: 100%;
            text-align: center;
        }
        .weather-icon {
            font-size: 100px;
            margin: 20px 0;
        }
        .city-text {
            font-size: 24px;
        }
        .condition-text {
            font-size: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<h1 style='text-align: center;'>Current Weather App</h1>", unsafe_allow_html=True)

    city = st.text_input('Enter City Name', 'New York').strip()

    if st.button('Get Weather'):
        weather = get_weather(city)
        if weather:
            weather_description = weather['weather'][0]['description']
            weather_icon_class = get_weather_icon(weather_description)

            st.markdown(f"<h3 class='city-text' style='text-align: center;'>City: {weather['name']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='weather-icon' style='text-align: center;'><i class='fas {weather_icon_class}'></i></div>", unsafe_allow_html=True)
            st.markdown(f"<h4 class='condition-text' style='text-align: center;'>Temperature: {weather['main']['temp']}°C</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 class='condition-text' style='text-align: center;'>Weather: {weather_description.capitalize()}</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 class='condition-text' style='text-align: center;'>Humidity: {weather['main']['humidity']}%</h4>", unsafe_allow_html=True)
            st.markdown(f"<h4 class='condition-text' style='text-align: center;'>Wind Speed: {weather['wind']['speed']} m/s</h4>", unsafe_allow_html=True)
        else:
            st.error("City not found or API error.")

if __name__ == '__main__':
    main()
