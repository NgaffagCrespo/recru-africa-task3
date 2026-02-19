import requests


def fetch_weather(city, api_key):
    """
    Fetch current weather data from OpenWeather API.
.
    Parameters:
        city (str): City name (e.g., "Douala").
        api_key (str): OpenWeather API key.

    Returns:
        dict: Clean JSON with selected fields or error message.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raises HTTPError for bad responses
        data = response.json()

        # Extract only useful fields
        clean_data = {
            "city": data.get("name"),
            "temperature": data.get("main", {}).get("temp"),
            "weather": data.get("weather", [{}])[0].get("description"),
            "humidity": data.get("main", {}).get("humidity")
        }
        return clean_data

    except requests.exceptions.RequestException as e:
        # Handle network errors, timeouts, etc.
        return {"error": f"Network issue: {str(e)}"}
    except ValueError:
        # Handle JSON parsing errors
        return {"error": "Invalid response format"}
    except KeyError:
        # Handle missing fields
        return {"error": "Unexpected response structure"}
