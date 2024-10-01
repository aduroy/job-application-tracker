import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify


PREFIX = 'prospects-overview'


# -----------------------------------------------------------------------------
# - STORE LAST LOAD TIME
# -----------------------------------------------------------------------------
PROSPECTS_LOAD = dcc.Store(id=f'{PREFIX}-store-load-time')

# -----------------------------------------------------------------------------
# - BUTTON CREATE PROSPECT
# -----------------------------------------------------------------------------
ADD_NEW_PROSPECT = dmc.Group(
    children=[
        dmc.Button(
            'New prospect',
            id=f'{PREFIX}-prospect-new',
            color='violet',
            leftSection=DashIconify(icon="ic:round-plus"),
            size='md'
        )
    ],
    justify='flex-end',
    style={'margin-top': '70px'}
)

# -----------------------------------------------------------------------------
# - MODAL CREATE PROSPECT
# -----------------------------------------------------------------------------
PROSPECTS_MODAL_CREATE = dmc.Modal(
    children=[
        html.Div(
            children=[
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.TextInput(id=f'{PREFIX}-prospect-new-name', label='Name', required=True),
                            ],
                        ),
                        dmc.Stack(
                            children=[
                                dmc.TextInput(id=f'{PREFIX}-prospect-new-url', label='URL'),
                            ],
                        ),
                    ],
                    grow=True,
                    align='flex-start'
                ),
                dmc.Space(h=20),
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Textarea(
                                    id=f'{PREFIX}-prospect-new-notes',
                                    label="Notes",
                                    placeholder="",
                                    autosize=True,
                                    minRows=4,
                                    maxRows=4,
                                ),
                            ]
                        )
                    ],
                    grow=True
                ),
                dmc.Space(h=20),
                dmc.Group(
                    children=[
                        dmc.Button('Cancel', id=f'{PREFIX}-prospect-new-cancel', color='violet', variant="subtle"),
                        dmc.Button('Save', id=f'{PREFIX}-prospect-new-submit', color='violet'),
                    ],
                    justify="flex-end",
                ),
            ],
            style={'padding': '20px'}
        )
    ],
    title='Create New Prospect',
    id=f'{PREFIX}-modal-prospect-create',
    size='xl',
)

# -----------------------------------------------------------------------------
# - MODAL EDIT PROSPECT
# -----------------------------------------------------------------------------
PROSPECTS_MODAL_EDIT = dmc.Modal(
    children=[
        html.Div(
            children=[
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.TextInput(id=f'{PREFIX}-prospect-edit-name', label='Name', required=True),
                            ],
                        ),
                        dmc.Stack(
                            children=[
                                dmc.TextInput(id=f'{PREFIX}-prospect-edit-url', label='URL'),
                            ],
                        ),
                    ],
                    grow=True,
                    align='flex-start'
                ),
                dmc.Space(h=20),
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Textarea(
                                    id=f'{PREFIX}-prospect-edit-notes',
                                    label="Notes",
                                    placeholder="",
                                    autosize=True,
                                    minRows=4,
                                    maxRows=4,
                                ),
                            ]
                        )
                    ],
                    grow=True
                ),
                dmc.Space(h=20),
                dmc.Group(
                    children=[
                        dmc.Button('Cancel', id=f'{PREFIX}-prospect-edit-cancel', color='violet', variant="subtle"),
                        html.Div(id=f'{PREFIX}-prospect-edit-submit-div'),
                    ],
                    justify="flex-end",
                ),
            ],
            style={'padding': '20px'}
        )
    ],
    title='Edit Prospect',
    id=f'{PREFIX}-modal-prospect-edit',
    size='xl',
)

# -----------------------------------------------------------------------------
# - MODAL DELETE PROSPECT
# -----------------------------------------------------------------------------
PROSPECTS_MODAL_DELETE = dmc.Modal(
    children=[
        html.Div(
            children=[
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Text('Permanently delete:'),
                                dmc.Text(id=f'{PREFIX}-prospect-delete-name', style={'text-align': 'center'}, fw=700),
                            ],
                        ),
                    ],
                    justify='center'
                ),
                dmc.Space(h=20),
                dmc.Group(
                    children=[
                        dmc.Button('Cancel', id=f'{PREFIX}-prospect-delete-cancel', color='violet', variant="subtle"),
                        html.Div(id=f'{PREFIX}-prospect-delete-submit-div'),
                    ],
                    justify="flex-end",
                ),
            ],
            style={'padding': '20px'}
        )
    ],
    title='Delete Prospect',
    id=f'{PREFIX}-modal-prospect-delete',
    size='xl',
)

# -----------------------------------------------------------------------------
# - TABLE PROSPECTS LIST
# -----------------------------------------------------------------------------
PROSPECT_LIST = dmc.Group(
    children=[
        dmc.Stack(id=f'{PREFIX}-prospects-list')
    ], grow=True
)