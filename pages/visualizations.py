import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

templates = ["cerulean"]
load_figure_template(templates)

# Registrar la página
dash.register_page(__name__, path='/visualizations')


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

# Exportar df_antioquia a CSV con codificación UTF-8
# df_antioquia.to_csv('assets/df_antioquia_2.csv', index=False, encoding='utf-8')



# ======================================================================================================================
#                                      CHOROPLETH DE ANTIOQUIA v.2 (Objeto gráfico)
# ======================================================================================================================

# Crear el objeto gráfico de mapa
fig = go.Figure()

# Añadir la capa de choropleth
fig.add_trace(
    go.Choropleth(
        geojson=geo_json,
        locations=df_antioquia['DPTOMPIO'],
        z=df_antioquia['NEW'],
        featureidkey="properties.DPTOMPIO",
        colorscale="Blues",
        colorbar=dict(title="NEW"),
        geo="geo",  # Cambia esta línea
        uirevision='static',
    )
)

# Actualizar el diseño del gráfico
fig.update_geos(fitbounds="locations", visible=False, projection_type="mercator")
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
            
            # Dropdown con lista de municipios
            dcc.Dropdown(
                id='dropdown-municipios',
                options=[{'label': i, 'value': i} for i in df_antioquia['MPIO_CNMBR'].unique()],
            ),

            # Separador
            html.Hr(),

            # Texto con el municipio seleccionado
            html.Div(id='municipio-seleccionado'),
    
        ], width=7),

    ], style={'padding-left': '20px', 'padding-right': '20px', 'padding-top': '10px'}),


])



# ======================================================================================================================
#                                              CALLBACKS DE LA PÁGINA
# ======================================================================================================================

# Actualizar el choropleth cuando se seleccione un municipio
@dash.callback(
    Output('choropleth-ANT', 'figure'),
    [Input('dropdown-municipios', 'value')]
)
def update_choropleth(selected_municipio):
    # Crear el objeto gráfico de mapa
    fig = go.Figure()

    # Añadir la capa de choropleth
    fig.add_trace(
        go.Choropleth(
            geojson=geo_json,
            locations=df_antioquia['DPTOMPIO'],
            z=df_antioquia['NEW'],
            featureidkey="properties.DPTOMPIO",
            colorscale="blues",
            colorbar=dict(title="NEW"),
            geo="geo",  # Cambia esta línea
            uirevision='static',
            marker=dict(
                line=dict(
                    color=['orange' if municipio == selected_municipio else '#444' for municipio in df_antioquia['MPIO_CNMBR']],
                    width=[4 if municipio == selected_municipio else 1 for municipio in df_antioquia['MPIO_CNMBR']]
                )
            )
        )
    )

    # Actualizar el diseño del gráfico
    fig.update_geos(fitbounds="locations", visible=False, projection_type="mercator")
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=400,  # Ajusta el valor de altura según tus preferencias
    )

    return fig

# Actualizar el texto con el municipio seleccionado
@dash.callback(
    Output('municipio-seleccionado', 'children'),
    [Input('dropdown-municipios', 'value')]
)
def update_text(selected_municipio):
    # Retorna html.H3 con el nombre del municipio seleccionado
    bandera_municipio = "https://upload.wikimedia.org/wikipedia/commons/1/13/Flag_of_Zaragoza_%28Antioquia%29.svg" #TODO: Conectar con la base de datos

    # Retorna html.H4 con el nombre del municipio seleccionado y su bandera
    return html.H4([html.Img(src=bandera_municipio, style={'height': '25px', 'width': 'auto'}), '\t Tres tristes tigres de ', selected_municipio])