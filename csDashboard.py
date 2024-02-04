#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Tammy Hartline
# CS-340
# Final Project
# Interactive Dashboard coded with Python/Uses MongoDB integration
# October 2023

# Setup the Jupyter version of Dash
from jupyter_dash import JupyterDash

# Configure the necessary Python module imports for dashboard components
import dash
import dash_leaflet as dl
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px  # For heatmap
from dash import dash_table
import base64
import pymongo
# Configure OS routines
import os

# Configure the plotting routines
import pandas as pd

# Change 'animal_shelter' and 'AnimalShelter' to match your CRUD Python module file name and class name
from module import AnimalShelter

# Data Manipulation / Model
# Update with your username and password and CRUD Python module name
username = "aacuser"
pwd = "myPassword"

# Set the default host to '127.0.0.1:27017'
default_host = 'mongodb://aacuser:myPassword@127.0.0.1:27017/aac'
host = os.getenv('MONGO_HOST', default_host)

# Create a MongoClient using the determined host
client = pymongo.MongoClient(host)
port = int(os.getenv('MONGO_PORT', 27017))  # Default to set port

db = 'AAC'
col = 'animals'
shelter = AnimalShelter(username, pwd, host, port, db, col)

# Class read method must support return of a list object and accept projection JSON input.
# Sending the read method an empty document requests all documents be returned.
df = pd.DataFrame.from_records(shelter.read({}))

# MongoDB v5+ is going to return the '_id' column, which will cause the data_table to crash. So, we remove it here.
# The df.drop command allows us to drop the column. If we do not set inplace=True, it will return a new dataframe
# that does not contain the dropped column(s).
df.drop(columns=['_id'], inplace=True)

# Dashboard Layout / View
app = JupyterDash(__name__)

# Add in Grazioso Salvare’s logo
image_filename = 'Grazioso_Salvare_Logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# Place the HTML image tag in the line below into the app.layout code according to your design.
# Also, remember to include a unique identifier such as your name or date.
# html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))

# Create global variables to populate filtered data

# Get each animal type in the collection (distinct, no duplicates)
unq_animal_types = df['animal_type'].unique()
data = df.to_dict('records')
app.layout = html.Div([
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
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
            *[html.Button(animal_type, id=f'btn-{animal_type}', n_clicks=0) for animal_type in unq_animal_types]
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


# In[ ]:


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


# In[ ]:


@app.callback(
    [Output('datatable-id', 'data'), Output('datatable-id', 'columns')],
    [Input('btn-all', 'n_clicks')] + [Input(f'btn-{animal_type}', 'n_clicks') for animal_type in unq_animal_types] + [Input('rescue-filter', 'value')],
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


# In[ ]:


@app.callback(
    Output('bubble-plot', 'figure'),
    Output('datatable-id', 'derived_viewport_data'),
    Output('graph-id', "children"),
    Input('rescue-filter', 'value'),
    [Input(f'btn-{animal_type}', 'n_clicks') for animal_type in unq_animal_types],
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


# In[ ]:


# Map
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


# In[ ]:


#display all column names of DataFrame
print(dff.columns.tolist())
df.dtypes
print(df.head())


# In[ ]:




