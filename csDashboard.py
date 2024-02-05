# Tammy Hartline
# CS-499 - Previous Version CS-340
# Capstone
# Interactive Dashboard coded with Jupyter notebook and dash using MongoDB in CS-340
# October 2023
# Updated Version - 02/2024 Interactive Dashboard coded with python and using SQLite for CS-499 

# Setup Dash
from dash import Dash

# Configure the necessary Python module imports for dashboard components
import dash
import dash_leaflet as dl
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash import dash_table
import base64
from module import AnimalShelter

# Configure OS routines
import os

# Configure the plotting routines
import pandas as pd

# Import CRUD file
from module import AnimalShelter

# Data Manipulation / Model
# Update with your username and password and CRUD Python module name
db_path = 'animals.db'
shelter = AnimalShelter(db_path)

# Class read method must support return of a list object and accept projection JSON input.
# Sending the read method an empty document requests all documents be returned.
data = shelter.read()

# Assuming the first row contains column names, set them explicitly
df = pd.DataFrame(data[1:], columns=data[0])


# Dashboard Layout / View
app = Dash(__name__)

# Add in Grazioso Salvare’s logo
image_filename = 'Grazioso_Salvare_Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Place the HTML image tag in the line below into the app.layout code according to your design.
# Also, remember to include a unique identifier such as your name or date.
html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

# Create global variables to populate filtered data

# Get each animal type in the collection (distinct, no duplicates)
unq_animal_types = df['breed'].unique()
data = df.to_dict('records')
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
            html.Button('All', id='btn-all', n_clicks=0),
            *[html.Button(breed, id=f'btn-{breed}', n_clicks=0) for breed in unq_animal_types]
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
        dcc.Graph(id='bubble-plot', className='col-6'),
        html.Div([
            html.Div(id='graph-id', className='col-12'),
            html.Div(id='map-id', className='col-12'),
        ], className='col-6'),
    ], className='row'),

    # Row 5: Breed Count
    html.Div(id='breed-count'),

    # Row 6: Log
    html.Div([
        dcc.Markdown(id='log-output', style={'whiteSpace': 'pre-line'})
    ], className='row'),

], style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(
    Output('breed-count', 'children'),
    Input('rescue-filter', 'value')
)
def update_breed_count(selected_rescue_type):
    if selected_rescue_type == 'reset':
        return f'Total Breeds: {len(df)}'
    
    count = 0
    
    for index, row in df.iterrows():
        breed = row['breed']
        rescue_types = row['rescue_type']
        
        if selected_rescue_type in rescue_types:
            count += 1
    
    return f'Breeds with {selected_rescue_type} Rescue: {count}'


@app.callback(
    [Output('datatable-id', 'data'), Output('datatable-id', 'columns')],
    [Input('btn-all', 'n_clicks')] + [Input(f'btn-{breed}', 'n_clicks') for breed in unq_animal_types] + [Input('rescue-filter', 'value')],
    prevent_initial_call=True
)
def update_dashboard(*args):
    btn_all_clicks, *btn_type_click, rescue_filter = args

    context = dash.callback_context
    button_id = context.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'btn-all':
        selected_breed = None
    else:
        selected_breed = button_id.split('-')[1]

    if selected_breed:
        filtered_data = [record for record in data if record['breed'] == selected_breed]
    else:
        filtered_data = data

    rescue_filter_style = {'display': 'block' if selected_breed == 'Dog' else 'none'}

    if rescue_filter != 'reset':
        filtered_data = [record for record in filtered_data if record['rescue_type'] == rescue_filter]

    columns = [{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns]

    return filtered_data, columns


@app.callback(
    Output('bubble-plot', 'figure'),
    Output('datatable-id', 'derived_viewport_data'),
    Output('graph-id', "children"),
    Input('rescue-filter', 'value'),
    [Input(f'btn-{breed}', 'n_clicks') for breed in unq_animal_types],
    prevent_initial_call=True
)
def update_plot(rescue_filter, *btn_clicks):
    dff = df.copy()

    if rescue_filter == 'reset':
        dff_breeds = dff[dff['breed'] == 'Dog']
        rescue_counts = dff_breeds['rescue_type'].value_counts()
    else:
        dff_breeds = dff[(dff['breed'] == 'Dog') & (dff['rescue_type'] == rescue_filter)]
        rescue_counts = dff_breeds['rescue_type'].value_counts()        

    total_rescue_breeds = len(dff_breeds)

    dff_breeds['size'] = dff_breeds['rescue_type'].map(rescue_counts)

    fig = px.scatter(
        dff_breeds,
        x='age',
        y='outcome_type',
        size='size',
        color='breed',
        hover_name='breed'
    )

    return fig, dff_breeds.to_dict('records'), total_rescue_breeds


# Map
@app.callback(
    Output('map-id', "children"),
    Input('datatable-id', "derived_viewport_data"),
    Input('datatable-id', 'selected_rows'),
    prevent_initial_call=True
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
                                dl.Tooltip('Animal Shelter'),
                                dl.Popup([
                                    html.H1(selected_row["breed"]),
                                    html.P(selected_row["name"])
                                ])
                            ]
                        )
                    ]
                )
            ]

    return []


if __name__ == '__main__':
    serve(app.server, host='0.0.0.0', port=8050)
