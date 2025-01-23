import pandas as pd

def load_flight_data():
    # Read the CSV file
    data = pd.read_csv('/Users/surya/Desktop/DAV Final Project/Archive/flights_sample_3m.csv', index_col=None)

    # Filter the data for American Airlines flights from LAX
    data = data[(data['AIRLINE_CODE'] == 'AA') & (data['ORIGIN'] == 'LAX')]

    # Reset index
    data.reset_index(drop=True, inplace=True)

    # Convert columns to correct data types
    data['CANCELLED'] = data['CANCELLED'].astype(int)
    data['DIVERTED'] = data['DIVERTED'].astype(int)
    data['CRS_DEP_TIME'] = data['CRS_DEP_TIME'].astype(float)
    data['CRS_ARR_TIME'] = data['CRS_ARR_TIME'].astype(float)

    columns_to_clean = ['AIR_TIME', 'ELAPSED_TIME', 'ARR_DELAY', 'WHEELS_ON', 'ARR_TIME', 'TAXI_IN', 'TAXI_OUT', 'WHEELS_OFF', 'DEP_DELAY', 'DEP_TIME']
    data = data.dropna(subset=columns_to_clean)

    # Reset index
    data.reset_index(drop=True, inplace=True)

    return data

