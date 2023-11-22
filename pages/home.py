import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.graph_objects as go
import json
import pickle
from pgmpy.inference import VariableElimination
from dash.exceptions import PreventUpdate

templates = ["cerulean"]
load_figure_template(templates)

# Registrar la página
dash.register_page(__name__, path='/')


# ======================================================================================================================
#                                   CARGA DE DATOS, MODELOS Y DESCARGO DE RESPONSABILIDAD             
# ======================================================================================================================
{}
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

# Cargar modelo entrenado desde el archivo
try:
    with open('assets/modelo_entrenado.pkl', 'rb') as f:
        loaded_model = pickle.load(f)
except FileNotFoundError:
    print("El archivo del modelo no se encontró.")
except pickle.UnpicklingError:
    print("Error al cargar el modelo.")
    loaded_model = None

# Crea un objeto de inferencia
infer = VariableElimination(loaded_model)



# ======================================================================================================================
#                                               FUNCIONES AUXILIARES
# ======================================================================================================================

# Función para crear un menú desplegable de Bootstrap
def create_dd(id, label, options, placeholder, width=12, optionHeight=35):
    """
    Crea un menú desplegable de Bootstrap.

    Args:
        id (str): Identificador del menú desplegable.
        label (str): Etiqueta del menú desplegable.
        options (list): Opciones del menú desplegable. Cada opción es un diccionario con las claves 'label' y 'value'.
        placeholder (str): Placeholder del menú desplegable.
        width (int, optional): Ancho del menú desplegable. Defaults to 12.
        optionHeight (int, optional): Altura de las opciones del menú desplegable. Defaults to 35.
    
    Returns:
        dbc.Col: Menú desplegable de Bootstrap.
    """
    return dbc.Col([
        dbc.Label(label, html_for=id, size="sm"),
        dcc.Dropdown(id=id, 
            options=options,
            placeholder=placeholder,
            optionHeight=optionHeight,
            persistence=True  # Habilitar la persistencia para mantener el estado
        ),
    ], width=width)

# Función para crear un botón de información de Bootstrap
def create_info_btn(button_id, width=1):
    """
    Crea un botón de información de Bootstrap.

    Args:
        button_id (str): Identificador del botón.
        width (int, optional): Ancho del botón. Defaults to 1.

    Returns:
        dbc.Col: Botón de información de Bootstrap.
    """
    return dbc.Col([
        html.Button("ℹ️", id=button_id, className="btn btn-info", style={'float': 'right'}),
        dbc.Popover(
            [
                dbc.PopoverHeader("Input Requirements"),
                dbc.PopoverBody("Please provide values for both 'Approved Credits' and 'Enrolled Credits' to have them factored into the model."),
            ],
            id=f"popover-{button_id}",
            target=button_id,
            trigger="hover",
        ),
    ], width=width)



# ======================================================================================================================
#                                               CONTENIDO DE LA PÁGINA
# ======================================================================================================================

layout = html.Div([

    # ------------------------------------------------------------------------------------------------------------------
    #                                           PANEL DE LA IZQUIERDA: FORMULARIO
    # ------------------------------------------------------------------------------------------------------------------
    html.Div([

        # Título del formulario
        html.H3([
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
            
            # Menú desplegable 1: Información personal
            dbc.AccordionItem([

                        # Fila 1
                        dbc.Row([

                            # Gender
                            create_dd('dd_gender', 'Gender', dd_params['gender'], 'Gender', 6),

                            # Age at enrollment
                            create_dd('dd_age_at_enrollment', 'Age at enrollment', dd_params['age_at_enrollment'], 'Age at enrollment', 6),

                        ],style={'margin-bottom': '5px'}),

                    ], title='Información personal'
                ),

                # Menú desplegable 2: Información socioeconómica
                dbc.AccordionItem(
                    [
                        # Fila 1
                        dbc.Row([

                            # Occupation of financial responsible party (occup_fin_res_party)
                            create_dd('dd_occup_fin_res_party', 'Occupation of financial responsible party', dd_params['occup_fin_res_party'], 'Occupation of financial responsible party', 12, 55),

                        ],style={'margin-bottom': '5px'}),

                        # Fila 2
                        dbc.Row([
                           
                            # Debtor
                            create_dd('dd_debtor', 'Debtor', dd_params['debtor'], 'Debtor', 6),

                            # Scholarship holder (scholarship)
                            create_dd('dd_scholarship', 'Scholarship holder', dd_params['scholarship'], 'Scholarship holder', 6),

                        ],style={'margin-bottom': '5px'}),

                    ],
                    title='Información socieconómica'
                ),

                # Menú desplegable 3: Información del colegio
                    dbc.AccordionItem(
                        [
                            # Fila 1
                            dbc.Row([

                                # Course
                                create_dd('dd_course', 'Course', dd_params['course'], 'Course'),

                            ],style={'margin-bottom': '5px'}),

                            # Fila 2
                            dbc.Row([

                                # Admission grade
                                create_dd('dd_admission_grade', 'Admission grade', dd_params['admission_grade'], 'Admission grade'),

                            ],style={'margin-bottom': '5px'}),
                                
                        ],
                        title='Información del colegio'
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
        html.H3("Predicción del puntaje global"),
        html.P("Texto que acompañará el gráfico con la predicción del modelo."),
        html.Div(
            dbc.Spinner(
                dcc.Graph(
                    id='gauge-graph',
                ),
                size="lg",  # Ajusta el tamaño del spinner según tus preferencias
                color="primary",  # Cambia el color del spinner si es necesario
            ),
            style={'height': '180px', 'overflow': 'auto', 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
        ),

    ], className='col-md-7', style={'padding-left': '40px', 'padding-right': '40px', 'padding-top': '10px'})
    
], className= 'row')



# ======================================================================================================================
#                                                LÓGICA DE LA APLICACIÓN
# ======================================================================================================================

# ----------------------------------------------------------------------------------------------------------------------
#                                                       GAUGE GRAPH
# ----------------------------------------------------------------------------------------------------------------------
@dash.callback(
    [Output('gauge-graph', 'figure')],  
    [Input(f'dd_{param}', 'value') for param in dd_params.keys()]
)
def display_selected_values(*values):
    """
    Esta función se encarga de actualizar el gráfico de gauge con la predicción del modelo.

    Args:
        *values: Valores de los parámetros del formulario.

    Returns:
        dcc.Graph: Gráfico de gauge con la predicción del modelo.
    """

    # NOTA 1 PARA ZAI: ESTA PARTE LA VAMOS A CONSERVAR ASÍ PORQUE ES LA QUE SE ENCARGA DE HACER LA PREDICCIÓN -------------------------------

    # TODO: Conectar con el modelo y hacer la predicción

    # Crear un diccionario para almacenar las evidencias
    evidence = {}

    # Evidencias de los dropdowns
    for param, value in zip(dd_params.keys(), values):
        if value is not None:
            correct_param_name = param_name_mapping[0].get(f'dd_{param}', f'Unknown parameter: {param}')
            evidence[correct_param_name] = value  # Agregar el parámetro al diccionario

    # # Se predice la probabilidad de éxito académico
    # inferencia = infer.query(["Target"], evidence=evidence) # Target: éxito académico

    # # Tomar el valor de inferencia.values[0] redondearlo a 2 decimales y multiplicarlo por 100
    # probability = round(inferencia.values[0] * 100, 2)
    probability = len(evidence)*10

    # FIN DE LA NOTA 1 PARA ZAI ----------------------------------------------------------------------------------------------------------------
    
    # Crear el gráfico de gauge
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=probability,
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': 'darkblue'},
            'bar': {'color': '#29339b', 'thickness': 0.5},
            'steps': [
                {'range': [0, 25], 'color': '#FFA78E'},
                {'range': [25, 75], 'color': '#FFDF9C'},
                {'range': [75, 100], 'color': '#91DEBF'}
            ],
            'threshold': {'line': {'color': '#4CA98F', 'width': 4}, 'thickness': 0.75, 'value': 85},
            'borderwidth': 2, 
            'bordercolor': 'gray'
        }
    ))

    fig.update_layout(
        margin=dict(t=50, b=10),  # Ajusta el margen del gráfico
        height=180,  # Ajusta la altura de la figura
        width=500,  # Ajusta el ancho de la figura
        template=templates[0]  # Aplica el tema
    )

    return [fig]


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