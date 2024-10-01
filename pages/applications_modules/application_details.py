import dash_mantine_components as dmc
from dash import Dash, html, Output, Input, State, callback, dcc
from dash_iconify import DashIconify
import datetime

from pages.applications_modules.application_edit import APPLICATION_EDIT_MODAL


PREFIX = 'application-details'


APPLICATION_NOTES = dmc.Stack(
    children=[
        dmc.Text('Notes', fw=500, c='dimmed', size='md', style={'width': '100%', 'margin-top': '10px'}),
        dmc.ScrollArea(
            children=[
                dmc.Code(id=f'{PREFIX}-notes', block=True, style={'height': '107px'})
            ],
            h=107, offsetScrollbars=False
        )
    ],
    gap=0,
    style={'width': '100%'}
)


COMPANY_SUMMARY = dmc.Group(
    children=[
        dmc.Stack(
            children=[
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Text(id=f'{PREFIX}-job-title', fw=700, size='xl'),
                            ]
                        ),
                        dmc.Stack(
                            children=[
                                dmc.Menu(
                                    [
                                        dmc.MenuTarget(dmc.ActionIcon(DashIconify(icon="material-symbols:settings"), variant='subtle', color='violet')),
                                        dmc.MenuDropdown([
                                            dmc.MenuItem("Edit", id=f'{PREFIX}-application-edit', leftSection=DashIconify(icon="mi:edit")),
                                            dmc.MenuItem("Delete", id=f'{PREFIX}-application-delete', leftSection=DashIconify(icon="mi:delete"))
                                        ]),
                                    ],
                                )
                            ]
                        ),
                    ],
                    gap=5,
                    align='flex-end',
                    justify='space-between',
                    style={'margin-bottom': '15px'}
                ),
                dmc.Group([
                    dmc.Stack([
                        dmc.Group([
                            dmc.Stack([DashIconify(icon="mdi:at", color='#7950f2', width=20)]),
                            dmc.Stack([dmc.Text(id=f'{PREFIX}-company', fw=300, size='md', style={'width': '100%'})]),
                        ], align='center', gap=10),
                    ]),
                    dmc.Stack([
                        dmc.Group([
                            dmc.Stack([DashIconify(icon="mdi:location", color='#7950f2', width=20)]),
                            dmc.Stack([
                                dmc.Group(
                                    children=[
                                        dmc.Stack([
                                            dmc.Text(id=f'{PREFIX}-city', fw=300, size='md'),
                                        ]),
                                        html.Div(id=f'{PREFIX}-map-link'),
                                    ],
                                    gap=5,
                                    align='center',
                                ),
                            ]),
                        ], align='center', gap=10),
                    ]),
                ], grow=True),
                dmc.Space(h=20),
                dmc.Group([
                    dmc.Stack([
                        dmc.Group([
                            dmc.Stack([DashIconify(icon="ri:calendar-line", color='#7950f2', width=20)]),
                            dmc.Stack([dmc.Text(id=f'{PREFIX}-application-date', fw=300, size='md', style={'width': '100%'})]),
                        ], align='center', gap=10),
                    ]),
                    dmc.Stack([
                        dmc.Group([
                            dmc.Stack([DashIconify(icon="material-symbols:mail-outline", color='#7950f2', width=20)]),
                            dmc.Stack([
                                dmc.Group(
                                    children=[
                                        dmc.Stack([
                                            dmc.Text(id=f'{PREFIX}-via', fw=300, size='md'),
                                        ]),
                                        html.Div(id=f'{PREFIX}-offer-link'),
                                    ],
                                    gap=5,
                                    align='center',
                                ),
                            ]),
                        ], align='center', gap=10),
                    ]),
                ], grow=True),
                dmc.Space(h=20),
                dmc.Group(
                    children=[
                        APPLICATION_NOTES
                    ]
                )
            ],
            flex=1, gap=0
        ),
    ],
    align='flex-start',
)


APPLICATION_MODAL_DELETE = dmc.Modal(
    children=[
        html.Div(
            children=[
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Text('Permanently delete:'),
                                dmc.Text(id=f'{PREFIX}-application-delete-name', style={'text-align': 'center'}, fw=700),
                            ],
                        ),
                    ],
                    justify='center'
                ),
                dmc.Space(h=20),
                dmc.Group(
                    children=[
                        dmc.Button('Cancel', id=f'{PREFIX}-application-delete-cancel', color='violet', variant="subtle"),
                        dmc.Button('Delete', id=f'{PREFIX}-application-delete-submit', color='#fa5252'),
                    ],
                    justify="flex-end",
                ),
            ],
            style={'padding': '20px'}
        )
    ],
    title='Delete Application',
    id=f'{PREFIX}-modal-application-delete',
    size='xl',
)


CONTACTS_HEADER = dmc.Group(
    children=[
        dmc.Stack(
            children=[
                dmc.Text('Contacts', fw=700, size='lg'),
            ]
        ),
        dmc.Stack(
            children=[
                dmc.Button(
                    'New contact',
                    id=f'{PREFIX}-contact-new',
                    color='violet',
                    leftSection=DashIconify(icon="ic:round-plus"),
                    size='sm'
                )
            ]
        )
    ],
    justify='space-between',
)

CONTACTS_MODAL_CREATE = dmc.Modal(
    children=[
        html.Div(
            children=[
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.TextInput(id=f'{PREFIX}-contact-new-name', label='Name', required=True),
                            ],
                        ),
                        dmc.Stack(
                            children=[
                                dmc.TextInput(id=f'{PREFIX}-contact-new-position', label='Position'),
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
                                    id=f'{PREFIX}-contact-new-notes',
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
                        dmc.Button('Cancel', id=f'{PREFIX}-contact-new-cancel', color='violet', variant="subtle"),
                        dmc.Button('Save', id=f'{PREFIX}-contact-new-submit', color='violet'),
                    ],
                    justify="flex-end",
                ),
            ],
            style={'padding': '20px'}
        )
    ],
    title='Create New Contact',
    id=f'{PREFIX}-modal-contact-create',
    size='xl',
)

CONTACTS_MODAL_EDIT = dmc.Modal(
    children=[
        html.Div(
            children=[
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.TextInput(id=f'{PREFIX}-contact-edit-name', label='Name', required=True),
                            ],
                        ),
                        dmc.Stack(
                            children=[
                                dmc.TextInput(id=f'{PREFIX}-contact-edit-position', label='Position'),
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
                                    id=f'{PREFIX}-contact-edit-notes',
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
                        dmc.Button('Cancel', id=f'{PREFIX}-contact-edit-cancel', color='violet', variant="subtle"),
                        html.Div(id=f'{PREFIX}-contact-edit-submit-div'),
                    ],
                    justify="flex-end",
                ),
            ],
            style={'padding': '20px'}
        )
    ],
    title='Edit Contact',
    id=f'{PREFIX}-modal-contact-edit',
    size='xl',
)

CONTACTS_MODAL_DELETE = dmc.Modal(
    children=[
        html.Div(
            children=[
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Text('Permanently delete:'),
                                dmc.Text(id=f'{PREFIX}-contact-delete-name', style={'text-align': 'center'}, fw=700),
                            ],
                        ),
                    ],
                    justify='center'
                ),
                dmc.Space(h=20),
                dmc.Group(
                    children=[
                        dmc.Button('Cancel', id=f'{PREFIX}-contact-delete-cancel', color='violet', variant="subtle"),
                        html.Div(id=f'{PREFIX}-contact-delete-submit-div'),
                    ],
                    justify="flex-end",
                ),
            ],
            style={'padding': '20px'}
        )
    ],
    title='Delete Contact',
    id=f'{PREFIX}-modal-contact-delete',
    size='xl',
)


CONTACTS = dmc.Group(
    id=f'{PREFIX}-contacts',
    children=[],
    align='flex-start',
)


TIMELINE_HEADER = dmc.Group(
    children=[
        dmc.Stack(
            children=[
                dmc.Text('Timeline', fw=700, size='lg'),
            ]
        ),
        dmc.Stack(
            children=[
                dmc.Button(
                    'New step',
                    id=f'{PREFIX}-timeline-new',
                    color='violet',
                    leftSection=DashIconify(icon="ic:round-plus"),
                    size='sm'
                )
            ]
        )
    ],
    justify='space-between',
)


TIMELINE_MODAL_CREATE = dmc.Modal(
    children=[
        html.Div(
            children=[
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.TextInput(id=f'{PREFIX}-timeline-new-name', label='Name', required=True),
                            ],
                        ),
                        dmc.Stack(
                            children=[
                                dmc.Select(
                                    id=f'{PREFIX}-timeline-new-via', label='Location',
                                    data=[
                                        {"value": "on_site", "label": "On-site"},
                                        {"value": "phone_call", "label": "Phone Call"},
                                        {"value": "video_call", "label": "Video Call"},
                                        {"value": "home", "label": "At Home"},
                                        {"value": "other", "label": "Other"},
                                    ],
                                    value='on_site'
                                ),
                            ],
                        ),
                        dmc.Stack(
                            children=[
                                dmc.DatePicker(
                                    id=f'{PREFIX}-timeline-new-scheduled-at',
                                    label='Scheduled date', required=True,
                                    value=datetime.date.today()
                                ),
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
                                    id=f'{PREFIX}-timeline-new-notes',
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
                        dmc.Button('Cancel', id=f'{PREFIX}-timeline-new-cancel', color='violet', variant="subtle"),
                        dmc.Button('Save', id=f'{PREFIX}-timeline-new-submit', color='violet'),
                    ],
                    justify="flex-end",
                ),
            ],
            style={'padding': '20px'}
        )
    ],
    title='Create New Step',
    id=f'{PREFIX}-modal-timeline-create',
    size='xl',
)

TIMELINE_MODAL_EDIT = dmc.Modal(
    children=[
        html.Div(
            children=[
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.TextInput(id=f'{PREFIX}-timeline-edit-name', label='Name', required=True),
                            ],
                        ),
                        dmc.Stack(
                            children=[
                                dmc.Select(
                                    id=f'{PREFIX}-timeline-edit-via', label='Location',
                                    data=[
                                        {"value": "on_site", "label": "On-site"},
                                        {"value": "phone_call", "label": "Phone Call"},
                                        {"value": "video_call", "label": "Video Call"},
                                        {"value": "home", "label": "At Home"},
                                        {"value": "other", "label": "Other"},
                                    ],
                                    value='on_site'
                                ),
                            ],
                        ),
                        dmc.Stack(
                            children=[
                                dmc.DatePicker(
                                    id=f'{PREFIX}-timeline-edit-scheduled-at',
                                    label='Scheduled date', required=True,
                                    value=datetime.date.today()
                                ),
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
                                    id=f'{PREFIX}-timeline-edit-notes',
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
                        dmc.Button('Cancel', id=f'{PREFIX}-timeline-edit-cancel', color='violet', variant="subtle"),
                        html.Div(id=f'{PREFIX}-timeline-edit-submit-div'),
                    ],
                    justify="flex-end",
                ),
            ],
            style={'padding': '20px'}
        )
    ],
    title='Edit Step',
    id=f'{PREFIX}-modal-timeline-edit',
    size='xl',
)

TIMELINE_MODAL_DELETE = dmc.Modal(
    children=[
        html.Div(
            children=[
                dmc.Group(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Text('Permanently delete:'),
                                dmc.Text(id=f'{PREFIX}-timeline-delete-name', style={'text-align': 'center'}, fw=700),
                            ],
                        ),
                    ],
                    justify='center'
                ),
                dmc.Space(h=20),
                dmc.Group(
                    children=[
                        dmc.Button('Cancel', id=f'{PREFIX}-timeline-delete-cancel', color='violet', variant="subtle"),
                        html.Div(id=f'{PREFIX}-timeline-delete-submit-div'),
                    ],
                    justify="flex-end",
                ),
            ],
            style={'padding': '20px'}
        )
    ],
    title='Delete Step',
    id=f'{PREFIX}-modal-timeline-delete',
    size='xl',
)


TIMELINE = dmc.Group(
    id=f'{PREFIX}-timeline',
    children=[],
    align='flex-start',
)

DRAWER = dmc.Drawer(
    id=f"{PREFIX}-drawer",
    position='right',
    size=800,
    children=[
        html.Div(
            children=[
                dcc.Store(id=f'{PREFIX}-store-current'),
                APPLICATION_EDIT_MODAL,
                APPLICATION_MODAL_DELETE,
                COMPANY_SUMMARY,
                dmc.Space(h=40),
                CONTACTS_HEADER,
                CONTACTS_MODAL_CREATE,
                CONTACTS_MODAL_EDIT,
                CONTACTS_MODAL_DELETE,
                dmc.Space(h=30),
                CONTACTS,
                dmc.Space(h=40),
                TIMELINE_HEADER,
                TIMELINE_MODAL_CREATE,
                TIMELINE_MODAL_EDIT,
                TIMELINE_MODAL_DELETE,
                dmc.Space(h=30),
                TIMELINE
            ],
            style={'padding': '0 50px 50px 50px'}
        )
    ],
)