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

# Obtener el diccionario de correspondencias entre los nombres de los parámetros y los nombres de las variables del modelo
param_name_mapping = all_params.get('param_name_mapping', {})



# ======================================================================================================================
#                                               CARGA DE MODELOS
# ======================================================================================================================
model_names = ['modelo_entrenado_ENG', 'modelo_entrenado_LEC', 'modelo_entrenado_MATH',
               'modelo_entrenado_NATUR', 'modelo_entrenado_SOC', 'modelo_entrenado_Global']

# Crear un diccionario para almacenar los modelos cargados
loaded_models = {}

# Cargar los modelos desde los archivos .pkl en la carpeta 'assets'
for model_name in model_names:
    try:
        with open(f'assets/{model_name}.pkl', 'rb') as f:
            loaded_models[model_name] = pickle.load(f)
    except FileNotFoundError:
        print(f"El archivo del modelo {model_name} no se encontró.")
        loaded_models[model_name] = None
    except pickle.UnpicklingError:
        print(f"Error al cargar el modelo {model_name}.")
        loaded_models[model_name] = None

# Crear objetos de inferencia para cada modelo cargado
inference_objects = {model_name: VariableElimination(loaded_model) if loaded_model else None
                     for model_name, loaded_model in loaded_models.items()}

# Mapeo de áreas a modelos de inferencia
area_to_model_mapping = all_params.get('area_to_model_mapping', {})[0]

# Diccionario que hace corresponder el nombre del área del conocimiento del dropdown con el nombre de las variables objetivo de los modelos
target_variable = all_params.get('target_variable', {})[0]

# Función para realizar la inferencia
def realizar_inferencia(area_seleccionada):
    """
    Realiza la inferencia con el modelo de inferencia correspondiente al área seleccionada.

    args:
        area_seleccionada (str): Nombre del área seleccionada.

    returns:
        objeto_de_inferencia (VariableElimination): Objeto de inferencia para el área seleccionada.
    """
    modelo_entrenado_key = area_to_model_mapping.get(area_seleccionada)
    
    if modelo_entrenado_key:
        objeto_de_inferencia = inference_objects.get(modelo_entrenado_key)
        return objeto_de_inferencia
    else:
        return f"No se encontró un objeto de inferencia para el área {area_seleccionada}"



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

                    # Fila 1
                    dbc.Row([

                        # COLE_SUBREGION: Subregión del Establecimiento
                        create_dd('dd_cole_subregion', 'Subregión', dd_params['cole_subregion'], 'Subregión', 6),

                        # SEMAFORO_VIOL: Nivel de violencia del municipio en el que se encuentra el Establecimiento
                        create_dd('dd_semaforo_viol', 'Nivel de violencia', dd_params['semaforo_viol'], 'Nivel de violencia', 6),
                        

                    ],style={'margin-bottom': '5px'}),

                    # Fila 1
                    dbc.Row([

                        # COLE_AREA_UBICACION: Área de ubicación de la Sede
                        create_dd('dd_cole_area_ubicacion', 'Área de ubicación de la Sede', dd_params['cole_area_ubicacion'], 'Área de ubic. de la Sede', 12),

                    ],style={'margin-bottom': '5px'}),

                    # Fila 2
                    dbc.Row([

                        # COLE_JORNADA: Jornada del Establecimiento
                        create_dd('dd_cole_jornada', 'Jornada', dd_params['cole_jornada'], 'Jornada', 6),

                        # COLE_BILINGUE: Indica si el Establecimiento es bilingue o no
                        create_dd('dd_cole_bilingue', 'Bilingüe', dd_params['cole_bilingue'], 'Bilingüe', 6),

                    ],style={'margin-bottom': '5px'}),
                       
                ],
                title='Información del colegio'
            ),

            # Menú desplegable 2: Información personal del estudiante
            dbc.AccordionItem([

                # Fila 1
                    dbc.Row([

                        # ESTU_GENERO: Género del estudiante
                        create_dd('dd_estu_genero', 'Género del estudiante', dd_params['estu_genero'], 'Género', 6),

                        # ESTU_EDAD: Edad del estudiante
                        create_dd('dd_estu_edad', 'Edad del estudiante', dd_params['estu_edad'], 'Edad', 6),

                    ],style={'margin-bottom': '5px'}),

            ], title='Información personal del estudiante'),


            # Menú desplegable 3: Información socioeconómica del estudiante
            dbc.AccordionItem([

                    # Fila 1
                    dbc.Row([

                        # FAMI_EDUCACION_MoP: Máxima educación alcanzada por la madre o el padre
                        create_dd('dd_fami_educacion_mop', 'Educación de la madre o el padre', dd_params['fami_educacion_mop'], 'Educación de la madre o el padre', 12),
                        
                    ],style={'margin-bottom': '5px'}),

                    # Fila 2
                    dbc.Row([

                        # FAMI_ESTRATOVIVIENDA: Estrato de la vivienda
                        create_dd('dd_fami_estratovivienda', 'Estrato de vivienda', dd_params['fami_estratovivienda'], 'Estrato', 12),

                    ],style={'margin-bottom': '15px'}),

                    # Fila 3
                    dbc.Row([

                        # FAMI_RECURSOS: Recursos del hogar
                        dbc.Label("Recursos del hogar", html_for="fami_recursos", size="sm"),
                        dbc.Checklist(
                            options=[
                                {"label": "¿Tiene internet?", "value": 4}, 
                                {"label": "¿Tiene computador?", "value": 3},
                                {"label": "¿Tiene lavadora?", "value": 2},
                                {"label": "¿Tiene automóvil?", "value": 1},
                            ],
                            value=[],
                            id="fami_recursos",
                            inline=False,
                            switch=True,
                            persistence=True,
                        ),

                    ],style={'margin-bottom': '5px'}),


                ], title='Información socioeconómica del estudiante',
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
                        {'label': 'Global', 'value': 'global'}
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

        # Markdown con la interpretación del desempeño
        dcc.Markdown(id='interpretacion-desempenho', dangerously_allow_html=True, style={'margin-top': '10px'}),

        # TODO: Eliminar estos componentes de prueba
        # Mostrar valores de dropdowns seleccionados
        html.Div(id='dd-output-container', style={'margin-top': '10px'}),


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
        # Output('dd-output-container', 'children'), # TODO: Eliminar esta salida cuando se conecte con el modelo
     ],  
    [Input(f'dd_{param}', 'value') for param in dd_params.keys()],
    [Input('fami_recursos', 'value')],
    [Input('dd_area', 'value')]
)
def display_selected_values(*values):

    # Separar los valores de los dropdowns de los valores de los recursos y el área de conocimiento
    dropdown_values = values[:-2]
    recursos = values[-2]
    selected_area = values[-1]

    # Crear un diccionario para almacenar las evidencias
    evidence = {}

    # Evidencias de los dropdowns
    for param, value in zip(dd_params.keys(), dropdown_values):
        if value is not None:
            correct_param_name = param_name_mapping[0].get(f'dd_{param}', f'Unknown parameter: {param}')
            evidence[correct_param_name] = value  # Agregar el parámetro al diccionario

    # Evidencias de los recursos
    if recursos is not None:
        evidence['FAMI_RECURSOS'] = sum(recursos)

    # Crear un objeto de inferencia por de acuerdo al área seleccionada
    infer = realizar_inferencia(selected_area)

    # Selección de la variable objetivo del modelo y hacer query con objeto de inferencia
    target = target_variable[selected_area]
    inferencia = infer.query([target], evidence=evidence) # Target: éxito académico
    
    # Desempeño: Corresponde al índice del valor máximo en inferencia.values + 1  
    desempenho = inferencia.values.argmax()+1

    # Impresiones de prueba
    # print(inferencia) 
    # print(inferencia.values)
    # print(desempenho)

    # Crear el gráfico de predicción del desempeño
    fig = create_predicted_performance_chart(desempenho, selected_area)
   
    # # TODO: Eliminar esta salida cuando se conecte con el modelo
    # salida = html.Pre(json.dumps(evidence, indent=4, ensure_ascii=False))
    # return [fig, salida]

    return [fig]



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
        if selected_area == 'global':
            total_blocks = 5
        else:
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
    [Output(f'dd_{param}', 'value') for param in dd_params.keys()] +
    [Output("fami_recursos", "value")],
    [Input('clear-button', 'n_clicks')],
    prevent_initial_call=True
)
def clear_form(n_clicks):
    if n_clicks is not None and n_clicks > 0:
        
        # Clear the dropdowns
        output_values = {f'dd_{param}': None for param in dd_params.keys()}

        # Clear the fami_recursos switches
        fami_recursos_value = []

        return [output_values[param] for param in output_values] + [fami_recursos_value]
    
    else:
        raise PreventUpdate


# ----------------------------------------------------------------------------------------------------------------------
#                                                       PROGRESO
# ----------------------------------------------------------------------------------------------------------------------
@dash.callback(
    [Output('progress-bar', 'value'),Output('progress-bar', 'label')],
    [Input(f'dd_{param}', 'value') for param in dd_params.keys()],
)
def update_progress_bar(*values):
    # Calcula el progreso en función del número de valores ingresados
    total_params = len(dd_params)+1  # Total de parámetros (dropdowns y recursos)
    
    # Cuenta el número de parámetros diligenciados en dropdowns
    filled_params = sum([value is not None for value in values])+1 # Suma 1 por los recursos
       
    # Calcula el progreso con dos decimales
    progress = round(filled_params / total_params * 100)

    return progress, f"{progress} %" if progress >= 5 else ""