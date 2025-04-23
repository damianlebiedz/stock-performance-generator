import plotly.express as px
from dash import Dash, html, dcc, dash_table
import dash_bootstrap_components as dbc

def generate_summary_report(summary):
    try:
        fig = px.line(
            summary,
            x='Date',
            y='Total change',
            title='Total change Over Time',
            labels={'Total change': 'Całkowita zmiana', 'Date': 'Data'}
        )

        app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

        app.layout = dbc.Container([
            html.H1("Raport dla wybranej spółki", className='text-center my-4'),

            html.Div(
                dcc.Graph(
                    id='graph',
                    figure=fig,
                    config={'displayModeBar': True},
                    style={'width': '90%', 'margin': 'auto'}
                ),
                style={'textAlign': 'center'}
            ),

            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            dash_table.DataTable(
                                id='table',
                                columns=[{"name": col, "id": col} for col in summary.columns],
                                data=summary.to_dict('records'),
                                filter_action='native',
                                page_size=15,
                                style_table={
                                    'overflowX': 'auto',
                                    'maxHeight': '400px'
                                },
                                style_header={
                                    'backgroundColor': 'rgb(230, 230, 230)',
                                    'fontWeight': 'bold'
                                }
                            )
                        ],
                        title="📊 Pokaż/ukryj dane źródłowe"
                    )
                ],
                style={
                    'width': '90%',
                    'margin': 'auto',
                    'marginTop': '30px'
                }
            )
        ], fluid=True)

        return app

    except Exception as e:
        print(e)