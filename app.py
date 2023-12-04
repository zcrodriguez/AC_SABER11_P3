import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CERULEAN, '/assets/custom.css', dbc.icons.FONT_AWESOME], use_pages=True)
server = app.server

# ======================================================================================================================
#                                               LAYOUT PRINCIPAL
# ======================================================================================================================
app.layout = html.Div([

    # Barra de navegación
    dbc.Navbar(
        dbc.Container([

            # Logo y título
            html.A(
                dbc.Row([
                    dbc.Col(html.Img(src="./assets/croquis-ANT2.png", height="40px"), width="auto"),
                    dbc.Col(dbc.NavbarBrand("Saber 11° en Antioquia")),
                ], align="center"),
            ),

            # Links de la barra de navegación
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink([html.I(className="fa fa-house")," Inicio"], href="/", active="exact")),
                    dbc.NavItem(dbc.NavLink([html.I(className="fa fa-magnifying-glass-chart")," Visualizaciones"], href="/visualizations", active="exact",)),
                ],
                pills=True, 
            ),
        ]),
        color="primary", dark=True,
    ),

    # Contenido de la página
    dash.page_container
])

# ======================================================================================================================
#                                              EJECUCIÓN DE LA APLICACIÓN
# ======================================================================================================================
if __name__ == '__main__':
    app.run_server(host = "0.0.0.0", debug=True)