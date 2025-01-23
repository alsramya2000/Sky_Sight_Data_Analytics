from dash import html, dcc, Output, Input, State, Dash
import logging

def get_flight_number_layout(app):
    logging.basicConfig(level=logging.INFO)

    layout = html.Div([
        html.H1('Sky Sight - Insightful Analysis of Air Travel!'),
        html.P('Check Flight Status'),
        dcc.Input(id='flight-number', type='text', placeholder='Enter Flight Number'),
        html.Button('Submit', id='submit-button', n_clicks=0),
        html.Div(id='log-output'),
        html.Div(id='flight-number-output')
    ])

    @app.callback(
        Output('flight-number-output', 'children'),
        Input('submit-button', 'n_clicks'),
        State('flight-number', 'value')
    )
    def update_flight_number_output(n_clicks, flight_number):
        if n_clicks > 0 and flight_number:
            logging.info(f'Flight number received: {flight_number}')
            return f"User's flight number = {flight_number}"
        return ''

    return layout
