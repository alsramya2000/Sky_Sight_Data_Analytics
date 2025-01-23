import dash
from dash import html, dcc, Output, Input
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from real_time import get_real_time_flight_data
from data_loader import load_flight_data

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H3('Enter Flight Number'),
    dcc.Input(id='flight-number', type='text', placeholder='Enter Flight Number'),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='flight-info-container'),
    html.Div(id='graph-container')
])

@app.callback(
    Output('flight-info-container', 'children'),
    Output('graph-container', 'children'),
    Input('submit-button', 'n_clicks'),
    Input('flight-number', 'value')
)
def update_flight_info_and_graph(n_clicks, flight_number):
    if n_clicks > 0 and flight_number:
        # Get real-time flight data
        rt_flights = get_real_time_flight_data(flight_number)

        # Get historical flight data
        data = load_flight_data()
        dest = str(rt_flights['arrival_iata'][0])
        dest_data = data[data['DEST'] == dest]
        dest_data['FL_DATE'] = pd.to_datetime(dest_data['FL_DATE'])
        dest_data['YEAR'] = dest_data['FL_DATE'].dt.year
        average_dep_delay_per_year = dest_data.groupby('YEAR')['DEP_DELAY'].mean().reset_index()
        average_arr_delay_per_year = dest_data.groupby('YEAR')['ARR_DELAY'].mean().reset_index()

        # Create flight info divs
        flight_info_divs = []
        flight_info = {
            'Flight Date': str(rt_flights['flight_date'][0]),
            'Status': str(rt_flights['flight_status'][0]),
            'Departure Airport': str(rt_flights['departure_airport'][0]),
            'Departure Terminal': str(rt_flights['departure_terminal'][0]),
            'Departure Delay': str(rt_flights['departure_delay'][0]),
            'Arrival Airport': str(rt_flights['arrival_airport'][0]),
            'Arrival Airport Code': str(rt_flights['arrival_iata'][0]),
            'Arrival Terminal': str(rt_flights['arrival_terminal'][0]),
            'Arrival Gate': str(rt_flights['arrival_gate'][0]),
            'Arrival Baggage': str(rt_flights['arrival_baggage'][0])
        }
        for key, value in flight_info.items():
            flight_info_divs.append(html.Div([html.P(f'{key}: {value}')]))
            
        fig12 = make_subplots(rows=1, cols=2, subplot_titles=('Average Departure Delay', 'Average Arrival Delay'))

        # Add bar traces to the subplots
        fig12.add_trace(
            go.Bar(x=average_dep_delay_per_year['YEAR'], y=average_dep_delay_per_year['DEP_DELAY'], name='Departure Delay'),
            row=1, col=1
        )

        fig12.add_trace(
            go.Bar(x=average_arr_delay_per_year['YEAR'], y=average_arr_delay_per_year['ARR_DELAY'], name='Arrival Delay'),
            row=1, col=2
        )

        # Update layout
        fig12.update_layout(title_text=f'Average Departure and Arrival Delay in past years for LAX to {dest}',
                            xaxis_title='Year',
                            yaxis_title='Average Delay (minutes)',
                            height=600,
                            showlegend=False)


        #chart 3
        flight_number = int(flight_number)
        filtered_df = data[data['FL_NUMBER'] == flight_number]

        melted_df = pd.melt(filtered_df, id_vars=['FL_DATE', 'FL_NUMBER', 'DEP_DELAY'],
                            value_vars=['DELAY_DUE_CARRIER', 'DELAY_DUE_WEATHER', 'DELAY_DUE_NAS',
                                        'DELAY_DUE_SECURITY', 'DELAY_DUE_LATE_AIRCRAFT'],
                            var_name='Delay Cause', value_name='Delay')
        fig3 = px.scatter(melted_df, x='FL_DATE', y='Delay', color='Delay Cause', 
                        title=f'Flight {flight_number} - Departure Delay vs. Date with Delay Cause',
                        labels={'FL_DATE': 'Flight Date', 'Delay': 'Delay (mins)', 'Delay Cause': 'Delay Cause'})

        fig45 = make_subplots(rows=1, cols=2, subplot_titles=('Average Delay', 'On-Time Performance'))

        # chart 4
        filtered_df = data[data['FL_NUMBER'] == int(flight_number)]
        departure_delay = filtered_df['DEP_DELAY'].mean()
        arrival_delay = filtered_df['ARR_DELAY'].mean()

        fig45.add_trace(go.Bar(
            x=['Departure Delay', 'Arrival Delay'],
            y=[departure_delay, arrival_delay],
            marker_color=['skyblue', 'lightgreen'],
            text=[f'{departure_delay:.2f} min', f'{arrival_delay:.2f} min'],
            textposition='auto',
            name='Average Delay'
        ), row=1, col=1)

        # chart 5
        filtered_df['DEP_DELAY'] = filtered_df['DEP_TIME'] - filtered_df['CRS_DEP_TIME']
        filtered_df['ARR_DELAY'] = filtered_df['ARR_TIME'] - filtered_df['CRS_ARR_TIME']

        total_flights = len(filtered_df)
        on_time_departures = len(filtered_df[filtered_df['DEP_DELAY'] <= 0])
        on_time_arrivals = len(filtered_df[filtered_df['ARR_DELAY'] <= 0])

        departure_on_time_percentage = (on_time_departures / total_flights) * 100
        arrival_on_time_percentage = (on_time_arrivals / total_flights) * 100

        categories = ['On-Time Departures', 'On-Time Arrivals']
        percentages = [departure_on_time_percentage, arrival_on_time_percentage]

        fig45.add_trace(go.Bar(
            x=categories,
            y=percentages,
            marker_color=['skyblue', 'lightgreen'],
            text=[f'{departure_on_time_percentage:.2f}%', f'{arrival_on_time_percentage:.2f}%'],
            textposition='auto',
            name='On-Time Performance'
        ), row=1, col=2)

        fig45.update_layout(
            title=f'Flight {flight_number} On-Time Performance Analysis',
            width=1200,
            height=600,
            showlegend=False
        )

        fig_pie = make_subplots(rows=1, cols=2, subplot_titles=('Departure Performance', 'Arrival Performance'), specs=[[{'type':'domain'}, {'type':'domain'}]])

        # Pie chart for departure performance
        departure_labels = ['On-Time Departures', 'Delayed Departures']
        departure_sizes = [on_time_departures, total_flights - on_time_departures]
        departure_fig = go.Figure(data=[go.Pie(labels=departure_labels, values=departure_sizes)])
        departure_fig.update_traces(marker=dict(colors=['lightgreen', 'purple']), hole=0.3)

        # Add the departure pie chart to the first subplot
        for trace in departure_fig.data:
            fig_pie.add_trace(trace, row=1, col=1)

        # Pie chart for arrival performance
        arrival_labels = ['On-Time Arrivals', 'Delayed Arrivals']
        arrival_sizes = [on_time_arrivals, total_flights - on_time_arrivals]
        arrival_fig = go.Figure(data=[go.Pie(labels=arrival_labels, values=arrival_sizes)])
        arrival_fig.update_traces(marker=dict(colors=['skyblue', 'salmon']), hole=0.3)

        # Add the arrival pie chart to the second subplot
        for trace in arrival_fig.data:
            fig_pie.add_trace(trace, row=1, col=2)

        # Update layout
        fig_pie.update_layout(title_text=f'On-Time/Delayed Performance for Flight {flight_number} throughout the years',
                            height=400,
                            width=800,
                            showlegend=False)


        # Combine flight info divs and graphs into a single div
        flight_info_and_graphs_div = html.Div([
            *flight_info_divs,
            dcc.Graph(figure=fig12),
            dcc.Graph(figure=fig3),
            dcc.Graph(figure=fig45),
            dcc.Graph(figure=fig_pie)
        ])

        

        return flight_info_and_graphs_div, ''

    return '', ''



if __name__ == '__main__':
    app.run_server(debug=True)
