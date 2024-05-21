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
|  ###  Start -- 05/2024 - TH                                                                               |
|  [Converted jupyter notebook file into a Python application file to more easily integrate as web          |
|  application instead of hosting locally.]                                                                 |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start -- 05/2024 - TH                                                                               |
|  [Updated language to call the new animal_shelter.py import, versus previous module.py.]                  |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start -- 05/2024 - TH                                                                               |
|  [Corrected filters and continuously debugging to determine what is causing them to not function          |
|  properly if they function at all.]                                                                       |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start --05/2024 - TH                                                                                |
|  [Added enhancements as planned, but still running into buggy application issues.]                        |
|  ### - End                                                                                                |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|  ###  Start --05/2024 - TH                                                                                |
|  [Made final enhancements, debugged, tested and is now ready for MVP deployment.                          |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|                                            Notes:                                                         |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|   05/17/2024                                                                                              |
|   Notes for next assignments and TODOS: Figure out why the code is not launching the web application.     |
|   Current Issues: The code is not launching the web application at all. Either it returns                 |
|   Not found, or it returns a 504 error page. Cannot continue to test until I can get it to deploy.        |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|   05/18/2024                                                                                              |
|   Update: After several alterations, and updating the final call to the app.run_server method,            |
|   the application is now launching.                                                                       |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|   05/18/2024                                                                                              |
|   Notes for next assignments and TODOS: Debugging and testing the application                             |
|   Current Issues: Filters are not functioning properly. The data is not being filtered as expected.       |
|   When clicking on any filter, or using the text filter, the data is not changed, or sorted.              |
|   It also does not populate the graph with the correct data.                                              |
|   Continue altering the code and testing to find the issue and continue adding enhancements.              |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
|   05/19/2024                                                                                              |
|   Notes on final adjustments to get to MVP.                                                               |
|   The map functionality was never helpful, so I removed it altogether, as it only ever showed the         |
|   location of the animal shelter, not the lat and long in the data table. I also removed the              |
|   rescue filter and rescue type, as it was not very UI friendly, nor was it visually appealing.           |
|   Instead of the bubble chart populating with a count of dog rescue types, it now populates with          |
|   animal_type, and is grouped based on type and outcome type for the animal. This is more intuitive       |
|   and uses the data in a more insightful manner. This is my final adjustment to the code, and now plan    |
|   to deploy to my created live server.                                                                    |
|*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*|
'''

from dash import Dash, html, dcc, dash_table  # Importing necessary Dash components
import dash  # Importing Dash
from dash.dependencies import Input, Output  # Importing Dash callback functions
import plotly.express as px  # Importing Plotly Express for data visualization
import pandas as pd  # Importing Pandas for data manipulation
from animal_shelter import AnimalShelter  # Importing AnimalShelter class for data access
import base64  # Importing base64 for image encoding

# Setup Dash
app = Dash(__name__)  # Creating a Dash application instance

# Data Manipulation / Model
db_path = 'animals.db'  # Path to the database file
shelter = AnimalShelter(db_path)  # Creating an instance of AnimalShelter to interact with the database
data = shelter.read()  # Reading data from the database
df = pd.DataFrame(data)  # Creating a Pandas DataFrame from the retrieved data

# Get each animal type in the collection (distinct, no duplicates)
unq_animal_types = df['animal_type'].unique()  # Extracting unique animal types from the DataFrame
data = df.to_dict('records')  # Converting DataFrame to a list of dictionaries for Dash data components

# Add in Grazioso Salvare’s logo
image_filename = 'Grazioso_Salvare_Logo.png'  # Path to the logo image file
encoded_image = base64.b64encode(open(image_filename, 'rb').read())  # Encoding the image to base64

# Defining the layout of the Dash application
app.layout = html.Div([
    html.Center(html.B(html.H1('Capstone Project Dashboard'))),  # Header
    html.Center(html.B(html.H1("Tammy Hartline's Grazioso Salvare DashBoard Final Project"))),  # Subheader
    html.Hr(),  # Horizontal line

    # Row 1: Header and Photo
    html.Div([
        html.Div(id='header', className='col-6', style={'text-align': 'center'}),
        html.Div([
            html.Img(id='customer-logo', src='data:image/png;base64,{}'.format(encoded_image.decode()),
                     alt='customer logo image'),
        ], className='col-6', style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}),
    ], className='row'),

    # Row 2: Buttons for Animal Types
    html.Div([
        html.Div([
            html.Button('All', id='btn-all', n_clicks=0),
            *[html.Button(animal_type, id=f'btn-{animal_type}', n_clicks=0) for animal_type in unq_animal_types]
            # Creating buttons for each unique animal type
        ], className='col-6'),
    ], className='row'),

    # Row 3: Data Table
    html.Div([
        dash_table.DataTable(
            id='datatable-id',
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
            ],  # Defining columns for the data table
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

    # Row 4: Graph
    html.Div([
        dcc.Graph(id='bubble-plot', className='col-6'),
    ], className='row'),
])

# This section demonstrates skills and conceptualization of software design/engineering by setting up a user-friendly interface for data visualization.
# It also exhibits good design practices by organizing the layout in a structured and visually appealing manner.

@app.callback(
    [Output('bubble-plot', 'figure'), Output('datatable-id', 'data'), Output('datatable-id', 'columns')],
    [Input('btn-all', 'n_clicks')] + [Input(f'btn-{animal_type}', 'n_clicks') for animal_type in unq_animal_types],
    prevent_initial_call=True
)
@app.callback(
    [Output('bubble-plot', 'figure'), Output('datatable-id', 'data'), Output('datatable-id', 'columns')],
    [Input('btn-all', 'n_clicks')] + [Input(f'btn-{animal_type}', 'n_clicks') for animal_type in unq_animal_types],
    prevent_initial_call=True
)
def update_dashboard(*args):
    btn_all_clicks, *btn_type_click = args

    # Determine which button was clicked
    ctx = dash.callback_context
    clicked_button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if clicked_button_id == 'btn-all':
        filtered_df = df.copy()  # No filter, so use the entire DataFrame
    else:
        selected_animal_type = clicked_button_id.split('-')[1]
        filtered_df = df[df['animal_type'] == selected_animal_type]  # Filter by selected animal type

    # Create age bins
    age_bins = [0, 8, 16, 52, 156, float('inf')]
    age_labels = ['0-2 months', '2-4 months', '4-12 months', '1-3 years', '3+ years']
    filtered_df['age_bin'] = pd.cut(filtered_df['age_upon_outcome_in_weeks'], bins=age_bins, labels=age_labels, right=False)

    # Group by animal_type, age_bin, and outcome_type and calculate the count
    grouped_df = filtered_df.groupby(['animal_type', 'age_bin', 'outcome_type']).size().reset_index(name='count')

    # Create a stacked bar chart
    fig = px.bar(
        grouped_df,
        x='age_bin',
        y='count',
        color='outcome_type',
        barmode='stack',
        facet_col='animal_type',
        labels={'age_bin': 'Age Bin', 'count': 'Count', 'outcome_type': 'Outcome Type', 'animal_type': 'Animal Type'},
        title='Outcome Type Count by Age Bin and Animal Type'
    )

    # Convert DataFrame to dict for dash_table
    filtered_data = filtered_df.to_dict('records')

    # Generate columns for dash_table
    columns = [{"name": i, "id": i, "deletable": False, "selectable": True} for i in filtered_df.columns]

    return fig, filtered_data, columns

# This callback function demonstrates skills and conceptualization of algorithms by dynamically updating the data visualization based on user interactions.
# It efficiently filters and processes data to generate relevant charts and tables.

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)
