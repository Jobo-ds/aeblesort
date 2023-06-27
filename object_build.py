import db_functions as db
from dash import Dash, html, dcc, ctx, dash_table
import dash_bootstrap_components as dbc
import pandas as pd


def build_card(row):
    return dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src=("assets/img/" + row["img"] + ".jpg"),
                            className="img-fluid rounded-start",
                        ),
                        md=3, sm=3
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.H4(row["name"], className="card-title"),
                                html.Small(row["latin_name"]),
                                html.P(
                                    row["description"],
                                    className="card-text",
                                ),
                            ],
                        ),
                        md=9, sm=9
                    ),
                ],
                className="g-0 d-flex",
                align="start",
            )
        ],
        className="mb-3",
    )

def build_card_small(row):
    return dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src=("assets/img/" + row["img"] + ".jpg"),
                            className="img-fluid rounded-start",
                        ),
                        md=3, sm=3
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.H4(row["name"], className="card-title"),
                                #html.Small(row["latin_name"]),
                                # html.P(
                                #     row["description"],
                                #     className="card-text",
                                # ),
                            ],
                        ),
                        md=9, sm=9
                    ),
                ],
                className="g-0 d-flex",
                align="start",
            )
        ],
        className="w-48 m-1",
    )

def build_button_buy(row):
    return dbc.Button(row["seller"], color="primary", className="me-1"),


def target_apple_card(id):
    # Single apple_card
    apple = db.get_apple(id)
    for index, row in apple.iterrows():
        return (build_card(row))

def getTargetAppleName(id):
    apple = db.get_apple(id)
    return apple["name"][0]

def build_pollination_cards(target_apple_name, id):
    list_cards = [html.H4(f"Æblesorter der kan bestøve {target_apple_name}", className="w-100 card-title")]
    apples = db.get_apples(id)
    for index, row in apples.iterrows():
        list_cards.append((build_card_small(row)))
    return list_cards

