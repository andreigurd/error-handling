import requests
import os


#--------------------------------------------------------------------------------------

def safe_api_call(city):
    """Make an API call with comprehensive error handling"""

    api_key = os.getenv('OPENWEATHER_API_KEY')

    if not api_key:
        print("Error: OPENWEATHER_API_KEY not set")
        return None

    while True:
        try:
            city = str(input("\nEnter a city name:\n"))
            break            
        except ValueError:
            print("Invalid entry. Please try again.")

    # Build the URL with query parameters
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
        }

    try:
        # Your API call here
        response = requests.get(base_url, params=params)
        pass
    except requests.exceptions.ConnectionError:
        print("Network error: Could not connect to the API")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

