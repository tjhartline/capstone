'''
# app.py
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ** Author:          Tammy Hartline                                                                       |
|  ** Version:         2.0.9                                                                                |
|  ** Description:     This file is meant to initialize the database functionality for the web application. |
|  ** Instructions:    Open CMD line -> navigate to app location (cd \path\to\repo\) -> run [python app.py] |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|                                            Changelog:                                                     |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start -- 01/2024 - TH                                                                               |
|  [Converted jupyter notebook file into a Python application file to more easily integrate as web          |
|  application instead of hosting locally.]                                                                 |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start -- 02/2024 - TH                                                                               |
|  [Updated language to call the new animal_shelter.py import, versus previous module.py.]                  |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start -- 02/2024 - TH                                                                               |
|  [Corrected filters and continuously debugging to determine what is causing them to not function          |
|  properly if they function at all.]                                                                       |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start --02/2024 - TH                                                                                |
|  [Added enhancements as planned, but still running into buggy application issues.]                        |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|                                            Notes:                                                         |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|   02/05/2024                                                                                              |
|   Notes for next assignments and TODOS: Figure out why the code is not launching the web application.     |
|   Current Issues: The code is not launching the web application at all. Either it returns                 |
|   Not found, or it returns a 504 error page. Cannot continue to test until I can get it to deploy.        |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|   02/07/2024                                                                                              |
|   Update: After several alterations, and updating the final call to the app.run_server method,            |
|   the application is now launching.                                                                       |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|   02/11/2024                                                                                              |
|   Notes for next assignments and TODOS: Debugging and testing the application                             |
|   Current Issues: Filters are not functioning properly. The data is not being filtered as expected.       |
|   When clicking on any filter, or using the text filter, the data is not changed, or sorted.              |
|   It also does not populate the graph with the correct data.                                              |
|   Continue altering the code and testing to find the issue and continue adding enhancements.              |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
'''

from sre_parse import State
from dash import Dash, html, dcc, dash_table  # Importing necessary Dash components
import dash  # Importing Dash
import dash_leaflet as dl
from dash.dependencies import Input, Output, State  # Importing Dash callback functions
import plotly.express as px  # Importing Plotly Express for data visualization
import pandas as pd
from traitlets import dlink  # Importing Pandas for data manipulation
from animal_shelter import AnimalShelter  # Importing AnimalShelter class for data access
import base64  # Importing base64 for image encoding

# Data Manipulation / Model
db_path = 'animals.db'
username = 'aacuser'
password = 'securepassword'

shelter = AnimalShelter(db_path=db_path, username=username, password=password)

# Class read method must support return of a list object and accept projection JSON input.
# Using an empty projection and query to retrieve all records
df = pd.DataFrame.from_records(shelter.read(projection=None, query=None))

# Check if animal id exists before dropping
if 'animal_id' in df.columns:
    df.drop(columns=['animal_id'], inplace=True)

# Get distinct animal types for filter
unq_animal_types = df['animal_type'].copy() if 'animal_type' in df.columns else None

# Setup Dash
app = Dash(__name__)

# Define authenticate function
def authenticate(username, password):
    valid_users = {'admin': 'adminPassword', 'aacuser': 'securepassword'}

    if username in valid_users and valid_users[username] == password:
        username = username
        password = password
        return True
    else:
        return False

# Add in Grazioso Salvare’s logo
image_filename = 'Grazioso_Salvare_Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
data = df.to_dict('records')

# Define layout
app.layout = html.Div([
    html.Center(html.B(html.H1('Capstone Project Dashboard'))),
    html.Center(html.B(html.H1("Tammy Hartline's Grazioso Salvare DashBoard Final Project"))),
    html.Hr(),

    # Row 1: Header and Photo
    html.Div([
        html.Div(id='header', className='col-6', style={'text-align': 'center'}),
        html.Div([
            html.Img(id='customer-logo', src='data:image/png;base64,{}'.format(encoded_image.decode()),
                     alt='customer logo image'),
        ], className='col-6', style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
    ], className='row'),

    # Row 2: Buttons for Animal Types and Radio Buttons
    html.Div([
        html.Div([
            html.Button('All', id='btn-all', n_clicks=0)
            *[html.Button(animal_type, id=f'btn-{animal_type}', n_clicks=0) for animal_type in unq_animal_types] if unq_animal_types else [],
        ], className='col-6'),
        html.Div([
            dcc.RadioItems(
                id='rescue-filter',
                options=[
                    {'label': 'Water Rescue', 'value': 'water'},
                    {'label': 'Mountain and Wilderness Rescue', 'value': 'mount'},
                    {'label': 'Disaster and Individual Tracking', 'value': 'disaster'},
                    {'label': 'Reset', 'value': 'reset'}
                ],
                value='reset',
            ),
        ], className='col-6', id='radio-buttons'),  # Give it an ID for callback
    ], className='row'),

    # Row 3: Data Table and Breed Count
    html.Div([
        dash_table.DataTable(
            id='datatable-id',
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
            ],
            data=data,
            # Set up the features for your interactive data table to make it user-friendly for your client.
            # If you completed the Module Six Assignment, you can copy in the code you created here.
            editable=False,
            sort_action="native",
            sort_mode="multi",
            selected_rows=[0],
            filter_action="native",
            page_action="native",
            page_current=0,
            page_size=10,
        ),
    ], className='row'),

    # Row 4: Graph and Map
    html.Div([
        dcc.Graph(id='bubble-plot', className='col-6'),  # Use dcc.Graph for bubble-plot
        html.Div([
            html.Div(id='graph-id', className='col-12'),  # Update the size to col-12
            html.Div(id='map-id', className='col-12'),  # Update the size to col-12
        ], className='col-6'),
    ], className='row'),

    # Row 5: Breed Count
    html.Div(id='breed-count'),

], style={'display': 'flex', 'flex-direction': 'column'})

# This section demonstrates skills and conceptualization of software design/engineering by setting up a user-friendly interface for data visualization.
# It also includes authentication implementation which further demonstrates these practices.
# It also exhibits good design practices by organizing the layout in a structured and visually appealing manner.

# Authentication callback
@app.callback(
    Output('url', 'pathname'),
    [Input('login-button', 'n-clicks')],
    [State('username', 'value'), State('password', 'value')]
)
def login(n_clicks, username, password):
    if n_clicks is not None and n_clicks > 0 and authenticate(username, password):
        return '/dashboard'
    else:
        return '/'


# Rescue type breeds callback
@app.callback(
    Output('breed-count', 'children'),
    Input('rescue-filter', 'value')
)
def update_breed_count(selected_rescue_type):
    if selected_rescue_type == 'reset':
        return f'Total Breeds: {len(df)}'
    
    # Initialize a count variable
    count = 0
    
    # Iterate through the DataFrame and count breeds based on selected rescue type
    for index, row in df.iterrows():
        breed = row['breed']
        rescue_types = row['rescue_type']
        
        # Check if the selected rescue type matches any of the breed's rescue types
        if selected_rescue_type in rescue_types:
            count += 1
    
    return f'Breeds with {selected_rescue_type} Rescue: {count}'


# Datatable callback
@app.callback(
    [Output('datatable-id', 'data'), Output('datatable-id', 'columns')],
    [Input('btn-all', 'n_clicks')] + [Input(f'btn-{animal_type}', 'n_clicks') for animal_type in (unq_animal_types or [])] + [Input('rescue-filter', 'value')],
    prevent_initial_call=True
)

def update_dashboard(*args):
    # Extract the values from the *args list
    btn_all_clicks, *btn_type_click, rescue_filter = args

    context = dash.callback_context
    button_id = context.triggered[0]['prop_id'].split('.')[0]
    
    # Determine the selected animal type
    if button_id == 'btn-all':
        selected_animal_type = None
    else:
        selected_animal_type = button_id.split('-')[1]

    # Filter the data based on the selected animal type
    if selected_animal_type:
        filtered_data = [record for record in data if record['animal_type'] == selected_animal_type]
    else:
        filtered_data = data

    # Show or hide the rescue filter based on the selected animal type
    rescue_filter_style = {'display': 'block' if selected_animal_type == 'dog' else 'none'}

    # Filter the data based on the selected rescue type
    if rescue_filter != 'reset':
        filtered_data = [record for record in filtered_data if record['rescue_type'] == rescue_filter]

    # Define the columns for the datatable
    columns = [{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]

    return filtered_data, columns

# Bubbleplot callback
@app.callback(
    Output('bubble-plot', 'figure'),
    Output('datatable-id', 'derived_viewport_data'),
    Output('graph-id', "children"),
    Input('rescue-filter', 'value'),
    [Input(f'btn-{animal_type}', 'n_clicks') for animal_type in (unq_animal_types or [])],
    prevent_initial_call=True
)
def update_plot(rescue_filter, *btn_clicks):
    dff = df.copy()

    # Calculate total counts of each rescue type for dogs
    if rescue_filter == 'reset':
        dff_dogs = dff[dff['animal_type'] == 'Dog']
        rescue_counts = dff_dogs['rescue_type'].value_counts()
    else:
        dff_dogs = dff[(dff['animal_type'] == 'Dog') & (dff['rescue_type'] == rescue_filter)]
        rescue_counts = dff_dogs['rescue_type'].value_counts()        

    # Calculate the total count of all rescue dogs
    total_rescue_dogs = len(dff_dogs)

    # Create a size column based on rescue counts for each data point
    dff_dogs['size'] = dff_dogs['rescue_type'].map(rescue_counts)

    # Create the bubble plot
    fig = px.scatter(
        dff_dogs,
        x='age_upon_outcome_in_weeks',
        y='outcome_type',
        size='size',  # Use the 'size' column for sizing
        color='breed',
        hover_name='animal_type'
    )

    return fig, dff_dogs.to_dict('records'), total_rescue_dogs

# Map callback
@app.callback(
    Output('map-id', "children"),
    Input('datatable-id', "derived_viewport_data"),
    Input('datatable-id', 'selected_rows'),
    prevent_initial_call = True
)
def update_map(viewData, selected_rows):
    dff = pd.DataFrame.from_dict(viewData)
    
    if selected_rows is not None and len(selected_rows) > 0:
        selected_row_index = selected_rows[0]

        if selected_row_index >= 0 and selected_row_index < len(dff):
            selected_row = dff.iloc[selected_row_index]

            latitude = selected_row['location_lat']
            longitude = selected_row['location_long']

            return [
                dl.Map(
                    style={'width': '1000px', 'height': '500px'},
                    center=[30.75, -97.48],
                    zoom=10,
                    children=[
                        dl.TileLayer(id="base-layer-id"),
                        dl.Marker(
                            position=(latitude, longitude),
                            children=[
                                dl.Tooltip('Austin Animal Shelter'),  # Replace with relevant tooltip data
                                dl.Popup([
                                    html.H1(selected_row["animal_type"]),
                                    html.P(selected_row["breed"])  # Replace with relevant popup content
                                ])
                            ]
                        )
                    ]
                )
            ]

    # Return an empty list when no row is selected or the selected index is out of bounds
    return []



app.run_server(debug=True)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
