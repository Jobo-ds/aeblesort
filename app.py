from dash import Dash, html, dcc, ctx, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import object_build as ob
import db_functions as db
from dash.exceptions import PreventUpdate

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], )

"""
Identify Apple Module
- Button to launch the Apple identifier.
"""

section_intro = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Er du i tvivl om bestøvning af æbletræer?", className="card-title"),
                html.P(
                    "Hvis du har et æbletræ i haven, skal det bestøves for at der kommer æbler. Det er ikke altid "
                    "lige til at finde ud af hvilke sorter af æbletræer som kan bestøve andre sorter, men det kan du "
                    "heldigvis få hjælp til her. Spørg altid din lokale planteskole eller havecenter til råds, "
                    "hvis du har brug for hjælp.",
                    className="card-text",
                ),
            ]
        ),
    ],
)

"""
Search Apple Module + Target Apple
- Search Dropdown
- Information on the currently selected apple (name + image +desc)
"""
dropdown_dict = db.build_search()
section_search = dbc.Card(
    [
        dbc.CardBody(
            [
                dcc.Dropdown(id="input_Search", placeholder="Søg efter æble...", value="string", clearable=True),
                html.Div(id="section_info", className="my-2")
            ],
            ),
    ],
)

"""
Pollination Table Module
- Table of apples that can pollinate this sort.
- Clicking a another sort, will allow the user to search for that.
"""

section_pollination = dbc.Card(
    [
        dbc.CardBody(
            [
                html.Div()
            ],
            id="pollination_cards_placement", className="d-flex flex-wrap"),
    ],
    style={"display": "None"}, id="section_pollination"
)

"""
DASH Layout
"""

layout_md = 8
layout_sm = 12

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(section_intro, md=layout_md, sm=layout_sm),
            ],
            className="my-3", justify="center"),
        dbc.Row(
            [
                dbc.Col(section_search, md=layout_md, sm=layout_sm),
            ],
            className="mb-3", justify="center"),
        dbc.Row(
            [
                dbc.Col(section_pollination, md=layout_md, sm=layout_sm),
            ],
            className="mb-3", justify="center"),
    ],
)

"""
Search
"""


@app.callback(
    Output("input_Search", "options"),
    Input("input_Search", "search_value")
)
def update_options(search_value):
    if not search_value:
        return dropdown_dict
    # if len(search_value) < 5:
    #     raise PreventUpdate
    return [o for o in dropdown_dict if search_value in o["label"]]


"""
Target Apple
"""


@app.callback(
    Output("section_info", "children"),
    Input("input_Search", "value"), prevent_initial_call=True
)
def update_targetApple(search_value):
    if not search_value:
        return html.Div()
    # if len(search_value) < 5:
    #     raise PreventUpdate
    return ob.target_apple_card(search_value)


"""
Pollination Apples
"""


@app.callback(
    Output("pollination_cards_placement", "children"),
    Output("section_pollination", component_property="style"),
    Input("input_Search", "value"), prevent_initial_call=True
)
def update_poliapples(target_apple_id):
    if not target_apple_id:
        return html.Div(), {"display": "None"}
    target_apple_name = ob.getTargetAppleName(target_apple_id)
    pollination_cards = ob.build_pollination_cards(target_apple_name, target_apple_id)
    return pollination_cards, {"display": "block"}


if __name__ == '__main__':
    app.run_server(debug=True)
