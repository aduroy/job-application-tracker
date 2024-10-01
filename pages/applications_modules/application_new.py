import dash_mantine_components as dmc
from dash import html


PREFIX = 'application-new'


APPLICATION_NEW_MODAL = dmc.Modal(
    title='New Job Application',
    id=f'{PREFIX}-modal-application-create',
    size='xl',
    children=[
        html.Div(
            children=[
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.TextInput(id=f'{PREFIX}-application-create-job-title', label='Job title', required=True),
                                dmc.TextInput(id=f'{PREFIX}-application-create-company', label='Company', required=True),
                                dmc.TextInput(id=f'{PREFIX}-application-create-city', label='City', required=True),
                            ],
                        ),
                        dmc.Stack(
                            children=[
                                dmc.DatesProvider(
                                    children=[
                                        dmc.DatePicker(id=f'{PREFIX}-application-create-date', label='Application date', required=True, valueFormat="MMM DD, YY"),
                                    ],
                                    settings={"locale": "en", "firstDayOfWeek": 1, "weekendDays": [0, 6]},
                                ),
                                dmc.Select(
                                    id=f'{PREFIX}-application-create-via',
                                    label="Via",
                                    value='website',
                                    required=True,
                                    data=[
                                        {"value": "website", "label": "Website"},
                                        {"value": "linkedin", "label": "LinkedIn"},
                                    ],
                                ),
                                dmc.TextInput(id=f'{PREFIX}-application-create-link', label='Link to offer', required=False),
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
                                    id=f'{PREFIX}-application-create-notes',
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
                        dmc.Stack(
                            children=[
                                dmc.TextInput(id=f'{PREFIX}-application-create-map-link', label='GoogleMaps/OpenStreeMap link'),
                            ]
                        )
                    ],
                    grow=True
                ),
                dmc.Space(h=40),
                dmc.Group(
                    children=[
                        html.Div(id=f'{PREFIX}-application-new-errors'),
                        dmc.Button('Cancel', id=f'{PREFIX}-application-new-cancel', color='violet', variant="subtle"),
                        dmc.Button('Save', id=f'{PREFIX}-application-new-submit', color='violet'),
                    ],
                    justify="flex-end",
                ),
            ],
            style={'padding': '20px'}
        )
    ],
)