import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.graph_objects as go
import json
import pickle
from pgmpy.inference import VariableElimination
from dash.exceptions import PreventUpdate
from utils.utils import create_dd, create_predicted_performance_chart, interpretar_desempenho

templates = ["cerulean"]
load_figure_template(templates)

# Registrar la página
dash.register_page(__name__, path='/')


# ======================================================================================================================
#                                   CARGA DE DATOS, MODELOS Y DESCARGO DE RESPONSABILIDAD             
# ======================================================================================================================

# Cargar el archivo JSON
try:
    with open('assets/parameter_options.JSON', 'r', encoding='utf-8') as json_file:
        all_params = json.load(json_file)
except FileNotFoundError:
    print("El archivo JSON no se encontró.")
except json.JSONDecodeError:
    print("Error al decodificar el archivo JSON.")
    all_params = {}

# Extraer solo los parámetros de los dropdowns
dd_params = all_params.get('dropdown_params', {})

# Obtener el diccionario de correspondencias
param_name_mapping = all_params.get('param_name_mapping', {})

# TODO: Habilitar la carga del modelo cuando esté listo
# Cargar modelo entrenado desde el archivo
# try:
#     with open('assets/modelo_entrenado.pkl', 'rb') as f:
#         loaded_model = pickle.load(f)
# except FileNotFoundError:
#     print("El archivo del modelo no se encontró.")
# except pickle.UnpicklingError:
#     print("Error al cargar el modelo.")
#     loaded_model = None

# # Crea un objeto de inferencia
# infer = VariableElimination(loaded_model)



# ======================================================================================================================
#                                               CONTENIDO DE LA PÁGINA
# ======================================================================================================================

layout = html.Div([

    # ------------------------------------------------------------------------------------------------------------------
    #                                           PANEL DE LA IZQUIERDA: FORMULARIO
    # ------------------------------------------------------------------------------------------------------------------
    html.Div([

        # Título del formulario
        html.H4([
            # html.I(className="fa fa-square-check"),
            "Parámetros del modelo",
            dbc.Badge("ℹ️", id="info-badge", color="primary", className="ml-2", style={'margin-left': '10px'}),
            dbc.Popover(
                [
                    dbc.PopoverHeader("Cómo usar el formulario"),
                    dbc.PopoverBody(
                        "Escoja los parámetros que desea utilizar para la predicción. "
                        "¡Proporcionar más información seleccionando parámetros adicionales "
                        "mejorará la precisión de la predicción!"
                    ),
                ],
                id="info-popover",
                target="info-badge",
                trigger="hover",
            ),
        ]),

        # Fila 1: Botón para limpiar el formulario y barra de progreso
        dbc.Row([

            # Botón para limpiar el formulario
            dbc.Col([
                dbc.Button("🧹Limpiar", id="clear-button", color="secondary", className="mr-1"),
            ], width=4, style={'margin-bottom': '10px', 'margin-top': '12px'}),

            # Barra de progreso
            dbc.Col([
                dbc.Label("Barra de progreso", html_for="progress-bar", size="sm"),
                dbc.Progress(id="progress-bar", value=0, striped=True, animated=False, style={'height': '25px'}),
            ], width=8, style={'margin-bottom': '10px'}),
            
        ], justify="center", style={'margin-bottom': '10px'}),
        html.Div(style={'margin-bottom': '10px'}),
        
        # ACORDEÓN DE MENÚS DESPLEGABLES
        dbc.Accordion([
            
            # Menú desplegable 1: Información del colegio
            dbc.AccordionItem(
                [
                    # Fila 0
                    dbc.Row([

                        # COLE_NATURALEZA: Naturaleza del Establecimiento
                        create_dd('dd_cole_naturaleza', 'Naturaleza', dd_params['cole_naturaleza'], 'Naturaleza', 6),

                        # COLE_CARACTER: Carácter del Establecimiento
                        create_dd('dd_cole_caracter', 'Carácter', dd_params['cole_caracter'], 'Carácter', 6),

                    ],style={'margin-bottom': '5px'}),

                    # Fila 1
                    dbc.Row([

                        # COLE_AREA_UBICACION: Área de ubicación de la Sede
                        create_dd('dd_cole_area_ubicacion', 'Área de ubicación de la Sede', dd_params['cole_area_ubicacion'], 'Área de ubic. de la Sede', 12),

                    ],style={'margin-bottom': '5px'}),

                    # Fila 2
                    dbc.Row([

                        # COLE_GENERO: Género del Establecimiento
                        create_dd('dd_cole_genero', 'Género', dd_params['cole_genero'], 'Género', 6),


                        # COLE_CALENDARIO: Calendario del Establecimiento
                        create_dd('dd_cole_calendario', 'Calendario', dd_params['cole_calendario'], 'Calendario', 6),

                    ],style={'margin-bottom': '5px'}),

                    # Fila 3
                    dbc.Row([

                        # COLE_JORNADA: Jornada del Establecimiento
                        create_dd('dd_cole_jornada', 'Jornada', dd_params['cole_jornada'], 'Jornada', 6),

                        # COLE_BILINGUE: Indica si el Establecimiento es bilingue o no
                        create_dd('dd_cole_bilingue', 'Bilingüe', dd_params['cole_bilingue'], 'Bilingüe', 6),

                    ],style={'margin-bottom': '5px'}),
                       
                ],
                title='Información del colegio'
            ),


            # Menú desplegable 2: Información personal y socioeconómica
            dbc.AccordionItem([

                    # Fila 1
                    dbc.Row([

                        # ESTU_GENERO: Género del estudiante
                        create_dd('dd_estu_genero', 'Género del estudiante', dd_params['estu_genero'], 'Género', 12),

                    ],style={'margin-bottom': '5px'}),

                    html.Hr(),

                    # Fila 2
                    dbc.Row([

                        # FAMI_EDUCACIONMADRE: Nivel educativo de la madre
                        create_dd('dd_fami_educacionmadre', 'Nivel educativo de la madre', dd_params['fami_educacionmadre'], 'Nivel educativo de la madre', 12),
                        
                    ],style={'margin-bottom': '5px'}),

                    # Fila 3
                    dbc.Row([

                        # FAMI_EDUCACIONPADRE: Nivel educativo del padre
                        create_dd('dd_fami_educacionpadre', 'Nivel educativo del padre', dd_params['fami_educacionpadre'], 'Nivel educativo del padre', 12),

                    ],style={'margin-bottom': '5px'}),


                    # Fila 4
                    dbc.Row([

                        # FAMI_ESTRATOVIVIENDA: Estrato de la vivienda
                        create_dd('dd_fami_estratovivienda', 'Estrato de vivienda', dd_params['fami_estratovivienda'], 'Estrato', 4),

                        # FAMI_PERSONASHOGAR: Número de personas en el hogar
                        create_dd('dd_fami_personashogar', 'Personas en hogar', dd_params['fami_personashogar'], 'N° personas', 4),

                        # FAMI_CUARTOSHOGAR: Número de cuartos en el hogar
                        create_dd('dd_fami_cuartoshogar', 'Cuartos en hogar', dd_params['fami_cuartoshogar'], 'N° cuartos', 4),

                    ],style={'margin-bottom': '5px'}),


                    # Filas 5
                    dbc.Row([

                        # FAMI_TIENECOMPUTADOR: Indica si el hogar tiene computador
                        create_dd('dd_fami_tienecomputador', '¿Tiene computador?', dd_params['fami_tienecomputador'], 'Tiene computador', 6),

                        # FAMI_TIENEINTERNET: Indica si el hogar tiene internet
                        create_dd('dd_fami_tieneinternet', '¿Tiene internet?', dd_params['fami_tieneinternet'], 'Tiene internet', 6),

                    ],style={'margin-bottom': '5px'}),

                    # Filas 6
                    dbc.Row([

                        # FAMI_TIENEAUTOMOVIL: Indica si el hogar tiene automóvil
                        create_dd('dd_fami_tieneautomovil', '¿Tiene automóvil?', dd_params['fami_tieneautomovil'], 'Tiene automóvil', 6),

                        # FAMI_TIENELAVADORA: Indica si el hogar tiene lavadora
                        create_dd('dd_fami_tienelavadora', '¿Tiene lavadora?', dd_params['fami_tienelavadora'], 'Tiene lavadora', 6),

                    ],style={'margin-bottom': '5px'}),


                ], title='Información personal y socioeconómica'
            ),

            ],
            id="accordion",
            always_open=False
        )
    ], className='col-md-5', style={'padding-left': '40px', 'padding-right': '40px', 'padding-top': '10px'}),  


    # ------------------------------------------------------------------------------------------------------------------
    #                                           PANEL DE LA DERECHA: PREDICCIÓN
    # ------------------------------------------------------------------------------------------------------------------
    html.Div([
        html.H3([html.I(className="fa fa-arrow-up-right-dots"),'\t Predicción del desempeño']),
        dcc.Markdown("Selecciona el **área del conocimiento** que deseas predecir:"),

        # Crear un menú desplegable para seleccionar el área del conocimiento
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(id="dd_area",
                    options=[
                        {'label': 'Matemáticas', 'value': 'matematicas'},
                        {'label': 'Ciencias naturales', 'value': 'ciencias_naturales'},
                        {'label': 'Ciencias sociales', 'value': 'ciencias_sociales'},
                        {'label': 'Lectura crítica', 'value': 'lectura_critica'},
                        {'label': 'Inglés', 'value': 'ingles'},
                    ],
                    placeholder="Área del conocimiento",
                    optionHeight=35,
                    persistence=True,
                    clearable=False,
                ),
            ], width=12, style={'margin-bottom': '10px'}),
        ], justify="center", style={'margin-bottom': '10px'}),
    
        # Gráfico de predicción del desempeño
        html.Div(
            dbc.Spinner(
                dcc.Graph(
                    id='predicted-performance-chart',
                    config={'displayModeBar': False, 'scrollZoom': False},
                ),
                size="lg",  # Ajusta el tamaño del spinner según tus preferencias
                color="primary",  # Cambia el color del spinner si es necesario
            ),
            style={'height': '200px', 'overflow': 'auto', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
        ),

        html.Hr(),

        # Título de la interpretación del desempeño
        html.H4([html.I(className="fa fa-magnifying-glass-chart"),'\t Interpretación del nivel de desempeño']),

        # Radio buttons para seleccionar el nivel de desempeño
        html.Div([
            dbc.RadioItems(
                id='radios',
                className="btn-group",  # Agrega la clase btn-group-toggle
                inputClassName="btn-check",
                labelClassName="btn btn-outline-primary",
                labelCheckedClassName="active",
                options=[],  # Se actualizará dinámicamente
                value=1,
            ),
        ], className="radio-group"),

        # Interpretación del nivel de desempeño
        dcc.Markdown(id='interpretacion-desempenho', dangerously_allow_html=True, style={'margin-top': '10px'}),

        # TODO: Eliminar estos componentes de prueba
        # Mostrar valores de dropdowns seleccionados
        html.Div(id='dd-output-container', style={'margin-top': '10px'}),
        html.Div(id='otro-componente'),


    ], className='col-md-7', style={'padding-left': '40px', 'padding-right': '40px', 'padding-top': '10px'})
    
], className= 'row')



# ======================================================================================================================
#                                                LÓGICA DE LA APLICACIÓN
# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------
#                               GRÁFICO DE PREDICCIÓN DEL DESEMPEÑO EN LA PRUEBA SABER 11
# ----------------------------------------------------------------------------------------------------------------------
@dash.callback(
    [
        Output('predicted-performance-chart', 'figure'),
        Output('dd-output-container', 'children'), # TODO: Eliminar esta salida cuando se conecte con el modelo
     ],  
    [Input(f'dd_{param}', 'value') for param in dd_params.keys()],
    [Input('dd_area', 'value')]
)
def display_selected_values(*values):

    # Separar los valores de los dropdowns de los valores del área del conocimiento
    dropdown_values = values[:-1]
    selected_area = values[-1]

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # NOTA 1 PARA ZAI: ESTA PARTE LA VAMOS A CONSERVAR ASÍ PORQUE ES LA QUE SE ENCARGA DE HACER LA PREDICCIÓN -------------------------------
    # TODO: Conectar con el modelo y hacer la predicción ------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Crear un diccionario para almacenar las evidencias
    evidence = {}

    # Evidencias de los dropdowns
    for param, value in zip(dd_params.keys(), dropdown_values):
        if value is not None:
            correct_param_name = param_name_mapping[0].get(f'dd_{param}', f'Unknown parameter: {param}')
            evidence[correct_param_name] = value  # Agregar el parámetro al diccionario

    # # Crear un objeto de inferencia por cada una de las áreas de desempeño y condicionarlo de acuerdo con selected_area
    # inferencia = infer.query(["Target"], evidence=evidence) # Target: éxito académico
    
    # Variable dummy para probar el funcionamiento del gráfico
    probability = len(evidence)*10
    desempenho = 0

    # Convertir puntaje a nivel de desempeño
    if selected_area == None or evidence == {}:
        desempenho = 0
    elif probability <= 25:
        desempenho = 1
    elif probability <= 50:
        desempenho = 2
    elif probability <= 75:
        desempenho = 3
    else:
        desempenho = 4

    # ------------------------------------------------------------------------------------------------------------------------------------------
    # FIN DE LA NOTA 1 PARA ZAI ----------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------------------------------

    # Crear el gráfico de predicción del desempeño
    fig = create_predicted_performance_chart(desempenho, selected_area)

    
    # TODO: Eliminar esta salida cuando se conecte con el modelo
    salida = html.Pre(json.dumps(evidence, indent=4, ensure_ascii=False))
    return [fig, salida]

    # return [fig]



# ----------------------------------------------------------------------------------------------------------------------
#                                                BOTONES DE NIVELES DE DESEMPEÑO
# ----------------------------------------------------------------------------------------------------------------------
@dash.callback(
    Output('radios', 'options'),
    [Input('dd_area', 'value')]
)
def generate_radio_options(selected_area):
    if selected_area == 'ingles':
        text_values = ["A-", "A1", "A2", "B1", "B+"]
    elif selected_area != None:
        total_blocks = 4  # Define el total de bloques según tus necesidades
        text_values = [str(i + 1) for i in range(total_blocks)]
    else:
        text_values = []

    options = [{'label': label, 'value': i + 1} for i, label in enumerate(text_values)]

    return options



# ----------------------------------------------------------------------------------------------------------------------
#                                                INTERPRETACIÓN DEL DESEMPEÑO
# ----------------------------------------------------------------------------------------------------------------------
@dash.callback(
    Output('interpretacion-desempenho', 'children'),
    [Input('radios', 'value'), Input('dd_area', 'value')]
)
def update_interpretacion_desempenho(nivel_desempenho, area_conocimiento):
    return interpretar_desempenho(area_conocimiento, nivel_desempenho)



# ----------------------------------------------------------------------------------------------------------------------
#                                                       LIMPIAR FORMULARIO
# ----------------------------------------------------------------------------------------------------------------------
@dash.callback(
    [Output(f'dd_{param}', 'value') for param in dd_params.keys()],
    [Input('clear-button', 'n_clicks')],
    prevent_initial_call=True
)
def clear_form(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        
        # Clear the dropdowns
        output_values = {f'dd_{param}': None for param in dd_params.keys()}
        return [output_values[param] for param in output_values]
    
    else:
        raise PreventUpdate



# ----------------------------------------------------------------------------------------------------------------------
#                                                       PROGRESO
# ----------------------------------------------------------------------------------------------------------------------
@dash.callback(
    [Output('progress-bar', 'value'),Output('progress-bar', 'label')],
    [Input(f'dd_{param}', 'value') for param in dd_params.keys()]
)
def update_progress_bar(*values):
    # Calcula el progreso en función del número de valores ingresados
    total_params = len(dd_params)  # Total de parámetros (dropdowns y créditos)
    
    # Cuenta el número de parámetros diligenciados en dropdowns
    filled_params = sum([value is not None for value in values])
       
    # Calcula el progreso con dos decimales
    progress = round(filled_params / total_params * 100)

    return progress, f"{progress} %" if progress >= 5 else ""