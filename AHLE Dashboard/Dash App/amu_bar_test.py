from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import os

CWD = os.getcwd()
DASH_DATA_FOLDER = os.path.join(CWD ,'data')
amu2018_combined_tall = pd.read_csv(os.path.join(DASH_DATA_FOLDER, 'amu2018_combined_tall.csv'))

#input_df = pd.read_csv('amu2018_combined_tall.csv')

app = Dash(__name__)


#Header and Html formatting for AMU Regional Stacked Bar
app.layout = html.Div([
   html.H4('2018 Antimicrobial Usage by Region'),
    dcc.Dropdown(
        id="dropdown",
        options=["Africa", "Americas", "Asia", "Far East and Oceania", "Middle East"],
        value="Americas",
        clearable=False,
        ),
    html.Div(children=[
        dcc.Graph(id="update_stacked_bar_amu", style={'display': 'inline-block'}),
        dcc.Graph(id="update_stacked_bar_amu2", style={'display': 'inline-block'})
    ])
])

#Update Stacked Bar Chart
@app.callback(
    Output('update_stacked_bar_amu', 'figure'),
    Input('dropdown', 'value'))
    #Input('antimicrobial_class', 'value'),
    #Input('amu_tonnes', 'value'))
    #Input('scope', 'value'),
    #Input('number_of_countries', 'value'),
    #Input('importance_ctg', 'value'))

def update_stacked_bar_amu(region):
    input_df = pd.read_csv(os.path.join(DASH_DATA_FOLDER,'amu2018_combined_tall.csv'))
    
    stackedbar_df = input_df.query("scope == 'All'").query("antimicrobial_class != 'total_antimicrobials'")#.query(f"region == '{region}'")
    

    #x = stackedbar_df['region']
    #y = stackedbar_df['antimicrobial_class']
    #color = stackedbar_df['amu_tonnes']
    #amu_bar_fig = update_stacked_bar_amu(stackedbar_df, x, y, color)
    amu_bar_fig = px.bar(stackedbar_df, x='region', y='amu_tonnes',
                         color='antimicrobial_class', barmode='stack',
                         labels={
                             "region": "Region",
                             "amu_tonnes": "AMU Tonnes",
                             "antimicrobial_class": "Antimicrobial Class"})
              
    return amu_bar_fig
        
@app.callback(
    Output('update_stacked_bar_amu2', 'figure'),
   Input('dropdown','value'))

def update_stacked_bar_amu2 (region):
    input_df = pd.read_csv(os.path.join(DASH_DATA_FOLDER,'amu2018_combined_tall.csv'))
    stackedbar_df = amu2018_combined_tall.copy()
    stackedbar_df = input_df.query("scope == 'All'").query("antimicrobial_class != 'total_antimicrobials'")
    amu_bar_fig2 = px.bar(stackedbar_df, x="region", y="amu_mg_perkgbiomass",
                         color='antimicrobial_class',
                         labels={
                             "region": "Region",
                             "amu_mg_perkgbiomass": "AMU Mg Per Kg Biomass",
                             "antimicrobial_class": "Antimicrobial Class"})

    return amu_bar_fig2

if __name__ == '__main__':
    app.run_server(debug=True)