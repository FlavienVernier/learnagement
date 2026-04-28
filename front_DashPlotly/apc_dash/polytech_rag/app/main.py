import dash
import dash_bootstrap_components as dbc

from app.ui.layout import create_layout
from app.ui.callbacks import register_callbacks


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

app.title = "Assistant Polytech RAG"
app.layout = create_layout()

register_callbacks(app)

server = app.server


if __name__ == "__main__":
    app.run(debug=True)