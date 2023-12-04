from dash import dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# ======================================================================================================================
#                                       FUNCIONES AUXILIARES PARA home.py
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
    """
    Retorna la interpretación del desempeño de un estudiante en la prueba Saber para un área específica del conocimiento.

    Args:
        area_conocimiento (str): Área del conocimiento para la cual se está realizando la predicción.
        nivel_desempenho (int): Nivel de desempeño predicho.

    Returns:
        str: Interpretación del desempeño.
    """

    # Definir el texto de interpretación según el área del conocimiento
    if area_conocimiento == 'matematicas':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "- El estudiante que se ubica en este nivel probablemente puede leer información puntual (un dato, por ejemplo) relacionada con situaciones cotidianas y presentada en tablas o gráficas con escala explícita, cuadrícula o, por lo menos, líneas horizontales."
        elif nivel_desempenho == 2:
            return "- Además de lo descrito en el nivel 1, el estudiante que se ubica en este nivel es capaz de comparar y establecer relaciones entre los datos presentados, e identificar y extraer información local y global de manera directa. Lo anterior en contextos familiares o personales que involucran gráficas con escala explícita, cuadrícula o, por lo menos, líneas horizontales u otros formatos con poca información."
        elif nivel_desempenho == 3:
            return "- Además de lo descrito en los niveles 1 y 2, el estudiante que se ubica en este nivel selecciona información, señala errores y hace distintos tipos de transformaciones y manipulaciones aritméticas y algebraicas sencillas; esto para enfrentarse a problemas que involucran el uso de conceptos de proporcionalidad, factores de conversión, áreas y desarrollos planos, en contextos laborales u ocupacionales, matemáticos o científicos, y comunitarios o sociales."
        elif nivel_desempenho == 4:
            return "- Además de lo descrito en los niveles 1, 2 y 3, el estudiante que se ubica en este nivel resuelve problemas y justifica la veracidad o falsedad de afirmaciones que requieren el uso de conceptos de probabilidad, propiedades algebraicas, relaciones trigonométricas y características de funciones reales. Lo anterior, en contextos principalmente matemáticos o científicos abstractos."
        else:
            return "Selecciona un nivel de desempeño para ver la interpretación."

    elif area_conocimiento == 'ciencias_naturales':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "- El estudiante que se ubica en este nivel muy posiblemente alcanza a reconocer información explícita, presentada de manera ordenada en tablas o gráficas, con un lenguaje cotidiano y que implica la lectura de una sola variable independiente. Por lo tanto, estos estudiantes demuestran un insuficiente desarrollo de la competencia *Indagación* definida en el marco teórico de la prueba."
        elif nivel_desempenho == 2:
            return "- Además de lo descrito en el nivel 1, el estudiante que se ubica en este nivel reconoce información suministrada en tablas, gráficas y esquemas de una sola variable independiente, y la asocia con nociones de los conceptos básicos de las ciencias naturales (*tiempo, posición, velocidad, imantación y filtración*)."
        elif nivel_desempenho == 3:
            return "- Además de lo descrito en los niveles 1 y 2, el estudiante que se ubica en este nivel interrelaciona conceptos, leyes y teorías científicas con información presentada en diversos contextos, en los que intervienen dos o más variables, para hacer inferencias sobre una situación problema o un fenómeno natural."
        elif nivel_desempenho == 4:
            return "- Además de lo descrito en los niveles 1, 2 y 3, el estudiante que se ubica en este nivel usa conceptos, teorías o leyes en la solución de situaciones problema que involucran procedimientos, habilidades, conocimientos y un lenguaje propio de las ciencias naturales."
        else:
            return "Selecciona un nivel de desempeño para ver la interpretación."    


    elif area_conocimiento == 'ciencias_sociales':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "- El estudiante que se ubica en este nivel podría reconocer algunos derechos ciudadanos en situaciones sencillas. Adicionalmente, podría reconocer factores que generan un conflicto e identificar creencias que explican algunos comportamientos."
        elif nivel_desempenho == 2:
            return "- Además de lo descrito en el nivel anterior, el estudiante que se ubica en este nivel reconoce deberes del Estado colombiano y situaciones de protección o vulneración de derechos en el marco del Estado social de derecho; identifica relaciones entre conductas de las personas y sus cosmovisiones; y reconoce las dimensiones presentes en una situación, problema, decisión tomada o propuesta de solución. Además, contextualiza fuentes y procesos sociales."
        elif nivel_desempenho == 3:
            return "- Además de lo descrito en los niveles anteriores, el estudiante que se ubica en este nivel identifica prejuicios o intenciones contenidos en una afirmación y reconoce las dimensiones e intereses involucrados en un problema o alternativa de solución. Asimismo, identifica algunos conceptos básicos de las ciencias sociales y modelos conceptuales, y valora y contextualiza la información presentada en una fuente."
        elif nivel_desempenho == 4:
            return "- Además de lo descrito en los niveles anteriores, el estudiante que se ubica en este nivel conoce algunas disposiciones de la Constitución Política de Colombia que posibilitan la participación ciudadana y el control a los poderes públicos; analiza y compara enunciados, intereses y argumentos; y evalúa alternativas de solución a un problema. \n Este estudiante analiza situaciones a partir de conceptos básicos de las ciencias sociales o de contextos históricos y/o geográficos. A su vez, relaciona fuentes y políticas con modelos conceptuales, y valora los contenidos de una fuente."
        else:
            return "Selecciona un nivel de desempeño para ver la interpretación." 
        
    elif area_conocimiento == 'lectura_critica':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "- El estudiante que se ubica en este nivel probablemente identifica elementos literales en textos continuos y discontinuos sin establecer relaciones de significado."
        elif nivel_desempenho == 2:
            return "- Además de lo que logra hacer en el nivel 1, el estudiante que se ubica en este nivel comprende textos continuos y discontinuos de manera literal. Asimismo, reconoce información explícita y la relaciona con el contexto."
        elif nivel_desempenho == 3:
            return "- Además de lo descrito en los niveles 1 y 2, el estudiante que se ubica en este nivel interpreta información de textos al inferir contenidos implícitos y reconocer estructuras, estrategias discursivas y juicios valorativos."
        elif nivel_desempenho == 4:
            return "- Además de lo descrito en los niveles 1, 2 y 3, el estudiante que se ubica en este nivel reflexiona a partir de un texto sobre la visión de mundo del autor (costumbres, creencias, juicios, carácter ideológico-político y posturas éticas, entre otros). Asimismo, da cuenta de elementos paratextuales significativos presentes en el texto. Finalmente, valora y contrasta los elementos mencionados."
        else:
            return "Selecciona un nivel de desempeño para ver la interpretación." 


    elif area_conocimiento == 'ingles':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "- El estudiante promedio clasificado en este nivel probablemente puede comprender algunas oraciones simples como preguntas o instrucciones, y utilizar vocabulario básico para nombrar personas u objetos que le son familiares."
        elif nivel_desempenho == 2:
            return "- Además de lo descrito en el nivel A-, el estudiante que se clasifica en este nivel puede comprender situaciones comunicativas sencillas y concretas en las que se haga uso de expresiones básicas para proporcionar información personal, y fórmulas de saludo, despedida, indicaciones de lugares, etc."
        elif nivel_desempenho == 3:
            return "- Además de lo descrito en los niveles A- y A1, el estudiante que se clasifica en este nivel puede comprender información específica en textos sencillos cotidianos, además de comunicarse mediante el uso de expresiones de uso diario para realizar y responder invitaciones, sugerencias, disculpas, etc."
        elif nivel_desempenho == 4:
            return "- Además de lo descrito en los niveles A-, A1y A2, el estudiante que se clasifica en este nivel posee un amplio vocabulario para comprender textos de temáticas específicas que son de su interés personal. De igual manera, el estudiante en este nivel logra comunicarse con cierta seguridad en asuntos que le son poco habituales, y puede expresar y comprender diversas opiniones y actitudes."
        elif nivel_desempenho == 5:
            return "- El estudiante promedio clasificado en este nivel supera las preguntas de mayor complejidad de la prueba. Este estudiante, además de lo descrito en los niveles A-, A1, A2 y B1, probablemente puede comprender textos y discursos sobre temáticas abstractas, gracias a que posee un amplio vocabulario de lectura. Asimismo, el estudiante probablemente puede comunicarse en diferentes contextos generales o académicos de manera espontánea."
        else:
            return "Selecciona un nivel de desempeño para ver la interpretación." 
        
    else:
        return "Selecciona un área del conocimiento para ver la interpretación de los niveles de desempeño."
        
