# import requests

# params = {
#   'access_key': '26d72d01a87bfb507b98935d52356e01'
# }

# api_result = requests.get('http://api.aviationstack.com/v1/flights?airline_name=American Airlines&dep_iata=LAX', params)

# api_response = api_result.json()

# # print(api_response)
# count = 0

# for flight in api_response['data']:
#     if (flight['departure']['delay'] != 'null'):
#         print(flight)
#         print('\n')
#         count+=1

# print (f"total flights = {count}")


import pandas as pd
import requests

params = {
    'access_key': '26d72d01a87bfb507b98935d52356e01'
}

api_result = requests.get('http://api.aviationstack.com/v1/flights?airline_name=American Airlines&dep_iata=LAX', params)

api_response = api_result.json()

# print(api_response)
delayed_flights = []

for flight in api_response['data']:
    if flight['departure']['delay'] != 'null':
        delayed_flights.append({
            'flight_date': flight['flight_date'],
            'flight_status': flight['flight_status'],
            'departure_airport': flight['departure']['airport'],
            'departure_delay': flight['departure']['delay'],
            'arrival_airport': flight['arrival']['airport'],
            'arrival_delay': flight['arrival']['delay']
        })

df = pd.DataFrame(delayed_flights)
print(df)
