import datetime

import dash_mantine_components as dmc
import plotly.graph_objs as go
from dash import dcc
from dash_iconify import DashIconify


PREFIX = 'insights-overview'

# -----------------------------------------------------------------------------
# - FILTERS
# -----------------------------------------------------------------------------
FILTERS = dmc.Group(
    children=[
        dmc.Stack(
            children=[
                dmc.Group(
                    children=[
                        dmc.DatesProvider(
                            children=[
                                dmc.DatePicker(id=f'{PREFIX}-from', label='From', value=datetime.date.today(), style={'width': '200px'}),
                                dmc.DatePicker(id=f'{PREFIX}-to', label='To', value=datetime.date.today(), style={'width': '200px'}),
                            ],
                            settings={"locale": "fr", "firstDayOfWeek": 1, "weekendDays": [0, 6]},
                        ),
                        dmc.Button('Reset', id=f'{PREFIX}-reset', color='violet'),
                    ],
                    # justify='flex-end',
                    align='end',
                )
            ]
        ),
        dmc.Stack(
            children=[
                dmc.Select(
                    id=f'{PREFIX}-by',
                    label="By",
                    data=[
                        {'value': 'day', 'label': "Day"},
                        {'value': 'week', 'label': "Week"},
                        {'value': 'month', 'label': "Month"},
                        {'value': 'weekday', 'label': "Weekday"},
                        {'value': 'monthday', 'label': "Monthday"}
                    ],
                    value="day",
                )
            ]
        ),
    ],
    justify='space-between',
    style={'margin-top': '70px'}
)

# -----------------------------------------------------------------------------
# - CARD APPLICATIONS
# -----------------------------------------------------------------------------
CARD_APPLICATIONS = dmc.Card(
    children=[
        dmc.Text(DashIconify(icon="pepicons-pencil:cv", color='#7950f2', width=30)),
        dmc.Text(id=f'{PREFIX}-applications-total', fw=700, size='xl'),
        dmc.Text('Applications', fw=500, size='lg', c='dimmed')
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={'text-align': 'center'}
)

# -----------------------------------------------------------------------------
# - CARD STEPS
# -----------------------------------------------------------------------------
CARD_STEPS = dmc.Card(
    children=[
        dmc.Text(DashIconify(icon="streamline:arrow-roadmap", color='#228be6', width=30)),
        dmc.Text(id=f'{PREFIX}-steps-total', fw=700, size='xl'),
        dmc.Text('Steps', fw=500, size='lg', c='dimmed')
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={'text-align': 'center'}
)

# -----------------------------------------------------------------------------
# - CARD GRAPH
# -----------------------------------------------------------------------------
CARD_GRAPH = dmc.Card(
    children=[
        dcc.Graph(
            id=f'{PREFIX}-graph-applications-steps-decline',
            figure=go.Figure(),
            config={
                'displayModeBar': False
            }
        ),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={'text-align': 'center', 'height': '280px'}
)

# -----------------------------------------------------------------------------
# - CARD APPLICATIONS-ONLY
# -----------------------------------------------------------------------------
CARD_APPLICATIONS_ONLY = dmc.Card(
    children=[
        dmc.Group(
            children=[
                dmc.Text(DashIconify(icon="pepicons-pencil:cv", color='#7950f2', width=30)),
                dmc.Text(DashIconify(icon="formkit:arrowright", color='#868e96', width=30)),
                dmc.Text(DashIconify(icon="ph:empty", color='rgb(134, 142, 150)', width=30)),
            ],
            justify='center'
        ),
        dmc.Text(id=f'{PREFIX}-applications-only', fw=700, size='xl'),
        dmc.Text('applications-only', fw=500, size='lg', c='dimmed'),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={'text-align': 'center'}
)

# -----------------------------------------------------------------------------
# - CARD FIRST STEP
# -----------------------------------------------------------------------------
CARD_FIRST_STEP = dmc.Card(
    children=[
        dmc.Group(
            children=[
                dmc.Text(DashIconify(icon="pepicons-pencil:cv", color='#7950f2', width=30)),
                dmc.Text(DashIconify(icon="formkit:arrowright", color='#868e96', width=30)),
                dmc.Text(DashIconify(icon="fluent:chat-multiple-16-regular", color='#228be6', width=30)),
            ],
            justify='center'
        ),
        dmc.Text(id=f'{PREFIX}-days-first-step', fw=700, size='xl'),
        dmc.Text('until first step', fw=500, size='lg', c='dimmed'),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={'text-align': 'center'}
)

# -----------------------------------------------------------------------------
# - CARD BETWEEN STEPS
# -----------------------------------------------------------------------------
CARD_BETWEEN_STEPS = dmc.Card(
    children=[
        dmc.Group(
            children=[
                dmc.Text(DashIconify(icon="fluent:chat-multiple-16-regular", color='#228be6', width=30)),
                dmc.Text(DashIconify(icon="formkit:arrowright", color='#868e96', width=30)),
                dmc.Text(DashIconify(icon="fluent:chat-multiple-16-regular", color='#228be6', width=30)),
            ],
            justify='center'
        ),
        dmc.Text(id=f'{PREFIX}-days-between-steps', fw=700, size='xl'),
        dmc.Text('between steps', fw=500, size='lg', c='dimmed'),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={'text-align': 'center'}
)

# -----------------------------------------------------------------------------
# - CARD DECLINE
# -----------------------------------------------------------------------------
CARD_DECLINE = dmc.Card(
    children=[
        dmc.Group(
            children=[
                dmc.Text(DashIconify(icon="pepicons-pencil:cv", color='#7950f2', width=30)),
                dmc.Text(DashIconify(icon="formkit:arrowright", color='#868e96', width=30)),
                dmc.Text(DashIconify(icon="material-symbols-light:cancel-outline", color='#fa5252', width=30)),
            ],
            justify='center'
        ),
        dmc.Text(id=f'{PREFIX}-days-decline', fw=700, size='xl'),
        dmc.Text('until decline', fw=500, size='lg', c='dimmed'),
    ],
    withBorder=True,
    shadow="sm",
    radius="md",
    style={'text-align': 'center'}
)

# -----------------------------------------------------------------------------
# - MAIN LAYOUT
# -----------------------------------------------------------------------------
MAIN_LAYOUT = dmc.Stack(
    children=[
        dmc.Grid(
            children=[
                dmc.GridCol(
                    children=[
                        dmc.Stack(
                            children=[
                                CARD_APPLICATIONS,
                                CARD_STEPS,
                            ]
                        )
                    ],
                    span=3
                ),
                dmc.GridCol(children=[CARD_GRAPH], span=9),
            ],
            gutter='lg'
        ),
        dmc.Grid(
            children=[
                dmc.GridCol(children=[CARD_APPLICATIONS_ONLY], span=3),
                dmc.GridCol(children=[CARD_FIRST_STEP], span=3),
                dmc.GridCol(children=[CARD_BETWEEN_STEPS], span=3),
                dmc.GridCol(children=[CARD_DECLINE], span=3),
            ],
            gutter='lg'
        ),
    ]
)