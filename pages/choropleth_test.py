import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd
import json

templates = ["cerulean"]
load_figure_template(templates)

# Registrar la página
dash.register_page(__name__, path='/choropleth_test')


# ======================================================================================================================
#                                               CHOROPLETH DE ANTIOQUIA
# ======================================================================================================================

# Cargar GeoJSON
with open('assets/MunicipiosVeredas19MB.json', encoding='utf-8') as geojson:
    geo_json = json.load(geojson)

# Usamos geojson_rewind para corregir la orientación de los polígonos del GeoJSON. Esto es necesario para que el choropleth funcione correctamente
from geojson_rewind import rewind
geo_json = rewind(geo_json, rfc7946=False)

# Cargar df del GeoJSON
df_map = pd.read_csv('assets/MunicipiosVeredas.csv', dtype=str)

# Filtrar los municipios de Antioquia
df_antioquia = df_map[df_map['DPTO_CCDGO'] == '05']

# Variable dummy para el choropleth
# TODO: Cambiar por puntajes promedio por prueba por municipio
df_antioquia = df_antioquia.copy()
df_antioquia['NEW'] = df_antioquia['MPIO_CCDGO'].astype(int)


# Crear el choropleth. Posibles paletas de colores: (Sunset*, Purples*, Blues, Greens, Oranges, Reds, YlOrRd, YlOrBr, Geyser, Earth, Electric, Bluered, RdBu, Picnic, Rainbow, Portland, Jet, Hot, Blackbody, Earth, Electric, Viridis, Cividis)
fig = px.choropleth(df_antioquia, geojson=geo_json, color="NEW",
                    locations="DPTOMPIO", featureidkey="properties.DPTOMPIO",
                    color_continuous_scale="Blues",
                    projection="mercator"
                    )
# fig.update_geos(fitbounds="locations", visible=False)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=400,  # Ajusta el valor de altura según tus preferencias
)



# ======================================================================================================================
#                                               CONTENIDO DE LA PÁGINA
# ======================================================================================================================
layout = html.Div([

    dbc.Row([
        html.H4([html.I(className="fa fa-location-dot"),'\t Promedio de puntaje global por municipio']),
    ], style={'padding-left': '20px', 'padding-right': '20px', 'padding-top': '10px'}),

    dbc.Row([
        
        # Columna izquierda: Choropleth
        dbc.Col([
            
            dcc.Graph(id="choropleth-ANT", figure=fig),
    
        ], width=5),

        # Columna derecha: Dropdown con lista de municipios
        dbc.Col([
            
            dcc.Dropdown(
                id='dropdown-municipios',
                options=[{'label': i, 'value': i} for i in df_antioquia['MPIO_CNMBR'].unique()],
                value='Medellín'
            ),
    
        ], width=7),

    ], style={'padding-left': '20px', 'padding-right': '20px', 'padding-top': '10px'}),

])