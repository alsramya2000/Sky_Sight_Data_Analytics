import requests
import pandas as pd
from faker import Faker
import random

def get_real_time_flight_data(flight_number):
    params = {
        'access_key': '0e226f3354dc3c5e8f5ef012d48d7064',
        'airline_name': 'American Airlines',
        'dep_iata': 'LAX',
        'flight_number': flight_number,
        'flight_status': 'scheduled'
    }

    api_result = requests.get('http://api.aviationstack.com/v1/flights', params)

    api_response = api_result.json()

    if 'data' not in api_response or not api_response['data']:  # If API response is empty or missing 'data' key, create and return fake data
        fake = Faker()
        fake_data = [{
            'flight_date': fake.date_between(start_date='-0d', end_date='today').strftime('%Y-%m-%d'),
            'flight_status': 'scheduled',
            'departure_airport': 'Los Angeles International Airport',
            'departure_iata': 'LAX',
            'departure_terminal': random.choice(['1', '2', '3', '4', '5', '6']),
            'departure_gate': fake.random_int(min=1, max=100),
            'departure_delay': random.randint(-30, 30),
            'departure_timezone': 'America/Los_Angeles',
            'arrival_timezone': 'America/New_York',
            'arrival_airport': 'John F. Kennedy International Airport',
            'arrival_iata': 'JFK',
            'arrival_terminal': random.choice(['1', '2', '4', '5', '7']),
            'arrival_gate': fake.random_int(min=1, max=100),
            'arrival_baggage': fake.random_int(min=1, max=20),
            'arrival_delay': random.randint(-30, 30),
            'airline_name': 'American Airlines',
            'airline_iata': 'AA',
            'scheduled_departure': fake.date_time_this_year(),
            'estimated_departure': fake.date_time_this_year(),
            'actual_departure': None,
            'wind_speed': fake.random_int(min=0, max=30),
            'rain': fake.random_int(min=0, max=5),
            'snow': fake.random_int(min=0, max=5)
        }]
        return pd.DataFrame(fake_data)

    rt_flight_list = []

    for flight in api_response['data']:
        rt_flight_list.append({
            'flight_date': flight['flight_date'],
            'flight_status': flight['flight_status'],
            'departure_airport': flight['departure']['airport'],
            'departure_iata': flight['departure']['iata'],
            'departure_terminal': flight['departure']['terminal'],
            'departure_gate': flight['departure']['gate'],
            'departure_delay': flight['departure']['delay'],
            'departure_timezone': flight['departure']['timezone'],
            'arrival_timezone': flight['arrival']['timezone'],
            'arrival_airport': flight['arrival']['airport'],
            'arrival_iata': flight['arrival']['iata'],
            'arrival_terminal': flight['arrival']['terminal'],
            'arrival_gate': flight['arrival']['gate'],
            'arrival_baggage': flight['arrival']['baggage'],
            'arrival_delay': flight['arrival']['delay'],
            'airline_name': flight['airline']['name'],
            'airline_iata': flight['airline']['iata'],
            'scheduled_departure': flight['departure']['scheduled'],
            'estimated_departure': flight['departure']['estimated'],
            'actual_departure': flight['departure']['actual']
        })

    rt_flights = pd.DataFrame(rt_flight_list, index=None)

    # get weather data to append to rt_flights
    api_key = '25e172d6296ba2374cfc37101892fed4'
    lat = 33.942791
    lon = -118.410042

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'

    response = requests.get(url)
    weather_data = response.json()

    if 'wind' in weather_data:
        wind_speed = weather_data['wind']['speed']
        rt_flights['wind_speed'] = wind_speed

    if 'rain' in weather_data:
        rain = weather_data['rain'].get('3h', 0)
        rt_flights['rain'] = rain
    else:
        rt_flights['rain'] = 0

    if 'snow' in weather_data:
        snow = weather_data['snow'].get('3h', 0)
        rt_flights['snow'] = snow
    else:
        rt_flights['snow'] = 0

    return rt_flights


# Example usage
if __name__ == '__main__':
    flight_number = 1565
    rt_flights = get_real_time_flight_data(flight_number)
    print(rt_flights)
