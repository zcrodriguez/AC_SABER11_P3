from dash import dcc, html
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
    total_blocks = 5 if area_conocimiento == 'ingles' or area_conocimiento == 'global' else 4

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


# ======================================================================================================================
#                                       FUNCIONES AUXILIARES PARA visualizations.py
# ======================================================================================================================

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
            return "##### ✍🏽 Puntaje: 0 a 35 \n - El estudiante que se ubica en este nivel probablemente puede leer información puntual (un dato, por ejemplo) relacionada con situaciones cotidianas y presentada en tablas o gráficas con escala explícita, cuadrícula o, por lo menos, líneas horizontales."
        elif nivel_desempenho == 2:
            return "##### ✍🏽 Puntaje: 36 a 50 \n - Además de lo descrito en el nivel 1, el estudiante que se ubica en este nivel es capaz de comparar y establecer relaciones entre los datos presentados, e identificar y extraer información local y global de manera directa. Lo anterior en contextos familiares o personales que involucran gráficas con escala explícita, cuadrícula o, por lo menos, líneas horizontales u otros formatos con poca información."
        elif nivel_desempenho == 3:
            return "##### ✍🏽 Puntaje: 51 a 70 \n - Además de lo descrito en los niveles 1 y 2, el estudiante que se ubica en este nivel selecciona información, señala errores y hace distintos tipos de transformaciones y manipulaciones aritméticas y algebraicas sencillas; esto para enfrentarse a problemas que involucran el uso de conceptos de proporcionalidad, factores de conversión, áreas y desarrollos planos, en contextos laborales u ocupacionales, matemáticos o científicos, y comunitarios o sociales."
        elif nivel_desempenho == 4:
            return "##### ✍🏽 Puntaje: 71 a 100 \n - Además de lo descrito en los niveles 1, 2 y 3, el estudiante que se ubica en este nivel resuelve problemas y justifica la veracidad o falsedad de afirmaciones que requieren el uso de conceptos de probabilidad, propiedades algebraicas, relaciones trigonométricas y características de funciones reales. Lo anterior, en contextos principalmente matemáticos o científicos abstractos."
        else:
            return "Selecciona un nivel de desempeño para ver la interpretación."

    elif area_conocimiento == 'ciencias_naturales':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "##### ✍🏽 Puntaje: 0 a 40 \n - El estudiante que se ubica en este nivel muy posiblemente alcanza a reconocer información explícita, presentada de manera ordenada en tablas o gráficas, con un lenguaje cotidiano y que implica la lectura de una sola variable independiente. Por lo tanto, estos estudiantes demuestran un insuficiente desarrollo de la competencia *Indagación* definida en el marco teórico de la prueba."
        elif nivel_desempenho == 2:
            return "##### ✍🏽 Puntaje: 41 a 55 \n - Además de lo descrito en el nivel 1, el estudiante que se ubica en este nivel reconoce información suministrada en tablas, gráficas y esquemas de una sola variable independiente, y la asocia con nociones de los conceptos básicos de las ciencias naturales (*tiempo, posición, velocidad, imantación y filtración*)."
        elif nivel_desempenho == 3:
            return "##### ✍🏽 Puntaje: 56 a 70 \n - Además de lo descrito en los niveles 1 y 2, el estudiante que se ubica en este nivel interrelaciona conceptos, leyes y teorías científicas con información presentada en diversos contextos, en los que intervienen dos o más variables, para hacer inferencias sobre una situación problema o un fenómeno natural."
        elif nivel_desempenho == 4:
            return "##### ✍🏽 Puntaje: 71 a 100 \n - Además de lo descrito en los niveles 1, 2 y 3, el estudiante que se ubica en este nivel usa conceptos, teorías o leyes en la solución de situaciones problema que involucran procedimientos, habilidades, conocimientos y un lenguaje propio de las ciencias naturales."
        else:
            return "Selecciona un nivel de desempeño para ver la interpretación."    


    elif area_conocimiento == 'ciencias_sociales':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "##### ✍🏽 Puntaje: 0 a 40 \n - El estudiante que se ubica en este nivel podría reconocer algunos derechos ciudadanos en situaciones sencillas. Adicionalmente, podría reconocer factores que generan un conflicto e identificar creencias que explican algunos comportamientos."
        elif nivel_desempenho == 2:
            return "##### ✍🏽 Puntaje: 41 a 55 \n - Además de lo descrito en el nivel anterior, el estudiante que se ubica en este nivel reconoce deberes del Estado colombiano y situaciones de protección o vulneración de derechos en el marco del Estado social de derecho; identifica relaciones entre conductas de las personas y sus cosmovisiones; y reconoce las dimensiones presentes en una situación, problema, decisión tomada o propuesta de solución. Además, contextualiza fuentes y procesos sociales."
        elif nivel_desempenho == 3:
            return "##### ✍🏽 Puntaje: 56 a 70 \n - Además de lo descrito en los niveles anteriores, el estudiante que se ubica en este nivel identifica prejuicios o intenciones contenidos en una afirmación y reconoce las dimensiones e intereses involucrados en un problema o alternativa de solución. Asimismo, identifica algunos conceptos básicos de las ciencias sociales y modelos conceptuales, y valora y contextualiza la información presentada en una fuente."
        elif nivel_desempenho == 4:
            return "##### ✍🏽 Puntaje: 71 a 100 \n - Además de lo descrito en los niveles anteriores, el estudiante que se ubica en este nivel conoce algunas disposiciones de la Constitución Política de Colombia que posibilitan la participación ciudadana y el control a los poderes públicos; analiza y compara enunciados, intereses y argumentos; y evalúa alternativas de solución a un problema. \n Este estudiante analiza situaciones a partir de conceptos básicos de las ciencias sociales o de contextos históricos y/o geográficos. A su vez, relaciona fuentes y políticas con modelos conceptuales, y valora los contenidos de una fuente."
        else:
            return "Selecciona un nivel de desempeño para ver la interpretación." 
        
    elif area_conocimiento == 'lectura_critica':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "##### ✍🏽 Puntaje: 0 a 35 \n - El estudiante que se ubica en este nivel probablemente identifica elementos literales en textos continuos y discontinuos sin establecer relaciones de significado."
        elif nivel_desempenho == 2:
            return "##### ✍🏽 Puntaje: 36 a 50 \n - Además de lo que logra hacer en el nivel 1, el estudiante que se ubica en este nivel comprende textos continuos y discontinuos de manera literal. Asimismo, reconoce información explícita y la relaciona con el contexto."
        elif nivel_desempenho == 3:
            return "##### ✍🏽 Puntaje: 51 a 65 \n - Además de lo descrito en los niveles 1 y 2, el estudiante que se ubica en este nivel interpreta información de textos al inferir contenidos implícitos y reconocer estructuras, estrategias discursivas y juicios valorativos."
        elif nivel_desempenho == 4:
            return "##### ✍🏽 Puntaje: 66 a 100 \n - Además de lo descrito en los niveles 1, 2 y 3, el estudiante que se ubica en este nivel reflexiona a partir de un texto sobre la visión de mundo del autor (costumbres, creencias, juicios, carácter ideológico-político y posturas éticas, entre otros). Asimismo, da cuenta de elementos paratextuales significativos presentes en el texto. Finalmente, valora y contrasta los elementos mencionados."
        else:
            return "Selecciona un nivel de desempeño para ver la interpretación." 


    elif area_conocimiento == 'ingles':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "##### ✍🏽 Puntaje: 0 a 47 \n - El estudiante promedio clasificado en este nivel probablemente puede comprender algunas oraciones simples como preguntas o instrucciones, y utilizar vocabulario básico para nombrar personas u objetos que le son familiares."
        elif nivel_desempenho == 2:
            return "##### ✍🏽 Puntaje: 48 a 57 \n - Además de lo descrito en el nivel A-, el estudiante que se clasifica en este nivel puede comprender situaciones comunicativas sencillas y concretas en las que se haga uso de expresiones básicas para proporcionar información personal, y fórmulas de saludo, despedida, indicaciones de lugares, etc."
        elif nivel_desempenho == 3:
            return "##### ✍🏽 Puntaje: 58 a 67 \n - Además de lo descrito en los niveles A- y A1, el estudiante que se clasifica en este nivel puede comprender información específica en textos sencillos cotidianos, además de comunicarse mediante el uso de expresiones de uso diario para realizar y responder invitaciones, sugerencias, disculpas, etc."
        elif nivel_desempenho == 4:
            return "##### ✍🏽 Puntaje: 68 a 78 \n - Además de lo descrito en los niveles A-, A1y A2, el estudiante que se clasifica en este nivel posee un amplio vocabulario para comprender textos de temáticas específicas que son de su interés personal. De igual manera, el estudiante en este nivel logra comunicarse con cierta seguridad en asuntos que le son poco habituales, y puede expresar y comprender diversas opiniones y actitudes."
        elif nivel_desempenho == 5:
            return "##### ✍🏽 Puntaje: 79 a 100 \n - El estudiante promedio clasificado en este nivel supera las preguntas de mayor complejidad de la prueba. Este estudiante, además de lo descrito en los niveles A-, A1, A2 y B1, probablemente puede comprender textos y discursos sobre temáticas abstractas, gracias a que posee un amplio vocabulario de lectura. Asimismo, el estudiante probablemente puede comunicarse en diferentes contextos generales o académicos de manera espontánea."
        else:
            return "Selecciona un nivel de desempeño para ver la interpretación."
        
    elif area_conocimiento == 'global':

        # Definir el texto de interpretación según el nivel de desempeño
        if nivel_desempenho == 1:
            return "##### ✍🏽 Puntaje: 0 a 100"
        elif nivel_desempenho == 2:
            return "##### ✍🏽 Puntaje: 101 a 200"
        elif nivel_desempenho == 3:
            return "##### ✍🏽 Puntaje: 201 a 300"
        elif nivel_desempenho == 4:
            return "##### ✍🏽 Puntaje: 301 a 400"
        elif nivel_desempenho == 5:
            return "##### ✍🏽 Puntaje: 401 a 500"
        
    else:
        return "Selecciona un área del conocimiento para ver la interpretación de los niveles de desempeño."
    

# Función para crear el contenido del offcanvas que muestra la información de las subregiones de antioquia. Retorna html.Div
# Valle de Aburrá, Oriente, Occidente, Suroeste, Nordeste, Norte, Urabá, Bajo Cauca, Magdalena Medio
def create_offcanvas_content(subregion):
    """
    Crea el contenido del offcanvas que muestra la información de las subregiones de Antioquia.

    Returns:
        html.Div: Contenido del offcanvas.
    """
    if subregion == "Valle de Aburrá":
        return html.Div([

            html.Img(src='https://www.comfenalcoantioquia.com.co/wcm/connect/cf661baa-28ff-46cb-aa97-02435c3e69cc/desktop/region-valle-de-aburra-comfenalco-web.jpg?MOD=AJPERES&CACHEID=ROOTWORKSPACE-cf661baa-28ff-46cb-aa97-02435c3e69cc-desktop-mVBg.Pe', className='img-fluid'),
            html.H5(subregion, style={'padding-top': '10px'}),
            html.P("Medellín, Barbosa, Girardota, Bello, Copacabana, Envigado, Itagüí, La Estrella, Sabaneta, Caldas.", style={'color': 'grey', 'font-style': 'italic', 'font-size': '13px'}),

            dbc.Alert(
                [
                    html.Ul([
                        html.Li([html.I(className="fa fa-ranking-star"),"\t Es la ", html.Strong("subregión con mejores condiciones de vida del departamento "), "de Antioquia."], style={'margin-bottom': '6px'}),
                        html.Li([html.I(className="fa fa-piggy-bank"),"\t Esta subregión ", html.Strong("aporta el 67,6% del PIB del departamento, "), "siendo la de mayor valor agregado."], style={'margin-bottom': '6px'}),
                        html.Li([html.I(className="fa fa-wifi"),"\t Penetración de internet fijo: 24,3%"]),
                    ], style={'padding-left': '20px', 'padding-top': '10px'}),

                ],
                color="light",
                style={'padding-top': '10px', 'padding-bottom': '10px', 'font-size': '13px'}
            ),

            dcc.Markdown('''
                Con una población de 4.05 millones, el Valle de Aburrá, ubicado en el centro de Antioquia y compuesto por diez municipios, destaca como la subregión más poblada del departamento. Aunque abarca solo el 1.83% del área, concentra más del 58.5% de los habitantes, resultando en una alta densidad poblacional de 3717 personas por kilómetro cuadrado. Este epicentro regional es crucial para servicios como salud, educación y empleo. A pesar de su buen bienestar social, persistentes desafíos, como el empleo informal y el rezago educativo, generan brechas en la calidad de vida de una parte significativa de la población.

                Económicamente, la subregión se especializa en servicios financieros, inmobiliarios, empresariales y manufactura, contribuyendo significativamente al PIB departamental. No obstante, enfrenta una tasa de desempleo del 11.6%, con notables disparidades de género. La densidad empresarial es notable, liderando con 37.8 empresas por mil habitantes en 2019, mayormente compuestas por microempresas en los sectores de comercio, manufactura y servicios. Estas dinámicas económicas y sociales, junto con apuestas estratégicas en clústeres, configuran el panorama que incide directamente en la calidad educativa de la región, marcando áreas de oportunidad y desafíos cruciales.

                ###### Bibliografía
                - [Subregiones de Antioquia: Diversidad y oportunidad. (s. f.). En _Coalición para la Alimentación y Uso del Suelo._](https://folucolombia.org/wp-content/uploads/2022/03/Subregiones-FOLU-Antioquia.pdf)
                - [Universidad de Antioquia. (2022i). Perfil de Desarrollo Subregional Subregión Valle de Aburrá de Antioquia. En _Consejo Territorial de Planeación de Antioquia._](https://ctpantioquia.co/wp-content/uploads/2023/11/Perfil-de-desarrollo-Valle-de-Aburra_compressed.pdf)
                
                         
            ''', dangerously_allow_html=True, style={'font-size': '13px'}),

        ])
    
    elif subregion == "Oriente":
        return html.Div([
            html.Img(src='https://www.comfenalcoantioquia.com.co/wcm/connect/ff409dc2-c645-4d88-ac8e-199846be5d38/desktop/region-oriente-comfenalco-web.jpg?MOD=AJPERES&CACHEID=ROOTWORKSPACE-ff409dc2-c645-4d88-ac8e-199846be5d38-desktop-mVBgDsD', className='img-fluid', height='100px'),
            html.H5(subregion, style={'padding-top': '10px'}),
            html.P("Abejorral, Argelia, Nariño, Sonsón, Alejandría, Concepción, El Peñol, Guatapé, Granada, San Carlos, San Rafael, Cocorná, San Luis, San Francisco, El Carmen de Viboral, El Retiro, El Santuario, Guarne, La Ceja, La Unión, Marinilla, Rionegro, San Vicente.", style={'color': 'grey', 'font-style': 'italic', 'font-size': '14px'}),
            
            dbc.Alert([
                html.Ul([

                    html.Li([html.I(className="fa fa-city"),"\t Posee una amplia ", html.Strong("red de entidades estatales de apoyo, fundaciones y empresas consolidadas, "), "que tienen gran cobertura territorial."], style={'margin-bottom': '6px'}),
                    html.Li([html.I(className="fa fa-bolt"),"\t Importante subregión en la ", html.Strong(" generación de hidroenergía "), "a nivel nacional."], style={'margin-bottom': '6px'}),
                    html.Li([html.I(className="fa fa-wheat-awn"),"\t", html.Strong("Despensa de alimentos regional de hortalizas, verduras y legumbres. "), "Aporta cerca del 60% de la producción de hortalizas del departamento."], style={'margin-bottom': '6px'}),
                    html.Li([html.I(className="fa fa-industry"),"\t Las ramas de actividad económica incluyen manufactura (25,3%), agricultura (11,5%), comercio (11,5%) y actividades inmobiliarias (9,6%). ", html.Strong("Alta inequidad entre municipios.")]),

                ], style={'padding-left': '20px', 'padding-top': '10px'}),

                ],
                color="light",
                style={'padding-top': '10px', 'padding-bottom': '10px', 'font-size': '13px'}
            ),


            dcc.Markdown('''
                La subregión Oriente de Antioquia, corazón del departamento, destaca por su sólido bienestar social y calidad de vida, situándose como la segunda con menores necesidades básicas insatisfechas y reduciendo significativamente la pobreza. A pesar de desafíos persistentes como el empleo informal, la baja escolaridad y desigualdades en ingresos, la subregión se posiciona como un centro económico clave. Además de su liderazgo en la oferta de energía gracias a su potencial hidroeléctrico, Oriente cuenta con la mayor extensión de vías pavimentadas en Antioquia, aunque se observan rezagos en algunos municipios distantes.

                Con una estructura económica diversificada que incluye sectores agropecuarios, industriales, comerciales y servicios financieros, Oriente se consolida como la segunda subregión con mayor densidad empresarial, impulsada principalmente por microempresas. La riqueza hídrica e industrial se distribuye en sus 23 municipios, agrupados en distintas zonas geográficas. A pesar de sus logros, los desafíos persisten, especialmente en términos de equidad de desarrollo entre sus municipios y la necesidad de mejorar la infraestructura vial para garantizar un crecimiento más equitativo en toda la subregión.
                         
                ###### Bibliografía
                - [Subregiones de Antioquia: Diversidad y oportunidad. (s. f.). En _Coalición para la Alimentación y Uso del Suelo._](https://folucolombia.org/wp-content/uploads/2022/03/Subregiones-FOLU-Antioquia.pdf)
                - [Universidad de Antioquia. (2022f). Perfil de Desarrollo Subregional Subregión Oriente de Antioquia. En _Consejo Territorial de Planeación de Antioquia._](https://ctpantioquia.co/wp-content/uploads/2023/11/Perfil-de-desarrollo-Oriente_compressed.pdf)
                         
            ''', dangerously_allow_html=True),
        ])
    
    elif subregion == "Occidente":
        return html.Div([
            html.Img(src='https://www.comfenalcoantioquia.com.co/wcm/connect/03740ddc-853b-4f52-892e-30bf78374e8a/unnamed.jpeg?MOD=AJPERES&CACHEID=ROOTWORKSPACE-03740ddc-853b-4f52-892e-30bf78374e8a-oJu3wSA', className='img-fluid', height='100px'),
            html.H5(subregion, style={'padding-top': '10px'}),
            html.P("Abriaquí, Anzá, Armenia, Buriticá, Caicedo, Cañasgordas, Dabeiba, Ebéjico, Frontino, Giraldo, Heliconia, Liborina, Olaya, Peque, Sabanalarga, San Jerónimo, Santa Fe de Antioquia, Sopetrán, Uramita", style={'color': 'grey', 'font-style': 'italic', 'font-size': '14px'}),
            
            dbc.Alert([
                html.Ul([

                    html.Li([html.I(className="fa fa-child"),"\t Mayor ", html.Strong("tasa de desnutrición infantil "), "en Antioquia: 9,6 por cada 100 mil niños y niñas menores de 5 años."], style={'margin-bottom': '6px'}),
                    html.Li([html.I(className="fa fa-hand-fist"),"\t Se presentan conflictos en el uso del suelo debido a la ", html.Strong("expansión de la frontera agropecuaria "), "para usos no aptos."], style={'margin-bottom': '6px'}),
                    html.Li([html.I(className="fa fa-caret-down"),"\tSe presentan procesos severos de degradación del suelo por las condiciones climáticas y prácticas de manejo y uso inadecuadas."])

                ], style={'padding-left': '20px', 'padding-top': '10px'}),

                ],
                color="light",
                style={'padding-top': '10px', 'padding-bottom': '10px', 'font-size': '13px'}
            ),

            dcc.Markdown('''

                    La subregión Occidente de Antioquia, con su población mayormente concentrada en el área rural, enfrenta desafíos significativos en términos de vulnerabilidad social, evidenciados por altos índices de empleo informal y bajo logro educativo. La falta de accesos adecuados a vivienda, servicios públicos, salud y educación, junto con preocupantes niveles de deserción escolar del 2.8%, limita el desarrollo de la población, especialmente en las zonas rurales. Los índices de pobreza se concentran en la zona rural, destacando problemas como el empleo informal (75.6%), bajo logro educativo (70.5%) y deficiencias en el saneamiento básico (41.2%), contribuyendo a una calidad de vida baja, marcada por carencias en recreación, condiciones habitacionales y educación.

                    Económicamente especializada en ganadería doble propósito, cultivo de frutas, fríjol, lulo, café, maíz, plátano, zapote y mango, la subregión Occidente enfrenta desafíos considerables en términos de vulnerabilidad social. Aunque presenta un alto potencial turístico gracias a su valioso patrimonio histórico, arquitectónico, arqueológico, cultural y paisajístico, así como a importantes desarrollos mineros, particularmente en el Distrito Minero de Frontino, la región sigue siendo la de menor aporte al PIB en Antioquia. Estos desafíos económicos y sociales, resaltan la urgente necesidad de intervenciones para mejorar la infraestructura básica, los servicios públicos y las condiciones de vida en el Occidente.

                    ###### Bibliografía
                    - [Subregiones de Antioquia: Diversidad y oportunidad. (s. f.). En _Coalición para la Alimentación y Uso del Suelo._](https://folucolombia.org/wp-content/uploads/2022/03/Subregiones-FOLU-Antioquia.pdf)
                    - [Universidad de Antioquia. (2022e). Perfil de Desarrollo Subregional Subregión Occidente de Antioquia. En _Consejo Territorial de Planeación de Antioquia._](https://ctpantioquia.co/wp-content/uploads/2023/11/Perfil-de-desarrollo-Occidente_compressed.pdf)        

            ''', dangerously_allow_html=True),
        ])
    
    elif subregion == "Suroeste":
        return html.Div([
            html.Img(src='https://www.comfenalcoantioquia.com.co/wcm/connect/c4394f43-33b8-4fa2-8e35-88fefdca3a22/desktop/region-suroeste-comfenalco-web.jpg?MOD=AJPERES&CACHEID=ROOTWORKSPACE-c4394f43-33b8-4fa2-8e35-88fefdca3a22-desktop-mVBguS1', className='img-fluid', height='100px'),
            html.H5(subregion, style={'padding-top': '10px'}),
            html.P("Amagá, Angelópolis, Fredonia, Venecia, Titiribí, Andes, Betania, Ciudad Bolívar, Hispania, Jardín, Betulia, Concordia, Salgar, Urrao, Caramanta, Jericó, La Pintada, Montebello, Pueblorrico, Santa Bárbara, Támesis, Tarso, Valparaíso.", style={'color': 'grey', 'font-style': 'italic', 'font-size': '14px'}),
            
            dbc.Alert([
                html.Ul([

                    html.Li([html.I(className="fa fa-mug-saucer"),"\t Reconocida como ", html.Strong("región cafetera "), "y en los últimos años ha ganado importancia la producción de frutas."], style={'margin-bottom': '6px'}),
                    html.Li([html.I(className="fa fa-handshake-simple"),"\t Presencia de ", html.Strong("esquemas asociativos territoriales subregionales "), "(Provincias administrativas y de planificación): Provincias de Cartama, Penderisco y Sinifaná, San Juan."], style={'margin-bottom': '6px'}),
                    html.Li([html.I(className="fa fa-wheat-awn"),"\t Dentro de las actividades económicas se incluyen la agricultura (29,9%), el  comercio (12,0%), las actividades inmobiliarias (9,4%) y la manufactura (8,5%)."])

                ], style={'padding-left': '20px', 'padding-top': '10px'}),

                ],
                color="light",
                style={'padding-top': '10px', 'padding-bottom': '10px', 'font-size': '13px'}
            ),


            dcc.Markdown('''
                         
                La subregión del Suroeste de Antioquia destaca por sus condiciones sociales estables en comparación con otras subregiones del Departamento, proporcionando un mayor bienestar a sus habitantes. Aunque presenta niveles moderados de pobreza, esta se concentra principalmente en la población rural, donde el empleo informal (72.9%) y el bajo logro educativo (73.2%) son factores determinantes. A pesar de estas privaciones, la calidad de vida en el Suroeste se posiciona favorablemente frente a otras subregiones, destacando aspectos como vulnerabilidad, desescolarización, capital del hogar y medio ambiente como los de menor superación.

                Económicamente, la subregión se fundamenta en la caficultura como la actividad más relevante y generadora de empleo, acompañada por la presencia de ganadería, minería de carbón y oro, producción frutícola, y un potencial turístico respaldado por sus excepcionales paisajes. En 2019, el Suroeste se posiciona como la séptima subregión con mayor densidad empresarial, mayoritariamente compuesta por microempresas. Estas empresas se concentran en municipios clave como Andes, Ciudad Bolívar, Amagá, Urrao, Santa Bárbara y Jericó, dedicándose principalmente a actividades comerciales, hoteles y restaurantes. Con miras al desarrollo económico, se plantean estrategias como la construcción de zonas industriales, el fortalecimiento del sector agroindustrial y la activación turística, especialmente centrada en la biodiversidad de la región y sus tradiciones cafeteras, el turismo de aventura y la preservación de sus pueblos patrimonio.
                         
                ###### Bibliografía
                - [Subregiones de Antioquia: Diversidad y oportunidad. (s. f.). En _Coalición para la Alimentación y Uso del Suelo._](https://folucolombia.org/wp-content/uploads/2022/03/Subregiones-FOLU-Antioquia.pdf)
                - [Universidad de Antioquia. (2022g). Perfil de Desarrollo Subregional Subregión Suroeste de Antioquia. En _Consejo Territorial de Planeación de Antioquia._](https://ctpantioquia.co/wp-content/uploads/2023/11/Perfil-de-desarrollo-Suroeste_compressed.pdf)
            ''', dangerously_allow_html=True),
        ])
    
    elif subregion == "Nordeste":
        return html.Div([

            html.Img(src='https://www.comfenalcoantioquia.com.co/wcm/connect/b31afc6c-0f74-4337-b281-3f4015828059/desktop/region-nordeste-comfenalco-web.jpg?MOD=AJPERES&CACHEID=ROOTWORKSPACE-b31afc6c-0f74-4337-b281-3f4015828059-desktop-mVBhaac', className='img-fluid', height='100px'),
            html.H5(subregion, style={'padding-top': '10px'}),
            html.P("Cisneros, San Roque, Santo Domingo, Amalfi, Vegachí, Yalí, Yolombó, Segovia, Remedios, Anorí.", style={'color': 'grey', 'font-style': 'italic', 'font-size': '14px'}),
            
            dbc.Alert([
                html.Ul([
                    html.Li([html.I(className="fa fa-house-crack"), html.Strong("\t Población "), "en situación de ", html.Strong("pobreza "), "(39,3%) y miseria (16,3%) por necesidades básicas insatisfechas."], style={'margin-bottom': '6px'}),
                    html.Li([html.I(className="fa fa-gem"),"\t La minería es una actividad que históricamente ha dado la identidad económica a la zona. En esta coexiste la ", html.Strong("minería artesanal con la industrial.")], style={'margin-bottom': '6px'}),
                    html.Li([html.I(className="fa fa-cubes-stacked"),"\t Los trapiches para la producción de panela y la producción aurífera requieren una intervención en modelos más eficientes y sostenibles de producción."])

                ], style={'padding-left': '20px', 'padding-top': '10px'}),

                ],
                color="light",
                style={'padding-top': '10px', 'padding-bottom': '10px', 'font-size': '13px'}
            ),

            dcc.Markdown('''
                         
                La subregión del Nordeste de Antioquia enfrenta altas necesidades básicas insatisfechas, especialmente en las zonas rurales, donde se concentran las privaciones asociadas al empleo informal (72.1%), bajo logro educativo (69.2%), y limitado acceso a eliminación de excretas (51.1%). A pesar de experimentar una pobreza multidimensional relativamente mejor que otras subregiones, persisten precariedades, principalmente en áreas rurales. La calidad de vida se ve afectada por bajos niveles de recreación (6.3%), presencia de materiales inadecuados (12.5%), y limitado capital en los hogares (17.0%).

                Económicamente, el Nordeste se destaca como la segunda subregión productora de oro en el departamento, siendo la minería la principal fuente de sustento. Sin embargo, estas actividades han generado conflictos socioambientales, desplazamientos forzados y afectaciones a la población. A pesar de este rol económico, la subregión presenta bajos ingresos y ejecución de egresos, reflejando limitadas posibilidades para generación de ingresos propios e inversiones. Las transferencias nacionales constituyen la principal fuente de ingresos, siendo destinadas principalmente a inversión.

                En cuanto a servicios públicos, el Nordeste experimenta bajas coberturas, siendo la subregión con la menor cobertura en acueducto, energía eléctrica y gas, lo que se refleja en altas necesidades básicas insatisfechas y condiciones sociales desfavorables. Además, la educación inicial, media y superior presenta bajas coberturas, limitando el acceso a empleos formales y afectando el desarrollo de la subregión. La vivienda muestra altos déficits cualitativos, especialmente en áreas rurales, y la subregión enfrenta elevadas tasas de homicidios, lesiones personales, violencia intrafamiliar y accidentes de transporte, asociados a la presencia de grupos armados y dinámicas vinculadas a cultivos ilícitos.

                ###### Bibliografía
                - [Subregiones de Antioquia: Diversidad y oportunidad. (s. f.). En _Coalición para la Alimentación y Uso del Suelo._](https://folucolombia.org/wp-content/uploads/2022/03/Subregiones-FOLU-Antioquia.pdf)
                - [Universidad de Antioquia. (2022c). Perfil de Desarrollo Subregional Subregión Nordeste de Antioquia. En _Consejo Territorial de Planeación de Antioquia._](https://ctpantioquia.co/wp-content/uploads/2023/11/Perfil-de-desarrollo-Nordeste_compressed-1.pdf)
            ''', dangerously_allow_html=True),
        ])
    
    elif subregion == "Norte":
        return html.Div([
            html.Img(src='https://www.comfenalcoantioquia.com.co/wcm/connect/4ff8ecad-62e8-4b32-aa2e-0acaedfb9cfd/desktop/region-norte-comfenalco-web.jpg?MOD=AJPERES&CACHEID=ROOTWORKSPACE-4ff8ecad-62e8-4b32-aa2e-0acaedfb9cfd-desktop-m.s.5Sj', className='img-fluid', height='100px'),
            html.H5(subregion, style={'padding-top': '10px'}),
            html.P("Carolina del Príncipe, Gómez Plata, Guadalupe, Angostura, Briceño, Campamento, Valdivia, Yarumal, Belmira, Don Matías, Entrerríos, San José de la Montaña, San Pedro de los Milagros, Santa Rosa de Osos, Ituango, San Andrés de Cuerquia, Toledo.", style={'color': 'grey', 'font-style': 'italic', 'font-size': '14px'}),
            
            dbc.Alert([
                html.Ul([
                    html.Li([html.I(className="fa fa-cow"), "\t En el subsector pecuario ", html.Strong("las principales actividades incluyen la producción de leche, "), "que la hace una de las regiones más productoras del país."], style={'margin-bottom': '6px'}),
                    html.Li([html.I(className="fa fa-wheat-awn"),"\t Los sectores con mayor participación en la economía son la agricultura, la manufactura, especialmente de maquilas, el comercio y la construcción"])

                ], style={'padding-left': '20px', 'padding-top': '10px'}),

                ],
                color="light",
                style={'padding-top': '10px', 'padding-bottom': '10px', 'font-size': '13px'}
            ),

            dcc.Markdown('''
                         
                La Subregión Norte de Antioquia se encuentra en una posición intermedia en cuanto a Necesidades Básicas Insatisfechas (NBI) en comparación con otras áreas del departamento, con algunas precariedades persistiendo, especialmente en las zonas rurales. La incidencia de la pobreza se concentra principalmente en el empleo informal y el bajo logro educativo, siendo más notable en las áreas rurales. A pesar de tener una calidad de vida de nivel medio en comparación con otras subregiones, se enfrenta a desafíos relacionados con aspectos como recreación, escolaridad y materiales inadecuados.

                Desde el punto de vista económico, la Subregión Norte destaca por sus actividades rurales, como la economía campesina y la producción lechera. Además, el turismo, impulsado por la riqueza natural y desarrollos hidroeléctricos, la posiciona como un centro de intercambio cultural y comercial. Aunque la producción agrícola es significativa, se vislumbran desafíos ante cambios potenciales en los flujos comerciales debido a nuevas conexiones con la Costa Atlántica, lo que sugiere la necesidad de una reorientación del ordenamiento territorial.

                En términos de servicios públicos, la Subregión Norte presenta ventajas en comparación con otras áreas, con altas coberturas en electricidad y gas. Aunque estas coberturas son estables, persisten precariedades en áreas rurales. La educación en transición y media tiene coberturas medias, mientras que la superior muestra una alta cobertura, beneficiando el desarrollo del talento humano. No obstante, enfrenta desafíos en seguridad, con tasas elevadas de homicidios vinculadas a grupos armados y al proyecto Hidroeléctrico de Ituango.
                         
                ###### Bibliografía
                - [Subregiones de Antioquia: Diversidad y oportunidad. (s. f.). En _Coalición para la Alimentación y Uso del Suelo._](https://folucolombia.org/wp-content/uploads/2022/03/Subregiones-FOLU-Antioquia.pdf)
                - [Universidad de Antioquia. (2022d). Perfil de Desarrollo Subregional Subregión Norte de Antioquia. En _Consejo Territorial de Planeación de Antioquia._](https://ctpantioquia.co/wp-content/uploads/2023/11/Perfil-de-desarrollo-Norte_compressed-2.pdf)
                                        
            ''', dangerously_allow_html=True),
        ])
    
    elif subregion == "Urabá":
        return html.Div([
            html.Img(src='https://www.comfenalcoantioquia.com.co/wcm/connect/ac52bcf6-bc4c-4f20-a091-038e27d388c6/desktop/region-uraba-comfenalco-web.jpg?MOD=AJPERES&CACHEID=ROOTWORKSPACE-ac52bcf6-bc4c-4f20-a091-038e27d388c6-desktop-mWfgMIF', className='img-fluid', height='100px'),
            html.H5(subregion, style={'padding-top': '10px'}),
            html.P("Necoclí, San Juan de Urabá, Arboletes, San Pedro de Urabá, Apartadó, Carepa, Chigorodó, Mutatá, Turbo, Murindó, Vigía del Fuerte.", style={'color': 'grey', 'font-style': 'italic', 'font-size': '14px'}),
            
            dbc.Alert([
                html.Ul([
                    html.Li([html.I(className="fa fa-wheat-awn-circle-exclamation"), "\t 86% de los hogares con ", html.Strong("inseguridad alimentaria.")], style={'margin-bottom': '6px'}),
                    html.Li([html.I(className="fa fa-house-crack"),"\t Indicador es de pobreza y miseria por encima de los valores departamentales."]),

                ], style={'padding-left': '20px', 'padding-top': '10px'}),

                ],
                color="light",
                style={'padding-top': '10px', 'padding-bottom': '10px', 'font-size': '13px'}
            ),


            dcc.Markdown('''
                         
                La subregión de Urabá, ubicada estratégicamente en el golfo del mismo nombre, destaca por su conexión con el Mar Caribe y su papel en la internacionalización del Departamento de Antioquia. Aunque el Distrito de Turbo ha potenciado estas conexiones, la subregión enfrenta desafíos considerables. Urabá se encuentra entre las subregiones con mayor vulnerabilidad social en Antioquia, especialmente en las zonas rurales, donde bajos ingresos afectan el acceso adecuado a vivienda, servicios públicos, salud y educación. La alta presencia de empleo informal complica aún más las condiciones sociales.

                A nivel económico, Urabá ha experimentado una transformación significativa, pasando de actividades forestales a una especialización en agricultura, destacando el cultivo de banano, plátano y ganadería. A pesar de ser una destacada productora, la subregión se enfrenta a desafíos, incluida una alta tasa de desempleo y un predominio significativo de empleo informal. Aunque Urabá es la tercera subregión con mayores ingresos en Antioquia, también presenta desigualdades en género en el empleo.

                El acceso a servicios públicos en Urabá refleja una cobertura media en comparación con otras subregiones de Antioquia, destacando deficiencias en acueducto y reciclaje. La atención en salud también presenta desafíos, con una alta tasa de mortalidad infantil por desnutrición. La vivienda, tanto en áreas urbanas como rurales, muestra déficits cuantitativos y cualitativos significativos, concentrados principalmente en zonas rurales. Además, el conflicto armado ha exacerbado las condiciones precarias, limitando el acceso a la propiedad, restringiendo la restitución de tierras y afectando el desarrollo socioeconómico de las comunidades locales. La presencia de grupos armados ha creado un ambiente de inseguridad que impacta la movilidad y el bienestar general de la población en la subregión.

                ###### Bibliografía
                - [Subregiones de Antioquia: Diversidad y oportunidad. (s. f.). En _Coalición para la Alimentación y Uso del Suelo._](https://folucolombia.org/wp-content/uploads/2022/03/Subregiones-FOLU-Antioquia.pdf)
                - [Universidad de Antioquia. (2022h). Perfil de Desarrollo Subregional Subregión Urabá de Antioquia. En _Consejo Territorial de Planeación de Antioquia._](https://ctpantioquia.co/wp-content/uploads/2023/11/Perfil-de-desarrollo-Uraba_compressed.pdf)
            ''', dangerously_allow_html=True),
        ])
    
    elif subregion == "Bajo Cauca":
        return html.Div([
            html.Img(src='https://www.comfenalcoantioquia.com.co/wcm/connect/ca0d70ef-acb6-4a20-91e1-b0b2bf720cb4/h-region-bajocauca-comfenalco%5B1%5D.jpg?MOD=AJPERES&CACHEID=ROOTWORKSPACE-ca0d70ef-acb6-4a20-91e1-b0b2bf720cb4-m.6MKCe', className='img-fluid', height='100px'),
            html.H5(subregion, style={'padding-top': '10px'}),
            html.P("Cáceres, Caucasia, El Bagre, Nechí, Tarazá y Zaragoza", style={'color': 'grey', 'font-style': 'italic', 'font-size': '14px'}),
            
            dbc.Alert([
                html.Ul([
                    html.Li([html.I(className="fa fa-person-rifle"), html.Strong("\t Conflictos entre actores económicos, pobladores y grupos armados "), "por la disputa del territorio y los recursos naturales."], style={'margin-bottom': '6px'}),
                    html.Li([html.I(className="fa fa-wheat-awn-circle-exclamation"), "\t 87,6% de los hogares presentan ", html.Strong("inseguridad alimentaria.")], style={'margin-bottom': '6px'}),
                    html.Li([html.I(className="fa house-crack"),"\t Subregión con ", html.Strong("alto índice de pobreza "), "multidimensional: 28,5%."]),

                ], style={'padding-left': '20px', 'padding-top': '10px'}),

                ],
                color="light",
                style={'padding-top': '10px', 'padding-bottom': '10px', 'font-size': '13px'}
            ),

            dcc.Markdown('''
                         
                Bajo Cauca, en Antioquia, enfrenta desafíos significativos en términos sociales, especialmente en sus áreas rurales, siendo la subregión con mayores necesidades básicas insatisfechas en el departamento. Con altos niveles de pobreza, la población se ve afectada por empleo informal, bajo logro educativo y carencias en saneamiento. La calidad de vida es la más baja del departamento, marcada por vulnerabilidad, desescolarización y limitado acceso a servicios públicos.

                Económicamente, Bajo Cauca destaca por su producción de oro y plata, así como actividades agrícolas como el cultivo de arroz, yuca, plátano y ñame. A pesar de estas actividades, la subregión enfrenta altas tasas de desempleo e informalidad laboral, lo que contribuye a la baja calidad de vida.

                En educación, Bajo Cauca enfrenta desafíos con baja cobertura en educación media, alta deserción escolar y escasez de instituciones. La situación de vivienda es crítica, con importantes déficits tanto cuantitativos como cualitativos, tanto en áreas urbanas como rurales. Además, la subregión experimenta graves problemas de seguridad, incluyendo altas tasas de homicidios, inseguridad percibida y complejidades derivadas del conflicto armado, como cultivos ilícitos y afectaciones sociales. Estos desafíos colectivos han generado condiciones precarias y limitado el desarrollo integral de Bajo Cauca.
                         
                ###### Bibliografía
                - [Subregiones de Antioquia: Diversidad y oportunidad. (s. f.). En _Coalición para la Alimentación y Uso del Suelo._](https://folucolombia.org/wp-content/uploads/2022/03/Subregiones-FOLU-Antioquia.pdf)
                - [Universidad de Antioquia. (2022a). Perfil de Desarrollo Subregional Subregión Bajo Cauca de Antioquia. En _Consejo Territorial de Planeación de Antioquia._](https://ctpantioquia.co/wp-content/uploads/2023/11/Perfil-de-desarrollo-Bajo-Cauca_compressed.pdf)
            ''', dangerously_allow_html=True),
        ])
    
    elif subregion == "Magdalena Medio":
        return html.Div([
            html.Img(src='https://www.comfenalcoantioquia.com.co/wcm/connect/044a39c7-c0d3-4518-810e-82e4235fcf1b/desktop/region-magdalenamedio-comfenalco-web.jpg?MOD=AJPERES&CACHEID=ROOTWORKSPACE-044a39c7-c0d3-4518-810e-82e4235fcf1b-desktop-mVBhgUJ', className='img-fluid', height='100px'),
            html.H5(subregion, style={'padding-top': '10px'}),
            html.P("Puerto Berrío, Puerto Nare, Puerto Triunfo, Yondó, Caracolí, Maceo.", style={'color': 'grey', 'font-style': 'italic', 'font-size': '14px'}),
            
            dbc.Alert([
                html.Ul([
                    html.Li([html.I(className="fa fa-thumbs-down"), "\t El", html.Strong("\t sector agropecuario "), "tiene muy bajo ", html.Strong("aporte al PIB "), "subregional: 2,76%."], style={'margin-bottom': '6px'}),

                ], style={'padding-left': '20px', 'padding-top': '10px'}),

                ],
                color="light",
                style={'padding-top': '10px', 'padding-bottom': '10px', 'font-size': '13px'}
            ),


            dcc.Markdown('''
                La subregión del Magdalena Medio ocupa una posición geoestratégica central en Colombia, sirviendo como un puente crucial y nodo de conexión para diversos territorios a través de redes terrestres, fluviales y aéreas. Con acceso cercano a importantes centros de mercado en Medellín, Bogotá y Bucaramanga, facilita la conexión de Antioquia con el centro del país y establece vínculos con Santander, Boyacá, Cundinamarca y Caldas.

                A pesar de su posición favorable, el Magdalena Medio enfrenta desafíos en términos de empleo informal y bajo logro educativo, especialmente en sus zonas rurales. Aunque la subregión presenta condiciones sociales estables en comparación con otras áreas de Antioquia, sufre altos niveles de pobreza, siendo más pronunciada en la población rural. La calidad de vida, evaluada a través de índices como vulnerabilidad, desescolarización, medio ambiente y acceso a servicios públicos, muestra que, a pesar de ciertos avances, persisten áreas críticas que necesitan mejoras. Además, la economía del Magdalena Medio está influenciada por la minería, la agricultura y la ganadería, aunque se enfrenta a desafíos en sectores como el turismo y la vivienda. El bienestar de la población se ve afectado por la falta de cobertura en servicios públicos, altas tasas de desempleo y limitado acceso a servicios de salud. Aunque se han logrado ciertos niveles de estabilidad gracias a los procesos de paz, aún persisten desafíos en la convivencia ciudadana, relacionados con la presencia de cultivos ilícitos y la dinámica del acceso a la propiedad rural.
                         
                ###### Bibliografía
                - [Subregiones de Antioquia: Diversidad y oportunidad. (s. f.). En _Coalición para la Alimentación y Uso del Suelo._](https://folucolombia.org/wp-content/uploads/2022/03/Subregiones-FOLU-Antioquia.pdf)
                - [Universidad de Antioquia. (2022b). Perfil de Desarrollo Subregional Subregión Magdalena Medio de Antioquia. En _Consejo Territorial de Planeación de Antioquia._](https://ctpantioquia.co/wp-content/uploads/2023/11/Perfil-de-desarrollo-Magdalena-Medio_compressed.pdf)
            ''', dangerously_allow_html=True),
        ])

            
