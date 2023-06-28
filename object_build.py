import db_functions as db
from dash import Dash, html, dcc, ctx, dash_table
import dash_bootstrap_components as dbc
import pandas as pd


def build_card(img, name, description):
    return dbc.Card(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            html.Img(src="assets/img/" + img + ".jpg",
                                     className="card-img-apple rounded-circle"),
                            className="d-flex justify-content-center"
                        ),
                        align="center", md=3, sm=3
                    ),
                    dbc.Col(
                        dbc.CardBody(
                            [
                                html.H4(name, className="card-title"),
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
        className="mb-3 card-target",
    )


def build_card_small(row):
    if row["seller2"] is not None:
        return dbc.Card(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                html.Img(src="assets/img/" + row["img"] + ".jpg",
                                         className="card-img-apple rounded-circle"),
                                className="d-flex justify-content-center"
                            ),
                            align="center", md=3, sm=3
                        ),
                        dbc.Col(
                            dbc.CardBody(
                                [
                                    html.H4(row["name"], className="card-title"),
                                    html.P(
                                        row["description_short"],
                                        className="card-text",
                                    ),
                                ],
                            ),
                            md=9, sm=12
                        ),
                    ],
                    className="g-0 d-flex",
                    align="start",
                ),
                dbc.Row(
                    dbc.Col(
                        [
                            html.Div(
                                [
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
                                className="d-flex justify-content-center mt-1"
                            ),
                        ],
                        className="mx-auto", sm=12),
                    align="center", justify="center"),
            ],
            className="w-48 m-1 p-1",
        )
    elif row["seller1"] is not None:
        return dbc.Card(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                html.Img(src="assets/img/" + row["img"] + ".jpg",
                                         className="card-img-apple rounded-circle"),
                                className="d-flex justify-content-center"
                            ),
                            align="center", md=3, sm=3
                        ),
                        dbc.Col(
                            dbc.CardBody(
                                [
                                    html.H4(row["name"], className="card-title"),
                                    html.P(
                                        row["description_short"],
                                        className="card-text",
                                    ),
                                ],
                            ),
                            md=9, sm=12
                        ),
                    ],
                    className="g-0 d-flex",
                    align="start",
                ),
                dbc.Row(
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    dbc.Button(
                                        [
                                            html.I(className="bi bi-cart me-2"),
                                            row["seller1"],
                                        ], color="success", className="m-1", size="sm",
                                        href=row["seller1_link"], target="_blank"),
                                ],
                                className="d-flex justify-content-center mt-1"
                            ),
                        ],
                        className="mx-auto", sm=12),
                    align="center", justify="center"),
            ],
            className="w-48 m-1 p-1",
        )
    else:
        return dbc.Card(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                html.Img(src="assets/img/" + row["img"] + ".jpg",
                                         className="card-img-apple rounded-circle"),
                                className="d-flex justify-content-center"
                            ),
                            align="center", md=3, sm=3
                        ),
                        dbc.Col(
                            dbc.CardBody(
                                [
                                    html.H4(row["name"], className="card-title"),
                                    html.P(
                                        row["description_short"],
                                        className="card-text",
                                    ),
                                ],
                            ),
                            md=9, sm=12
                        ),
                    ],
                    className="g-0 d-flex",
                    align="start",
                ),
            ],
            className="w-48 m-1 p-1",
        )

def build_credit(row):
    return html.Small(
        [
            row["name"],
            ": ",
            html.A(row["source_name"],
                   href=row["source_link"],
                   target="_blank"),
            " (Licens: ",
            html.A(row["license_name"],
                   href=row["license_link"],
                   target="_blank"),
            ") ",
            row["comment"],
            html.Br()
        ])


def target_apple_card(id):
    # Single apple_card
    apple = db.get_apple(id)
    for index, row in apple.iterrows():
        return (build_card(row["img"], row["name"], row["description"]))


def getTargetAppleName(id):
    apple = db.get_apple(id)
    return apple["name"][0]


def build_pollination_cards(target_apple_name, id):
    headline = html.H4(f"Æblesorter, der kan bestøve {target_apple_name}"
                       , className="w-100 card-title")
    description = html.P("Bestøvningen af dit æbletræ sker når der kommer blomster på træet, og er afhænging af at "
                         "bierne og andre insekter kan flyve mellem træet og bestøvningstræet. Derfor anbefales der "
                         "ikke at være mere end 20-30 meter mellem træerne. Hos nogle planteskoler kan de anbefale "
                         "sammensætninger af flere slags æbletræer som kan bestøve hinanden."
                         , className="w-100 card-text")
    list_cards = [headline, description]
    apples = db.get_apples(id)
    for index, row in apples.iterrows():
        list_cards.append((build_card_small(row)))
    print(list_cards)
    return list_cards


def build_credits():
    headline = html.H4(f"Anerkendelser"
                       , className="w-100 card-title")
    description = html.P("Tak til følgende for brug af billeder:"
                         , className="w-100 card-text")
    list_credit = [headline, description]
    df_credits = db.get_credits()
    for index, row in df_credits.iterrows():
        list_credit.append((build_credit(row)))
    return list_credit
