import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
from geojson_rewind import rewind
from utils.utils import create_offcanvas_content


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
geo_json = rewind(geo_json, rfc7946=False)



# ======================================================================================================================
#                                              PROMEDIOS PARA EL CHOROPLETH
# ======================================================================================================================
# Importar archivo df_antioquia_promedios.csv
df_antioquia = pd.read_csv('assets/df_antioquia_promedios.csv', dtype=str)

# ======================================================================================================================
#                                    BASES DE DATOS PARA LINE CHART DE MUNICIPIO
# ======================================================================================================================
df_antioquia_promedios = pd.read_csv('assets/df_antioquia_linechart.csv')
df_colombia = pd.read_csv('assets/df_colombia_linechart.csv')


# ======================================================================================================================
#                                      CHOROPLETH DE ANTIOQUIA v.2 (Objeto gráfico)
# ======================================================================================================================
# Crear el objeto gráfico de mapa
fig = go.Figure()

# Añadir la capa de choropleth
fig.add_trace(
    go.Choropleth(
        geojson=geo_json,
        locations=df_antioquia_promedios['COLE_MCPIO_UBICACION'],
        z=df_antioquia_promedios['PUNT_GLOBAL'][df_antioquia_promedios['AÑO'] == 2022],
        featureidkey="properties.MPIO_CNMBR",
        colorscale="Blues",
        # colorbar=dict(title="AVG_PUNT_GLOBAL"),
        geo="geo",
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
        
        # ---------------------------------------------------------------------------------------------------------------
        #                                                   OFFCANVAS
        # ---------------------------------------------------------------------------------------------------------------
        dbc.Offcanvas(
            id="offcanvas-subregion",
            is_open=False,
            placement='end',
            backdrop=False,
            scrollable=True,
        ),


        # ---------------------------------------------------------------------------------------------------------------
        #                                  IZQ: MAPA COROPLÉTICO DE ANTIOQUIA
        # ---------------------------------------------------------------------------------------------------------------
        dbc.Col([
            dcc.Graph(id="choropleth-ANT", figure=fig,style={'padding-bottom': '15px'}), 
            dcc.Slider(id='year-slider', marks={str(year): str(year) for year in range(2015, 2023)}, value=2022, step=1, persistence=True),
        ], width=5),



        # ---------------------------------------------------------------------------------------------------------------
        #                                  DER: TARJETA CON INFORMACIÓN DEL MUNICIPIO
        # ---------------------------------------------------------------------------------------------------------------
        dbc.Col([
            
            dbc.Card([
                
                # Encabezado de la tarjeta
                dbc.CardHeader([
                    
                    # Logo y dropdown con lista de municipios en la misma línea
                    html.Div([
                        
                        # Logo con id para poder modificarlo con callbacks
                        html.Img(
                            src="./assets/croquis-ANT2.png", 
                            height="40px",
                            id='flag-img',
                            style={
                                "boxShadow": "1px 1px 5px grey",  # Sombras con desplazamiento X, Y y radio
                            }
                        ),
                        
                        # Dropdown con lista de municipios
                        dcc.Dropdown(
                            id='dropdown-municipios',
                            options=[{'label': municipio, 'value': municipio} for municipio in df_antioquia['MPIO_CNMBR']],
                            value='MEDELLÍN',
                            persistence=True,
                            clearable=False,
                            style={'Font-size': '12px', 'width': '320px', 'margin-left': '10px'},
                            className="Dropdown-Title"
                        ),

                    ], style={'display': 'flex', 'align-items': 'center'})
                        
                ]),

                # Cuerpo de la tarjeta
                dbc.CardBody(
                    [
                        # Escribir texto en el mismo renglón que el botón subregion-button
                        html.Div([
                            html.H6([html.I(className="fa fa-location-dot"),'\t Subregión:'], style={'margin-right': '10px'}),  # Añadí un margen derecho
                            dbc.Button(id='subregion-button', color='primary', outline=True, size='sm'),
                        ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '10px'}),

                        html.Hr(),

                        # Crear diagrama de linea con puntajes por año (solo graph con id para modificarlo con callbacks)
                        dbc.Spinner(
                            dcc.Graph(
                                id="line-chart-ANT",
                                config={'displayModeBar': False, 'scrollZoom': False},
                            ),
                            size="lg",  # Ajusta el tamaño del spinner según tus preferencias
                            color="primary",  # Cambia el color del spinner si es necesario
                        ),
                    ]
                ),
                ],
                id='div-1'
            ),
            
        ], width=7),

    ], style={'padding-left': '20px', 'padding-right': '20px', 'padding-top': '10px'}),


])



# ======================================================================================================================
#                                              CALLBACKS DE LA PÁGINA
# ======================================================================================================================

# Actualizar el choropleth cuando se seleccione un municipio
@dash.callback(
    Output('choropleth-ANT', 'figure'),
    [Input('dropdown-municipios', 'value'),
     Input('year-slider', 'value')]
)
def update_choropleth(selected_municipio, selected_year):
    # Crear el objeto gráfico de mapa
    fig = go.Figure()

    # Añadir la capa de choropleth
    fig.add_trace(
        go.Choropleth(
            geojson=geo_json,
        locations=df_antioquia_promedios['COLE_MCPIO_UBICACION'],
        z=df_antioquia_promedios['PUNT_GLOBAL'][df_antioquia_promedios['AÑO'] == selected_year],
        zmin=180,
        zmax=300,
        featureidkey="properties.MPIO_CNMBR",
        colorscale="Blues",
            geo="geo",
            uirevision='static',
            hovertemplate="<br>".join([
                "<b>%{location}</b>",
                "Subregión: %{customdata}",
                "Puntaje global: %{z}",
            ]),
            customdata=df_antioquia['SUBREGION'],
            marker=dict(
                line=dict(
                    color=['orange' if municipio == selected_municipio else '#444' for municipio in df_antioquia['MPIO_CNMBR']],
                    width=[4 if municipio == selected_municipio else 1 for municipio in df_antioquia['MPIO_CNMBR']]
                )
            ),
            name='' # Para que no aparezca el nombre de la serie en la leyenda
        )
    )

    # Actualizar el diseño del gráfico
    fig.update_geos(fitbounds="locations", visible=False, projection_type="mercator")
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=400,  # Ajusta el valor de altura según tus preferencias
    )

    return fig


# ---------------------------------------------------------------------------------------------------------------
#                                  CALLBACKS PARA LA TARJETA CON INFORMACIÓN DEL MUNICIPIO
# ---------------------------------------------------------------------------------------------------------------
@dash.callback(
    [Output('flag-img', 'src'),
    Output('line-chart-ANT', 'figure'),
    Output('subregion-button', 'children')],
    [Input('dropdown-municipios', 'value')]
)
def update_flag_img(selected_municipio):

    # Selecciona la bandera del municipio seleccionado
    bandera = df_antioquia[df_antioquia['MPIO_CNMBR'] == selected_municipio]['BANDERA'].values[0]

    # ------------------- Crear el diagrama de linea con puntajes por año -------------------
    # Voy a tener una variable para seleccionar un municipio.
    municipio = selected_municipio

    # Voy a tener una variable para seleccionar una variable. Ej. Puntaje matemáticas
    variable = 'PUNT_GLOBAL'

    # Crear el objeto gráfico de línea
    fig = go.Figure()

    # Obtener datos del municipio seleccionado
    data_municipio = df_antioquia_promedios[df_antioquia_promedios['COLE_MCPIO_UBICACION'] == municipio]

    # Construir el gráfico de línea con marcadores
    fig.add_scatter(x=data_municipio['AÑO'], y=data_municipio[variable], mode='lines+markers', name=municipio, line=dict(color='blue', width=2), marker=dict(color='blue', size=8, symbol='circle'))

    # Comparar con el promedio de Colombia
    fig.add_scatter(x=df_colombia['AÑO'], y=df_colombia[variable], mode='lines+markers', name='COLOMBIA', line=dict(color='grey', width=2), marker=dict(color='grey', size=8, symbol='square'))

    # Añadir nombres de las series como anotaciones a la izquierda del comienzo de cada línea
    annotations = []

    for i in range(len(fig.data)):
        series_name = fig.data[i].name
        start_value = fig.data[i].y[0]

        # Agregar anotaciones de nombres de series
        annotations.append(
            dict(
                x=data_municipio['AÑO'].min(),
                y=start_value,
                text=series_name,
                showarrow=False,
                xanchor='right',
                font=dict(family='Arial', size=12, color=fig.data[i].line.color),
                xshift=-10
            )
        )

        # Agregar anotaciones de puntajes directamente
        for j, y_value in enumerate(fig.data[i].y):
            annotations.append(
                dict(
                    x=fig.data[i].x[j],
                    y=y_value + 3,
                    text=f'{y_value:.0f}',
                    showarrow=False,
                    arrowhead=0,
                    ax=0,
                    ay=-60,
                    font=dict(family='Arial', size=10, color='black')
                )
            )

    # Agregar anotaciones de fuente
    annotations.extend([
        dict(
            xref='paper', yref='paper', x=0.5, y=-0.27,
            xanchor='center', yanchor='top',
            text='Fuente: ICFES (2023). DataIcfes. Saber 11. <a href="https://www.icfes.gov.co/web/guest/data-icfes" target="_blank">[Enlace]</a>',
            font=dict(family='Arial', size=12, color='rgb(150,150,150)'),
            showarrow=False
        )
    ])

    # Configurar diseño y diseño de anotaciones
    fig.update_layout(
        # title='Promedio de ' + variable + ' en ' + municipio,
        xaxis_title='Año',
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(204, 204, 204)',
            linewidth=2,
            ticks='outside',
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            showticklabels=False,
        ),
        autosize=True,
        plot_bgcolor='white',
        showlegend=False,
        annotations=annotations  # Añadir las anotaciones al diseño
    )
    fig.update_layout(hovermode="x unified",
                      margin=dict(t=10, l=30, r=30),
                      height=300,)
    
    # Selecciona la subregión del municipio seleccionado
    subregion = df_antioquia[df_antioquia['MPIO_CNMBR'] == selected_municipio]['SUBREGION'].values[0]

    return bandera, fig, subregion


# ---------------------------------------------------------------------------------------------------------------
#                                 CALLBACKS PARA EL OFFCANVAS
# ---------------------------------------------------------------------------------------------------------------
# Cambiar el estado del offcanvas cuando se hace clic en el botón
@dash.callback(
    Output("offcanvas-subregion", "is_open"),
    [Input("subregion-button", "n_clicks")],
    [State("offcanvas-subregion", "is_open")]
)
def toggle_offcanvas(n_clicks, is_open):
    return not is_open if n_clicks else is_open

# Actualizar el contenido del offcanvas cuando se selecciona un municipio
@dash.callback(
    Output("offcanvas-subregion", "children"),
    [Input("dropdown-municipios", "value")]
)
def update_offcanvas(selected_municipio):

    # Selecciona la subregión del municipio seleccionado
    subregion = df_antioquia[df_antioquia['MPIO_CNMBR'] == selected_municipio]['SUBREGION'].values[0]

    return create_offcanvas_content(subregion)




        