import requests
import os

# set global default units
units = 'metric'
temp_units = 'C'
speed_units = 'm/s'

common_codes = {
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden - You're not allowed to access this",
    404: "Not Found - That resource doesn't exist",
    429: "Too Many Requests - You're making requests too fast",
    500: "Internal Server Error - Something broke on the server",
    503: "Service Unavailable - Server is down or overloaded"
}

#--------------------------------------------------------------------------------------

def safe_api_call(city):
    """Make an API call with comprehensive error handling"""

    api_key = os.getenv('OPENWEATHER_API_KEY')

    if not api_key:
        print("Error: OPENWEATHER_API_KEY not set")
        return None

    # Build the URL with query parameters
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
        }

    try:
        # Your API call here
        response = requests.get(base_url, params=params, timeout=7) # add timeout otherwise it may never trigger
        
        # Check if successful
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"City '{city}' not found")
            return None
        elif response.status_code == 401:
            print(f"OPENWEATHER_API_KEY not set. Unauthorized.")
            return None
        else:
            print(f'Error: {response.status_code} {common_codes[response.status_code]}')
            return None
    
    except requests.exceptions.ConnectionError:
        print("Network error: Could not connect to the API")
    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
#--------------------------------------------------------------------------------------
def display_weather(data):
    # weather_data was sent to this function in main with "display_weather(weather_data)" so now weather_data = data
    """Display weather data in a nice format"""
    if not data:
        return

    # Extract the data we want
    city = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    description = data['weather'][0]['description']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    # Display it nicely
    print(f"\n{'='*50}")
    print(f"Weather in {city}, {country}")
    print(f"{'='*50}")
    print(f"Temperature: {temp} {temp_units} (feels like {feels_like} {temp_units})")
    print(f"Conditions: {description.capitalize()}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} {speed_units}")    

#--------------------------------------------------------------------------------------
def main():
    """Main program loop"""
    print("Weather Lookup App")

    while True:
        city = str(input("\nEnter a city name:\n"))
        if city=="":
            print("Entry cannot be blank. Please try again.")
        else:
            break            

    weather_data = safe_api_call(city)
    display_weather(weather_data)

if __name__ == "__main__":
    main()