from dash import html, Input, Output
import dash_bootstrap_components as dbc
import app3_absenteisme_tools


app3_administratif_layout = html.Div([
    html.Div([
        html.Label("Absences :"),
        html.Div(id='absences')
    ], className="dropdown-container"),  # Conteneur avec une classe pour l'ajouter au style CSS
])


def register_callbacks(app):
    @app.callback(
        Output('absences', 'children'),
        Input('user_id', 'data')
    )
    def update_table_abs(user_id):
        df_abs = app3_absenteisme_tools.get_absence()
        table_absence = dbc.Table.from_dataframe(
            df_abs,
            # Key styling options:
            striped=True,
            bordered=True,
            hover=True,
        )
        return [table_absence]
