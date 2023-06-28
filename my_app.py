from dash import Dash, html, dcc, ctx, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import object_build as ob
import db_functions as db
from dash.exceptions import PreventUpdate

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], )
server = app.server

"""
Identify Apple Module
- Button to launch the Apple identifier.
"""

section_intro = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H1("Find bestøvere til æbletræ", className="card-title"),
                html.P(
                    [
                        "Hvis du har et æbletræ i haven, skal det bestøves for at der kommer æbler. Det er ikke altid "
                        "lige til at finde ud af hvilke sorter af æbletræer som kan bestøve andre sorter, men det kan du "
                        "heldigvis få hjælp til her. ",
                        html.Br(),
                        html.Br(),
                        "Information er samlet fra forskellige kilder, spørg altid din lokale planteskole eller "
                        "havecenter til råds, for at være sikker.",
                    ],
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
                html.H1("Søg efter æbletræ", className="card-title"),
                dcc.Dropdown(id="input_Search",
                             placeholder="Søg...",
                             value="string",
                             clearable=True,
                             maxHeight=300,
                             searchable=True,
                             ),
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

section_credits = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Kontakt & Henvisninger", className="card-title"),
                html.P(
                    [
                        "Har du kommentarer eller rettelser, kontakt venligst ",
                        dcc.Link("kontakt@bestøvere.dk", title='email', href='mailto:kontakt@bestøvere.dk',
                                 target='_blank')
                    ]),
                html.P(
                    [
                        "Information og billeder på siden er hentet fra forskellige kilder. Information om æbler og "
                        "træer kommer hovedsagelidt fra  ",
                        html.A("Pometets æblenøgle",
                               href="http://aeblenoeglen.science.ku.dk/",
                               target="_blank"),
                        " som er et fantastisk redskab selv at gå på opdagelse i ved spørgsmål om æbletræer og æbler."
                    ]),
                html.Div(id="gen_credits")
            ],
            className="card-text")
    ],
),
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
        dbc.Row(
            [
                dbc.Col(section_credits, md=layout_md, sm=layout_sm),
            ],
            className="mb-3", justify="center"),
        dcc.Input(
            id="dummy_input",
            style={"display": "None"},
        )
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


"""
Credits
"""


@app.callback(
    Output("gen_credits", "children"),
    Input("dummy_input", "value")
)
def insert_credits(dummy_value):
    credit_list = ob.build_credits()
    return credit_list


if __name__ == '__main__':
    app.run_server(debug=True)
