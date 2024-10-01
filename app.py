import dash_mantine_components as dmc
from dash import Dash, html, Output, Input, State, callback, dcc
from dash_iconify import DashIconify
import dash


stylesheets = [
    "https://unpkg.com/@mantine/dates@7/styles.css",
    "https://unpkg.com/@mantine/code-highlight@7/styles.css",
    "https://unpkg.com/@mantine/charts@7/styles.css",
    "https://unpkg.com/@mantine/carousel@7/styles.css",
    "https://unpkg.com/@mantine/notifications@7/styles.css",
    "https://unpkg.com/@mantine/nprogress@7/styles.css",
]
app = Dash(__name__, use_pages=True, external_stylesheets=stylesheets, suppress_callback_exceptions=True)


def get_icon(icon):
    return DashIconify(icon=icon, height=16)


APPSHELL = dmc.AppShell(
    children=[
        dmc.AppShellHeader(
            children=[
                dmc.Container(
                    children=[
                        dmc.Group(
                            children=[
                                dmc.Anchor(dmc.Button("Applications", color='violet'), href="/applications"),
                                dmc.Anchor(dmc.Button("Prospects", color='violet'), href="/prospects"),
                                dmc.Anchor(dmc.Button("Insights", color='violet'), href="/insights"),
                            ],
                            flex=True,
                            align='center',
                            style={'height': '70px'}
                        )
                    ],
                    size='xl',
                )
            ],
            style={'background-color': '#7950f2'}),
    ],
    header={"height": 70},
    padding="xl",
)


app.layout = dmc.MantineProvider(
    children=[
        dcc.Location(id=f'app-location', refresh=True),
        dmc.Container(
            children=[
                dmc.Stack(
                    children=[
                        APPSHELL,
                        dash.page_container
                    ]
                )
            ],
            style={"marginTop": 20, "marginBottom": 20},
            size='xl',
        )
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=True)