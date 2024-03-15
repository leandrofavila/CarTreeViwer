import plotly.graph_objects as go
from dash import dcc, html, Dash
from dash.dependencies import Input, Output
from conecta_db import DB

app = Dash(__name__)


def load_data():
    db = DB()
    return db.mach_load()


app.layout = html.Div([
    html.Label("Carga Maquina", style={'fontSize': 32, 'textAlign': 'center'}),
    html.Hr(),
    #interval=60000 = 1 minuto
    dcc.Interval(id='interval-component', interval=60000, n_intervals=0),
    dcc.Graph(id='graph')])


@app.callback(Output('graph', 'figure'), [Input('interval-component', 'n_intervals')])
def update_graph(n_intervals):
    df_load = load_data()
    fig = go.Figure(data=[
        go.Bar(
            name='Ordens',
            y=df_load['MAQUINA'],
            x=df_load['OP_PENDENTES'],
            text=df_load['PECAS_PENDENTES'],
            orientation='h',
            hovertemplate='<b>Maquina</b>: %{y}<br><b>OP Pendentes</b>: %{x}<br>Pecas Pendentes<b></b>: %{text}<extra></extra>'
        )
    ])
    fig.update_layout(
        yaxis={'categoryorder': 'total descending'},
        width=1360,
        height=800
    )
    fig.update_traces(
        textfont_size=12,
        textangle=0,
        textposition="outside"
    )
    return fig


if __name__ == '__main__':
    app.run_server(host='10.40.3.48', port=8014)
