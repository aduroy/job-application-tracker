import datetime

import dash_mantine_components as dmc
from dash import Dash, html, Output, Input, State, callback, dcc
from dash_iconify import DashIconify


from utils import get_written_days_from_date

PREFIX = 'applications-overview'

VIOLET = '#7950f2'
RED = '#fa5252'
GREEN = '#82c91e'

ADD_NEW_APPLICATION = dmc.Group(
    children=[
        dmc.Button(
            'New job application',
            id=f'{PREFIX}-application-new',
            color='violet',
            leftSection=DashIconify(icon="ic:round-plus"),
            size='md'
        )
    ],
    justify='flex-end',
    style={'margin-top': '70px'}
)


FILTER_SORT = dmc.Group(
    children=[
        dmc.Select(
            id=f'{PREFIX}-filter-status',
            label="Status",
            data=[
                {'value': 'all', 'label': 'All'},
                {'value': 'applied_only', 'label': 'Applied-only'},
                {'value': 'running', 'label': 'Running'},
                {'value': 'declined', 'label': 'Declined'},
            ],
            value="all",
        )
    ],
)


APPLICATION_LIST = dmc.Group(children=[dmc.Stack(id=f'{PREFIX}-application-list')], grow=True)

APPLICATION_LOAD = dcc.Store(id=f'{PREFIX}-store-load')


def get_application_status_layout(application_data):
    applied = VIOLET
    running = GREEN
    declined = RED

    color = applied
    if application_data.decline_date: color = declined
    elif application_data.application_steps: color = running

    status_layout = dmc.Stack(
        children=[],
        style={'background-color': color, 'width': '7px', 'height': '150px'}
    )

    return status_layout


def get_last_step_before_date(application_data, ref_date=datetime.date.today()):
    steps = sorted([s for s in application_data.application_steps if s.scheduled_date <= ref_date], key=lambda x: x.scheduled_date)

    step = None
    if len(steps) > 0:
        step = steps[-1]

    return step


def get_next_step_after_date(application_data, ref_date=datetime.date.today()):
    steps = sorted([s for s in application_data.application_steps if s.scheduled_date >= ref_date], key=lambda x: x.scheduled_date)

    step = None
    if len(steps) > 0:
        step = steps[0]

    return step


def get_application_timeline_layout(application_data):

    none_step = dmc.TimelineItem(
        title="_", lineVariant="dashed",
        children=[dmc.Text(['_'], size="sm", style={'color': 'transparent'})],
        style={'color': 'transparent'}
    )

    application_step = dmc.TimelineItem(
        title="Application",
        children=[
            dmc.Text(
                get_written_days_from_date(application_data.application_date),
                size='sm', c='dimmed',
                style={'width': '100%', 'font-style': 'normal'}
            )
        ],
        style={'font-style': 'italic'}
    )

    if application_data.decline_date:
        last_step_before_decline = get_last_step_before_date(application_data, ref_date=application_data.decline_date)

        if not last_step_before_decline:
            last_step = application_step
        else:
            last_step = dmc.TimelineItem(
                title=last_step_before_decline.name,
                children=[
                    dmc.Text(
                        get_written_days_from_date(last_step_before_decline.scheduled_date),
                        size='sm', c='dimmed',
                        style={'width': '100%'}
                    )
                ],
            )

        decline_step = dmc.TimelineItem(
            title="Declined",
            children=[
                dmc.Text(
                    [get_written_days_from_date(application_data.decline_date)],
                    c="dimmed",
                    size="sm",
                    style={'font-style': 'normal'}
                ),
            ],
            style={'font-style': 'italic'}
        )
        items = [
            last_step,
            decline_step
        ]

        items = items[::-1]
        active = 1
    else:
        last_step_before_now = get_last_step_before_date(application_data)
        next_step_after_now = get_next_step_after_date(application_data)

        if not last_step_before_now:
            last_step = application_step
        else:
            last_step = dmc.TimelineItem(
                title=last_step_before_now.name,
                children=[
                    dmc.Text([get_written_days_from_date(last_step_before_now.scheduled_date)], c="dimmed", size="sm")
                ],
            )

        if not next_step_after_now:
            next_step = none_step
        else:
            next_step = dmc.TimelineItem(
                title=next_step_after_now.name,
                children=[
                    dmc.Text(
                        [get_written_days_from_date(next_step_after_now.scheduled_date)],
                        c="dimmed",
                        size="sm",
                    ),
                ],
            )

        items = [
            last_step,
            next_step
        ]

        items = items[::-1]
        active = 0

    timeline_layout = dmc.Stack(
        children=[
            dmc.Timeline(
                active=active,
                reverseActive=True,
                align='right',
                bulletSize=15,
                lineWidth=2,
                color='violet',
                children=items,
                style={'margin-bottom': '10px', 'height': '100%', 'margin-top': '20px'}
            ),
        ],
        gap=0,
        style={'width': '200px'}
    )

    return timeline_layout


def get_application_main_layout(application_data):

    application_id = application_data.id
    job_title = application_data.job_title
    company = application_data.company
    city = application_data.city
    application_date = application_data.application_date
    via = application_data.via
    offer_link = application_data.offer_link
    map_link = application_data.map_link

    via_mapping = {
        'website': 'Website',
        'linkedin': 'Linkedin'
    }

    via = via_mapping[via]

    anchor_offer_link = None
    if offer_link:
        anchor_offer_link = dmc.Stack([
            dmc.Anchor([
                dmc.ActionIcon(
                    children=[
                        DashIconify(icon="mingcute:external-link-line")
                    ],
                    variant='subtle'
                )
            ], href=offer_link, target='_blank', id=f'{PREFIX}-offer-link')
        ])

    anchor_map_link = None
    if map_link:
        anchor_map_link = dmc.Stack([
            dmc.Anchor([
                dmc.ActionIcon(
                    children=[
                        DashIconify(icon="mingcute:external-link-line")
                    ],
                    variant='subtle'
                )
            ], href=map_link, target='_blank', id=f'{PREFIX}-offer-link')
        ])

    main_layout = dmc.Stack(
        children=[
            dmc.Group(
                children=[
                    dmc.Stack([
                        dmc.Text(job_title, fw=700, size='xl', style={'width': '100%', 'margin-bottom': '15px', 'margin-top': '9px'}),
                    ]),
                    dmc.Stack([
                        dmc.ActionIcon(
                            id={'type': f'{PREFIX}-application-details', 'index': application_id},
                            children=[
                                DashIconify(icon="ri:side-bar-line")
                            ],
                            size='md', color='violet',
                            variant='subtle'
                        )
                    ]),
                ],
                gap=5
            ),
            dmc.Group([
                dmc.Stack([
                    dmc.Group([
                        dmc.Stack([DashIconify(icon="mdi:at", color='#7950f2', width=20)]),
                        dmc.Stack([dmc.Text(company, fw=300, size='md', style={'width': '100%'})]),
                    ], align='center', gap=10),
                ]),
                dmc.Stack([
                    dmc.Group([
                        dmc.Stack([DashIconify(icon="mdi:location", color='#7950f2', width=20)]),
                        # dmc.Stack([dmc.Text(city, fw=300, size='md', style={'width': '100%'})]),
                        dmc.Stack([
                            dmc.Group(
                                children=[
                                    dmc.Stack([
                                        dmc.Text(city, fw=300, size='md'),
                                    ]),
                                    anchor_map_link,
                                ],
                                gap=5,
                                align='center',
                            ),
                        ]),
                    ], align='center', gap=10),
                ]),
            ], grow=True),
            dmc.Group([
                dmc.Stack([
                    dmc.Group([
                        dmc.Stack([DashIconify(icon="ri:calendar-line", color='#7950f2', width=20)]),
                        dmc.Stack([
                            dmc.Tooltip(
                                label=application_date.strftime('%b %d, %Y'),
                                position="bottom",
                                children=[
                                    dmc.Text(get_written_days_from_date(application_date), fw=300, size='md', style={'width': '100%'}),]
                            ),
                        ]),
                    ], align='center', gap=10),
                ]),
                dmc.Stack([
                    dmc.Group([
                        dmc.Stack([DashIconify(icon="material-symbols:mail-outline", color='#7950f2', width=20)]),
                        dmc.Stack([
                            dmc.Group(
                                children=[
                                    dmc.Stack([
                                        dmc.Text(via, fw=300, size='md'),
                                    ]),
                                    anchor_offer_link,
                                ],
                                gap=5,
                                align='center',
                            ),
                        ]),
                    ], align='center', gap=10),
                ]),
            ], grow=True),
        ],
        flex=1, gap=0
    )

    return main_layout


def get_application_notes_layout(application_data):

    notes = application_data.notes

    notes_layout = dmc.Stack(
        children=[
            dmc.Text('Notes', fw=500, c='dimmed', size='md', style={'width': '100%', 'margin-top': '10px'}),
            dmc.ScrollArea(
                children=[
                    dmc.Code(notes, block=True)
                ],
                h=107, offsetScrollbars=False
            )
        ],
        gap=0,
        style={'width': '350px'}
    )

    return notes_layout


def get_application_overview_layout(application_data):
    application_layout = dmc.Group(
        children=[
            dmc.Card(
                children=[
                    dmc.Group(
                        children=[
                            get_application_status_layout(application_data),
                            get_application_timeline_layout(application_data),
                            get_application_main_layout(application_data),
                            get_application_notes_layout(application_data),
                        ],
                        align='start',
                        gap=20
                    )
                ],
                withBorder=True,
                shadow='md',
            )
        ],
        grow=True
    )

    return application_layout


if __name__ == '__main__':
    pass
