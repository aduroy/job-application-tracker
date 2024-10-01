import dash_mantine_components as dmc
from dash import html


PREFIX = 'application-edit'


APPLICATION_EDIT_MODAL = dmc.Modal(
    title='Edit Job Application',
    id=f'{PREFIX}-modal-application-edit',
    size='xl',
    children=[
        html.Div(
            children=[
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.TextInput(id=f'{PREFIX}-application-edit-job-title', label='Job title', required=True),
                                dmc.TextInput(id=f'{PREFIX}-application-edit-company', label='Company', required=True),
                                dmc.TextInput(id=f'{PREFIX}-application-edit-city', label='City', required=True),
                            ],
                        ),
                        dmc.Stack(
                            children=[
                                dmc.DatesProvider(
                                    children=[
                                        dmc.Group(
                                            children=[
                                                dmc.Stack(
                                                    children=[
                                                        dmc.DatePicker(id=f'{PREFIX}-application-edit-date', label='Application date', required=True, valueFormat="MMM DD, YY"),
                                                    ]
                                                ),
                                                dmc.Stack(
                                                    children=[
                                                        dmc.DatePicker(id=f'{PREFIX}-application-edit-decline-date', label='Decline date', clearable=True, valueFormat="MMM DD, YY"),
                                                    ]
                                                )
                                            ],
                                            grow=True
                                        ),
                                    ],
                                    settings={"locale": "fr", "firstDayOfWeek": 1, "weekendDays": [0, 6]},
                                ),
                                dmc.Select(
                                    id=f'{PREFIX}-application-edit-via',
                                    label="Via",
                                    value='website',
                                    required=True,
                                    data=[
                                        {"value": "website", "label": "Website"},
                                        {"value": "linkedin", "label": "LinkedIn"},
                                    ],
                                ),
                                dmc.TextInput(id=f'{PREFIX}-application-edit-link', label='Link to offer', required=False),
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
                                    id=f'{PREFIX}-application-edit-notes',
                                    label="Notes",
                                    placeholder="",
                                    # w=500,
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
                        dmc.Stack(
                            children=[
                                dmc.TextInput(label='GoogleMaps/OpenStreeMap link', id=f'{PREFIX}-application-edit-map-link'),
                            ]
                        )
                    ],
                    grow=True
                ),
                dmc.Space(h=40),
                dmc.Group(
                    children=[
                        html.Div(id=f'{PREFIX}-application-edit-errors'),
                        dmc.Button('Cancel', id=f'{PREFIX}-application-edit-cancel', color='violet', variant="subtle"),
                        dmc.Button('Save', id=f'{PREFIX}-application-edit-submit', color='violet'),
                    ],
                    justify="flex-end",
                ),
            ],
            style={'padding': '20px'}
        )
    ],
)