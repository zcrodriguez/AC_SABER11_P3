import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pywaffle import Waffle # Usé py -m pip install pywaffle para instalarlo
import base64
from io import BytesIO
import json

templates = ["cerulean"]
load_figure_template(templates)

# Registrar la página
dash.register_page(__name__)

# ======================================================================================================================
#                                                     CARGA DE DATOS
# ======================================================================================================================

# Carga el archivo CSV en un DataFrame
df = pd.read_csv('Caro\'s_files/data_viz.csv', dtype={'Course': 'category'})  # Asegúrate de que la ruta sea correcta

# ======================================================================================================================
#                                               DICCIONARIOS AUXILIARES
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

# Extraer los diccionarios de cursos y escuelas
course_name = all_params.get('visualizations_dict', {}).get('course_name', {})
school_name = all_params.get('visualizations_dict', {}).get('school_name', {})


# ======================================================================================================================
#                                                     TARJETAS
# ======================================================================================================================

# Estilo del icono de las tarjetas
card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

# Valores para tarjetas
# TODO ajustar código para calcularlos a partir de base en RDS en AWS
card_val_a = len(df)
card_val_b = f"{round(len(df[df['Target'] == 'Graduate']) / card_val_a * 100, 2)}%"
card_val_c = round(len(df[df['Target'] == 'Dropout']) / card_val_a * 100, 2)
delta_card_c = f"{round(card_val_c - 29.0, 2)}%"
card_val_c = f"{card_val_c}%"

# Lista de datos para las tarjetas
cards_data = [
    {
        "icon_class": "fa fa-users",
        "bg_color": "bg-info",
        "value": card_val_a,
        "footer_text": "Students in dataset"
    },
    {
        "icon_class": "fa fa-user-graduate",
        "bg_color": "bg-success",
        "value": card_val_b,
        "footer_text": "Success rate"
    },
    {
        "icon_class": "fa fa-user-minus",
        "bg_color": "bg-secondary",
        "value": card_val_c,
        "footer_text": "Dropout rate | "
    },
]

# Bucle para generar las tarjetas de la primera fila
cards = []
for card_data in cards_data:
    card = dbc.Col(dbc.CardGroup([
        dbc.Card(html.Div(className=card_data["icon_class"], style=card_icon), className=card_data["bg_color"], style={"maxWidth": 75}),
        dbc.Card([
            dbc.CardBody([
                html.H4(card_data["value"], className="card-text",),
            ]),
            dbc.CardFooter([
                html.H6(card_data["footer_text"], style={"display": "inline"}),
                html.I(className="fa fa-caret-up text-secondary") if card_data["footer_text"].startswith("Dropout rate") else '',
                html.Span(delta_card_c if card_data["footer_text"].startswith("Dropout rate") else "", className="text-secondary"),
                html.Span(" vs Portugal" if card_data["footer_text"].startswith("Dropout rate") else "", className="text-secondary"),
            ]),
        ]),
    ], className="mt-4 shadow"))
    cards.append(card)

# ======================================================================================================================
#                                       GRÁFICOS PARA TAB 1: DROPOUT RATE BY COURSE
# ======================================================================================================================

# Calcula el porcentaje de graduate, enrolled y dropout por carrera
total_counts = df.groupby('Course')['Target'].count()
graduate_percentage = df[df['Target'] == 'Graduate'].groupby('Course')['Target'].count() / total_counts * 100
enrolled_percentage = df[df['Target'] == 'Enrolled'].groupby('Course')['Target'].count() / total_counts * 100
dropout_percentage = df[df['Target'] == 'Dropout'].groupby('Course')['Target'].count() / total_counts * 100

# Crea un nuevo DataFrame con los porcentajes
df_g1 = pd.DataFrame({'Course': total_counts.index,
                              'Students': total_counts.values,
                              'Graduate': graduate_percentage,
                              'Enrolled': enrolled_percentage,
                              'Dropout': dropout_percentage})

df_g1.head()

# Reemplaza los códigos de las carreras con sus nombres
df_g1['Course'] = df_g1['Course'].map(course_name)

# Añade una columna con el nombre de la escuela a partir del indice de la carrera
df_g1['School'] = df_g1.index.map(school_name)

# Ordena el DataFrame por el porcentaje de dropout de mayor a menor
df_g1 = df_g1.sort_values(by='Dropout', ascending=False)

def create_figure(df_g1, n_registros, highlighted_courses, top=True):

    topmargin = 15
    altura = 350
    
    # Si no hay carreras destacadas, se muestran todas
    if len(highlighted_courses) == 0:
        topmargin = 30
        altura = 650
        colors = ['#78C2AD' if course in df_g1['Course'].tail(4).values else 'lightgray' for course in df_g1['Course'].head(n_registros).values]
    
    elif top:
        df_g1 = df_g1.head(n_registros)
        colors = ['#E87479' if course in highlighted_courses
                  else '#F7BBBD' if course in df_g1['Course'].head(5).values
                  else '#E5E5E5' for course in df_g1['Course'].head(n_registros).values]
    else:
        df_g1 = df_g1.tail(n_registros)
        colors = ['#78C2AD' if course in highlighted_courses
                  else 'lightgrey' for course in df_g1['Course'].tail(n_registros).values]
        topmargin = 35

    fig = px.bar(df_g1, x='Dropout', y='Course',
                 labels={'variable': 'Course', 'value': 'Dropout rate'},
                 barmode="relative",
                 hover_data={'Course': False, 'Dropout': False,
                             'School': True,
                             'Dropout rate': [f'{percentage:.1f}%' for percentage in df_g1['Dropout'].values],
                             'Students': True})
    
    fig.update_traces(marker=dict(color=colors))
    fig.update_traces(texttemplate='%{value:.1f}%', textposition='inside')
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(categoryorder='total ascending')
    fig.update_layout(xaxis_title='', yaxis_title='Courses', margin=dict(t=topmargin, b=5), height=altura)

    if not top or len(highlighted_courses) == 0:
        fig.add_vline(x=29, line_width=2, line_dash="dash", line_color="#549f93", opacity=0.7, annotation_text="Portugal (29%)", annotation_position="top")
        fig.add_vrect(x0=0, x1=29, line_width=0, fillcolor="#549f93", opacity=0.2, layer='below')
        fig.add_vrect(x0=29, x1=66.7, line_width=0, fillcolor="#F3969A", opacity=0.1, layer='below')

    return fig

fig0 = create_figure(df_g1, 17, highlighted_courses=[])

n_registros = 10

highlighted_courses = ['Biofuel Production Technologies', 'Informatics Engineering', 'Management (evening attendance)']
fig1 = create_figure(df_g1, n_registros, highlighted_courses)

highlighted_courses = ['Biofuel Production Technologies']
fig2 = create_figure(df_g1, n_registros, highlighted_courses)



# ======================================================================================================================
#                                       GRÁFICOS PARA TAB 2: WAFFLE CHARTS
# ======================================================================================================================

# ====================================================    DEBTOR    ====================================================
# Calcula el número de estudiantes por cada diez que se gradúan graduate, enrolled y dropout por 'Debtor'
total_counts = df.groupby('Debtor')['Target'].count()
graduate_counts = df[df['Target'] == 'Graduate'].groupby('Debtor')['Target'].count()
enrolled_counts = df[df['Target'] == 'Enrolled'].groupby('Debtor')['Target'].count()
dropout_counts = df[df['Target'] == 'Dropout'].groupby('Debtor')['Target'].count()

# Calcula el porcentaje de estudiantes graduados, enrolados y en situación de abandono por 'Debtor'
graduate_percentage = (graduate_counts / total_counts * 10).round()
enrolled_percentage = (enrolled_counts / total_counts * 10).round()
dropout_percentage = (dropout_counts / total_counts * 10).round()

# Crea un DataFrame df_g2_debtor
df_g2_debtor = pd.DataFrame({
    'Debtor': total_counts.index.map({0: 'No', 1: 'Yes'}),
    'Students': total_counts.values,
    'Graduate': graduate_percentage.values,
    'Enrolled': enrolled_percentage.values,
    'Dropout': dropout_percentage.values
})

# Convierte los valores numéricos en los diccionarios a enteros (opcional)
df_g2_debtor_1 = df_g2_debtor[df_g2_debtor['Debtor'] == 'Yes'][['Graduate', 'Enrolled', 'Dropout']].sum().to_dict()
df_g2_debtor_0 = df_g2_debtor[df_g2_debtor['Debtor'] == 'No'][['Graduate', 'Enrolled', 'Dropout']].sum().to_dict()
df_g2_debtor_1 = {key: int(value) for key, value in df_g2_debtor_1.items()}
df_g2_debtor_0 = {key: int(value) for key, value in df_g2_debtor_0.items()}

from matplotlib.lines import Line2D
from matplotlib.patches import Patch
def create_waffle_chart(values):
    '''
    Función para crear un gráfico de waffle

    :param values: diccionario con los valores a representar
    :return: gráfico de waffle
    '''
    fig = plt.figure(
        FigureClass=Waffle, 
        rows=2,
        values=values,
        colors=["#91DEBF", "lightgray", "#FFA78E"], 
        font_size=30,
        characters=['⬤', '■', '▲'],
        figsize=(4, 2.3),
    )
    custom_legend_elements = [Line2D([0], [0], marker='o', color='white', markerfacecolor='#91DEBF', markeredgewidth=0, label='Graduated', markersize=10),
                            Line2D([0], [0], marker='^', color='white', markerfacecolor='#FFA78E', markeredgewidth=0, label='Dropout', markersize=10)]

    # Agregar manualmente los objetos Line2D personalizados a la leyenda
    fig.get_axes()[0].legend(handles=custom_legend_elements, loc='lower center', bbox_to_anchor=(0.5, -0.5), ncol=3, framealpha=0, fontsize=10)

    ax = fig.get_axes()[0]
    new_position = [0.1, 0, 0.8, 0.5]  # [left, bottom, width, height]
    ax.set_position(new_position)

    # Set position es una función de Axes que recibe como parámetro una lista con las coordenadas del rectángulo. La primera

    fig.set_canvas(plt.gcf().canvas)
    # legend = fig.get_axes()[0].legend(["dummy_label"])
    # legend.remove()
    return fig  # Devolver la figura creada

# Ejemplo de uso de la función
fig3 = create_waffle_chart(df_g2_debtor_1)
fig4 = create_waffle_chart(df_g2_debtor_0)

# ==================================================    SCHOLARSHIP    =================================================
# Calcula el número de estudiantes por cada diez que se gradúan graduate, enrolled y dropout por 'Scholarship holder'
total_counts = df.groupby('Scholarship holder')['Target'].count()
graduate_counts = df[df['Target'] == 'Graduate'].groupby('Scholarship holder')['Target'].count()
enrolled_counts = df[df['Target'] == 'Enrolled'].groupby('Scholarship holder')['Target'].count()
dropout_counts = df[df['Target'] == 'Dropout'].groupby('Scholarship holder')['Target'].count()

# Calcula el porcentaje de estudiantes graduados, enrolados y en situación de abandono por 'Scholarship holder'
graduate_percentage = (graduate_counts / total_counts * 10).round()
enrolled_percentage = (enrolled_counts / total_counts * 10).round()
dropout_percentage = (dropout_counts / total_counts * 10).round()

# Crea un DataFrame df_g2_scholarship
df_g2_scholarship = pd.DataFrame({
    'Scholarship holder': total_counts.index.map({0: 'No', 1: 'Yes'}),
    'Students': total_counts.values,
    'Graduate': graduate_percentage.values,
    'Enrolled': enrolled_percentage.values,
    'Dropout': dropout_percentage.values
})

# Convierte los valores numéricos en los diccionarios a enteros (opcional)
df_g2_scholarship_1 = df_g2_scholarship[df_g2_scholarship['Scholarship holder'] == 'Yes'][['Graduate', 'Enrolled', 'Dropout']].sum().to_dict()
df_g2_scholarship_0 = df_g2_scholarship[df_g2_scholarship['Scholarship holder'] == 'No'][['Graduate', 'Enrolled', 'Dropout']].sum().to_dict()
df_g2_scholarship_1 = {key: int(value) for key, value in df_g2_scholarship_1.items()}
df_g2_scholarship_0 = {key: int(value) for key, value in df_g2_scholarship_0.items()}

fig5 = create_waffle_chart(df_g2_scholarship_1)
fig6 = create_waffle_chart(df_g2_scholarship_0)



# ======================================================================================================================
#                                           TAB 1: DROPOUT RATE BY COURSE
# ======================================================================================================================
tab1_content = dbc.Card(

    dbc.CardBody([
        dbc.Row([
            
            # Gráfico a la izquierda
            dbc.Col([
                dbc.Card([

                    # Título del gráfico
                    dbc.CardHeader([
                        html.Div(id='title_cardhead_1', className='card-title'),
                    ]),
                    
                    # Gráfico
                    dcc.Graph(id='graph1', style={"maxHeight": "370px", "overflow-y": "scroll"}, config={'displayModeBar': False}),

                ], className="mt-4 shadow"),
            ], width=8),

            # Comentarios a la derecha
            dbc.Col([
                html.Br(),
                
                # Grupo de 3 botones a partir de los cuales se mostrará un output
                html.Div(
                    [
                        dbc.RadioItems(
                            id="radios",
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            persistence=True,
                            options=[
                                {"label": "Overview", "value": 0},
                                {"label": "Insight 1", "value": 1},
                                {"label": "Insight 2", "value": 2}
                            ],
                            value=0,
                        ),
                    ],
                    className="radio-group",
                ),
                
                html.Hr(),
               
                # Output que depende de los botones
                html.Div(id="output-radio-group"),

            ], width=4),
            
        ], style={'padding-left': '20px', 'padding-right': '20px', 'padding-bottom': '20px'}),
    ])
)



# ======================================================================================================================
#                                           TAB 2: DROPOUT RATE BY COURSE
# ======================================================================================================================
tab2_content = dbc.Card([
    
    dbc.CardHeader([
        html.Div([
                html.H6('Select a variable:', style={'margin-right': '10px', 'padding-left': '20px'}),  # Agrega estilo para el espaciado entre el texto y los botones
                dbc.RadioItems(
                    id="radios-tab2",
                    className="btn-group",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    persistence=True,
                    options=[
                        {"label": "Debtor", "value": 0},
                        {"label": "Scholarship holder", "value": 1},
                    ],
                    value=0,
                ),
            ], className="radio-group d-flex align-items-center")
    ]),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
      
                # Gráficos
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.Div(id='title_cardhead_2A', className='card-title'),
                            ]),
                            dbc.CardBody([
                                html.Img(id='graph2A', src='', style={'width':'100%','margin': '0 auto', 'display': 'block'}),
                            ]),
                        ], className="mt-4 shadow"),
                    ], width=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader([
                                html.Div(id='title_cardhead_2B', className='card-title'),
                            ]),
                            dbc.CardBody([
                                html.Img(id='graph2B', src='', style={'width':'100%', 'margin': '0 auto', 'display': 'block'}),
                            ]),
                        ], className="mt-4 shadow"),
                    ], width=6),
                ], style={'padding-left': '10px', 'padding-bottom': '20px'}),
            ], width=8),

            # Comentarios a la derecha
            dbc.Col([
                html.Br(),
                # Comentarios
                html.Div(id='md-tab2', style={'padding-left': '20px', 'padding-right': '20px'}),
            ], width=4),
            
        ], style={'padding-left': '20px', 'padding-right': '10px', 'padding-bottom': '20px'}),
    ]),
    
])

# ======================================================================================================================
#                                                    TABS' LAYOUT
# ======================================================================================================================
tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="Dropout rate by Course"),
        dbc.Tab(tab2_content, label="Socioeconomic variables vs academic performance"),
    ], persistence=True, style={'padding-left': '20px', 'padding-right': '20px', 'padding-bottom': '10px', 'padding-top': '30px'}
)

# ======================================================================================================================
#                                               CONTENIDO DE LA PÁGINA
# ======================================================================================================================
layout = html.Div([

    # Título
    dbc.Row([
        html.H3([html.I(className="fa fa-building-columns"),'\t Educational Outcomes Dashboard']),
    ], style={'padding-left': '20px', 'padding-right': '20px', 'padding-top': '10px'}),
    
    # Primera fila: Tarjetas generadas por el bucle
    dbc.Row(cards, style={'padding-left': '20px', 'padding-right': '20px'}),

    # Segunda fila: Gráficos
    tabs,

])


# ======================================================================================================================
#                                               CALLBACKS
# ======================================================================================================================

# Callback Tab 1: DROPOUT RATE BY COURSE
@dash.callback([Output("output-radio-group", "children"),
                Output('graph1', 'figure'),
                Output('title_cardhead_1', 'children')],
               [Input("radios", "value")])
def display_value(value):

    op0 = html.H4([html.I(className="fa fa-users"), '\t Courses by Dropout Rate']),
    op1 = html.H4([html.I(className="fa fa-user-minus"), '\t Top 10 Courses by Dropout Rate']),

    if value == 0:
        
        comentarios = dcc.Markdown('''
        ##### Overview
        - **<span style='color:#78C2AD' children=\"4 of 17 programs\" />** have maintained **dropout rates below the national average**.
        ''', dangerously_allow_html=True)
        return comentarios, fig0, op0
    
    elif value == 1:
        comentarios = html.Div([
            dcc.Markdown('''
            ##### Pay special attention to the ESTG
            - **<span style='color:#E87479' children=\"3 of the top 5 programs\" />** with the **highest dropout rates** are from the **Escola Superior de Tecnologia e Gestão (ESTG)**. 
            - This suggests that there may be specific challenges within ESTG contributing to higher dropout rates.
            ''', dangerously_allow_html=True),
        ])
        return comentarios, fig1, op1
    
    elif value == 2:
        comentarios = dcc.Markdown('''
        ##### Biofuel Production Technologies: An Alarmingly High Dropout Rate
        - **<span style='color:#E87479' children=\"Biofuel Production Technologies\" />** stands out with the **highest dropout rate at 67.7%**, surpassing the national average by a significant 38.7%.                         
        - The program's small enrollment of **only 12 students could impact its reliability** given the high dropout rate.
        ''', dangerously_allow_html=True)
        return comentarios, fig2, op1
    else:
        return 'Tiririri', fig0, op0


@dash.callback([Output(component_id='graph2A', component_property='src'),
                Output(component_id='graph2B', component_property='src'),
                Output(component_id='md-tab2', component_property='children'),
                Output(component_id='title_cardhead_2A', component_property='children'),
                Output(component_id='title_cardhead_2B', component_property='children')],
                [Input("radios-tab2", "value")])
def display_value(value):
    
    if value == 0:
        buf = BytesIO()
        fig3.savefig(buf, format="png", dpi=300)
        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        buf = BytesIO()
        fig4.savefig(buf, format="png", dpi=300)
        data2 = base64.b64encode(buf.getbuffer()).decode("ascii")

        comment = dcc.Markdown(
            '''
            #### Impact of **Debt** on Student Outcomes
            - Students who took loans are **less likely** to **<span style='color:#78C2AD' children="graduate (⬤)" />** compared to those who didn't.
            - Students with loans are **more likely** to **<span style='color:#FFA78E' children="drop out (▲)" />** compared to those without loans.
            '''
            , dangerously_allow_html=True)
        
        title_2A_content = html.H5([html.I(className="fa fa-circle-check"), '\t Debtor: Yes'])
        title_2B_content = html.H5([html.I(className="fa fa-circle-xmark"), '\t Debtor: No'])

        return f"data:image/png;base64,{data}", f"data:image/png;base64,{data2}", comment, title_2A_content, title_2B_content
    
    else:
        buf = BytesIO()
        fig5.savefig(buf, format="png", dpi=300)
        data = base64.b64encode(buf.getbuffer()).decode("ascii")

        buf = BytesIO()
        fig6.savefig(buf, format="png", dpi=300)
        data2 = base64.b64encode(buf.getbuffer()).decode("ascii")

        comment = dcc.Markdown(
            '''
            #### Impact of **Scholarships** on Student Outcomes
            - Students who received scholarships are **more likely** to **<span style='color:#78C2AD' children="graduate (⬤)" />** compared to those without.
            - Students with scholarships are **less likely** to **<span style='color:#FFA78E' children="drop out (▲)" />** compared to those without scholarships.
            '''
            , dangerously_allow_html=True)
        
        title_2A_content = html.H5([html.I(className="fa fa-circle-check"), '\t Scholarship holder: Yes'])
        title_2B_content = html.H5([html.I(className="fa fa fa-circle-xmark"), '\t Scholarship holder: No'])
        
        return f"data:image/png;base64,{data}", f"data:image/png;base64,{data2}", comment, title_2A_content, title_2B_content