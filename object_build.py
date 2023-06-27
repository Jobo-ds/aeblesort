import db_functions as db
from dash import Dash, html, dcc, ctx, dash_table
import dash_bootstrap_components as dbc
import pandas as pd


def build_card(img, name, latin_name, description):
    return dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.CardImg(
                            src=("assets/img/" + img + ".jpg"),
                            className="img-fluid rounded-start",
                        ),
                        md=3, sm=3
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.H4(name, className="card-title"),
                                html.Small(latin_name),
                                html.P(
                                    description,
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
    if row["seller2"] is not None:
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
                                    # html.Small(row["latin_name"]),
                                    # html.P(
                                    #     row["description"],
                                    #     className="card-text",
                                    # ),
                                    dbc.Button(
                                        [
                                            html.I(className="bi bi-cart me-2"),
                                            row["seller1"],
                                        ], color="success", className="m-1", size="sm",
                                               href=row["seller1_link"], target="_blank"),
                                    dbc.Button(
                                        [
                                            html.I(className="bi bi-cart me-2"),
                                            row["seller2"],
                                        ], color="success", className="m-1", size="sm",
                                        href=row["seller2_link"], target="_blank"),
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
    elif row["seller1"] is not None:
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
                                    # html.Small(row["latin_name"]),
                                    # html.P(
                                    #     row["description"],
                                    #     className="card-text",
                                    # ),
                                    dbc.Button(
                                        [
                                            html.I(className="bi bi-cart me-2"),
                                            row["seller1"],
                                        ], color="success", className="m-1", size="sm",
                                               href=row["seller1_link"], target="_blank"),
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
    else:
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
                                    # html.Small(row["latin_name"]),
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


def target_apple_card(id):
    # Single apple_card
    apple = db.get_apple(id)
    for index, row in apple.iterrows():
        return (build_card(row["img"], row["name"], row["latin_name"], row["description"]))


def getTargetAppleName(id):
    apple = db.get_apple(id)
    return apple["name"][0]


def build_pollination_cards(target_apple_name, id):
    list_cards = [html.H4(f"Æblesorter der kan bestøve {target_apple_name}", className="w-100 card-title")]
    apples = db.get_apples(id)
    for index, row in apples.iterrows():
        print(index, row)
        list_cards.append((build_card_small(row)))
    return list_cards
