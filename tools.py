#weather tool (geocoding and weather data retrieval)

import requests


# 1. geocoding tool

def weather_city(city):
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    
    geocoding_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }

    geocoding_response = requests.get(
            geocoding_url,
            params=geocoding_params
        )

    geocoding_data = geocoding_response.json()

    if "results" not in geocoding_data:
            return {
                "error": f"Could not find city: {city}"
            }
    location = geocoding_data["results"][0] 
    
    latitude = location["latitude"]
    longitude = location["longitude"]
    

# 2. weather data retrieval tool

    weather_url = "https://api.open-meteo.com/v1/forecast"
    
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m"
    }
    
    weather_response = requests.get(
        weather_url,
        params = weather_params
    )
    
    weather_data = weather_response.json()
    
    temperature = weather_data["current"]["temperature_2m"]
    
    return {
        "city": city,
        "temperature": temperature,
        "unit": "°C"
    }


def calculator(expression):
    try:
        return eval(expression)
    except Exception as e:
        return f"calculation exception {e}"