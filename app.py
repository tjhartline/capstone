'''

Tammy Hartline
Feb 2024
Capstone Course Week 4
#app.py - Main application file
Description: This file is meant to initialize the database functionality for the web application.
To execute, open terminal and type: python app.py once in the directory where the file is located.


--------------------------------------------------------------------------------------------
02/05/2024
Notes for next assignments and TODOS: Figure out why the code is not launching the web application.
Current Issues: The code is not launching the web application at all. Either it returns
Not found, or it returns a 504 error page. Cannot continue to test until I can get it to deploy.

02/07/2024
Update: After several alterations, and updating the final call to the app.run_server method, the application is now launching.
---------------------------------------------------------------------------------------------
02/11/2024
Notes for next assignments and TODOS: Debugging and testing the application
Current Issues: Filters are not functioning properly. The data is not being filtered as expected.
When clicking on any filter, or using the text filter, the data is not changed, or sorted.
It also does not populate the graph with the correct data.
Continue altering the code and testing to find the issue and continue adding enhancements.
----------------------------------------------------------------------------------------------
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

    # Create a bubble chart
    fig = px.scatter(filtered_df, x="animal_type", y="outcome_type", size=filtered_df.groupby('animal_type').size(), color="animal_type")

    # Convert DataFrame to dict for dash_table
    filtered_data = filtered_df.to_dict('records')

    # Generate columns for dash_table
    columns = [{"name": i, "id": i, "deletable": False, "selectable": True} for i in filtered_df.columns]

    return fig, filtered_data, columns

# This callback function demonstrates skills and conceptualization of algorithms by dynamically updating the data visualization based on user interactions.
# It efficiently filters and processes data to generate relevant charts and tables.

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)
