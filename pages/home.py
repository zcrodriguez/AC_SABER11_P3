import dash
from dash import html, dcc, Input, Output, State
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

# Función para crear un gráfico de bloques
def create_predicted_performance_chart(selected_blocks, area_conocimiento):
    """
    Crea un gráfico que representa el nivel de desempeño de un estudiante en la prueba Saber para un área específica del conocimiento.

    Args:
        selected_blocks (int): Número de bloques seleccionados que indican el nivel de desempeño predicho.
        area_conocimiento (str): Área del conocimiento para la cual se está realizando la predicción.

    Returns:
        dcc.Graph: Gráfico de rendimiento predicho con bloques y anotaciones visuales.
    """

    # Determina el total de bloques según el área de conocimiento (por ejemplo, 4 bloques para áreas distintas a inglés, 5 para inglés)
    total_blocks = 5 if area_conocimiento == 'ingles' else 4

    # Define colores según el nivel de desempeño predicho
    colors = ['blue' if i < selected_blocks else 'lightgrey' for i in range(total_blocks)]

    # Define etiquetas para cada bloque según el área de conocimiento
    text_values = ["A-", "A1", "A2", "B1", "B+"] if area_conocimiento == 'ingles' else [str(i + 1) for i in range(total_blocks)]

    fig = go.Figure()

    for i in range(total_blocks):
        height = i + 1
        fig.add_hline(y=height, line_width=3, line_color="white")

        bar = go.Bar(
            y=[height],
            x=[i + 1],
            width=0.8,
            marker_color=colors[i],
            showlegend=False,
            hoverinfo='none'
        )

        text = go.Scatter(
            x=[i + 1],
            y=[height + 0.3],
            text=[text_values[i]],
            mode='text',
            showlegend=False,
            hoverinfo='none'
        )

        fig.add_traces([bar, text])

        # Agrega una flecha indicadora para el nivel de desempeño seleccionado
        if i + 1 == selected_blocks:
            fig.add_annotation(
                x=i + 1,
                y=height + 0.9,
                text="▼",
                showarrow=False,
                font=dict(size=16)
            )

    # Configura el diseño del gráfico
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    fig.update_layout(height=200, width=400)

    return fig


# Función que retorna interpretación del desempeño por área del conocimiento y por nivel de desempeño
def interpretar_desempenho(area_conocimiento, nivel_desempenho):

    # Definir el texto de interpretación según el área del conocimiento
    if area_conocimiento == 'matematicas':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "El estudiante que se ubica en este nivel probablemente puede leer información puntual (un dato, por ejemplo) relacionada con situaciones cotidianas y presentada en tablas o gráficas con escala explícita, cuadrícula o, por lo menos, líneas horizontales."
        elif nivel_desempenho == 2:
            return "- Compara datos de dos variables presensentadas en una misma gráfica sin necesidad de hacer operaciones aritméticas. \n- Identifica valores o puntos representativos en diferentes tipos de registro a partir del significado que tienen en la situación. \n- Interpreta información presentada en tablas o gráficas con escala explícita, cuadrícula o, por lo menos, líneas horizontales."
        elif nivel_desempenho == 3:
            return "El estudiante se encuentra en el nivel de desempeño medio. Se recomienda que el estudiante refuerce sus conocimientos en el área de matemáticas."
        elif nivel_desempenho == 4:
            return "El estudiante se encuentra en el nivel de desempeño alto. Se recomienda que el estudiante refuerce sus conocimientos en el área de matemáticas."
        elif nivel_desempenho == 5:
            return "El estudiante se encuentra en el nivel de desempeño más alto. ¡Felicitaciones!"
        else:
            return "No se ha seleccionado un nivel de desempeño válido."
    

    elif area_conocimiento == 'ciencias_naturales':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "El estudiante se encuentra en el nivel de desempeño más bajo. Se recomienda que el estudiante refuerce sus conocimientos en el área de ciencias naturales."
        
        elif nivel_desempenho == 2:
            return "El estudiante se encuentra en el nivel de desempeño bajo. Se recomienda que el estudiante refuerce sus conocimientos en el área de ciencias naturales."
        
        elif nivel_desempenho == 3:
            return "El estudiante se encuentra en el nivel de desempeño medio. Se recomienda que el estudiante refuerce sus conocimientos en el área de ciencias naturales."
        
        elif nivel_desempenho == 4:
            return "El estudiante se encuentra en el nivel de desempeño alto. Se recomienda que el estudiante refuerce sus conocimientos en el área de ciencias naturales."
        
        elif nivel_desempenho == 5:
            return "El estudiante se encuentra en el nivel de desempeño más alto. ¡Felicitaciones!"
        
        else:
            return "No se ha seleccionado un nivel de desempeño válido."


    elif area_conocimiento == 'ciencias_sociales':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "El estudiante se encuentra en el nivel de desempeño más bajo. Se recomienda que el estudiante refuerce sus conocimientos en el área de ciencias sociales."
        
        elif nivel_desempenho == 2:
            return "El estudiante se encuentra en el nivel de desempeño bajo. Se recomienda que el estudiante refuerce sus conocimientos en el área de ciencias sociales."
        
        elif nivel_desempenho == 3:
            return "El estudiante se encuentra en el nivel de desempeño medio. Se recomienda que el estudiante refuerce sus conocimientos en el área de ciencias sociales."
        
        elif nivel_desempenho == 4:
            return "El estudiante se encuentra en el nivel de desempeño alto. Se recomienda que el estudiante refuerce sus conocimientos en el área de ciencias sociales."
        
        elif nivel_desempenho == 5:
            return "El estudiante se encuentra en el nivel de desempeño más alto. ¡Felicitaciones!"
        
        else:
            return "No se ha seleccionado un nivel de desempeño válido."


    elif area_conocimiento == 'lectura_critica':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "El estudiante se encuentra en el nivel de desempeño más bajo. Se recomienda que el estudiante refuerce sus conocimientos en el área de lectura crítica."
        
        elif nivel_desempenho == 2:
            return "El estudiante se encuentra en el nivel de desempeño bajo. Se recomienda que el estudiante refuerce sus conocimientos en el área de lectura crítica."
        
        elif nivel_desempenho == 3:
            return "El estudiante se encuentra en el nivel de desempeño medio. Se recomienda que el estudiante refuerce sus conocimientos en el área de lectura crítica."
        
        elif nivel_desempenho == 4:
            return "El estudiante se encuentra en el nivel de desempeño alto. Se recomienda que el estudiante refuerce sus conocimientos en el área de lectura crítica."
        
        elif nivel_desempenho == 5:
            return "El estudiante se encuentra en el nivel de desempeño más alto. ¡Felicitaciones!"
        
        else:
            return "No se ha seleccionado un nivel de desempeño válido."


    elif area_conocimiento == 'ingles':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "- El estudiante se encuentra en el nivel de desempeño más bajo. Se recomienda que el estudiante refuerce sus conocimientos en el área de inglés. \n- El estudiante se encuentra en el nivel de desempeño más bajo. Se recomienda que el estudiante refuerce sus conocimientos en el área de inglés."
        
        elif nivel_desempenho == 2:
            return "El estudiante se encuentra en el nivel de desempeño bajo. Se recomienda que el estudiante refuerce sus conocimientos en el área de inglés."
        
        elif nivel_desempenho == 3:
            return "El estudiante se encuentra en el nivel de desempeño medio. Se recomienda que el estudiante refuerce sus conocimientos en el área de inglés."
        
        elif nivel_desempenho == 4:
            return "El estudiante se encuentra en el nivel de desempeño alto. Se recomienda que el estudiante refuerce sus conocimientos en el área de inglés."
        
        elif nivel_desempenho == 5:
            return "El estudiante se encuentra en el nivel de desempeño más alto. ¡Felicitaciones!"
        
        else:
            return "No se ha seleccionado un nivel de desempeño válido."
        
    else:
        return ""
        



# ======================================================================================================================
#                                               CONTENIDO DE LA PÁGINA
# ======================================================================================================================

layout = html.Div([

    # Elemento para almacenar el nivel de desempeño predicho
    dcc.Store(id='desempenho-store', storage_type='memory'),

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
                    persistence=True  # Habilitar la persistencia para mantener el estado
                ),
            ], width=12, style={'margin-bottom': '10px'}),
        ], justify="center", style={'margin-bottom': '10px'}),
    
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

        # Mostrar valores de dropdowns seleccionados
        html.Div(id='dd-output-container', style={'margin-top': '10px'}),
        
        # TODO: Eliminar estos componentes de prueba
        html.Hr(),
        html.Div(id='otro-componente'),

        # Interpretación del desempeño
        html.H4([html.I(className="fa fa-magnifying-glass-chart"),'\t Interpretación']),

        # Markdown con la interpretación del desempeño
        dcc.Markdown(id='interpretacion-desempenho', style={'margin-top': '10px'}),

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
        Output('interpretacion-desempenho', 'children'),
        Output('desempenho-store', 'data')
     ],  
    [Input(f'dd_{param}', 'value') for param in dd_params.keys()],
    [Input('dd_area', 'value')]
)
def display_selected_values(*values):

    # Separar los valores de los dropdowns de los valores del área del conocimiento
    dropdown_values = values[:-1]
    selected_area = values[-1]

    # NOTA 1 PARA ZAI: ESTA PARTE LA VAMOS A CONSERVAR ASÍ PORQUE ES LA QUE SE ENCARGA DE HACER LA PREDICCIÓN -------------------------------
    # TODO: Conectar con el modelo y hacer la predicción

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
    elif probability <= 75:
        desempenho = 2
    else:
        desempenho = 3

    # FIN DE LA NOTA 1 PARA ZAI ----------------------------------------------------------------------------------------------------------------
    
    # Crear el gráfico de gauge
    # Ejemplo de uso: cambia el número y el área del conocimiento para ver cómo se actualiza el gráfico
    fig = create_predicted_performance_chart(desempenho, selected_area)

    # Retornar html.pre con evidence
    # TODO: Eliminar esta salida cuando se conecte con el modelo
    salida = html.Pre(json.dumps(evidence, indent=4, ensure_ascii=False)) 

    # Retornar interpretación del desempeño
    interpretacion = interpretar_desempenho(selected_area, desempenho)

    return [fig, salida, interpretacion, desempenho]



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


@dash.callback(
    Output('otro-componente', 'children'),
    [Input('desempenho-store', 'modified_timestamp')],
    [State('desempenho-store', 'data')]
)
def otro_callback(timestamp, desempenho):
    if timestamp is None:
        raise dash.exceptions.PreventUpdate

    return f"El desempeño es: {desempenho}"