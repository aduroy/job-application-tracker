import datetime
import json

import dash
from dash import html, Output, Input, State, callback, dcc, ALL, MATCH
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from utils import get_written_days_from_date
from database.controllers_applications import ApplicationHelper, ApplicationStepHelper, ContactHelper
from pages.applications_modules.overview import get_application_overview_layout

# -----------------------------------------------------------------------------
# - Applications Overview
# -----------------------------------------------------------------------------
PRE_OVERVIEW = 'applications-overview'
PRE_DETAILS = 'application-details'
PRE_APP_NEW = 'application-new'
PRE_APP_EDIT = 'application-edit'


@callback(
    Output(f'{PRE_OVERVIEW}-application-list', 'children'),
    Input(f'{PRE_OVERVIEW}-filter-status', 'value'),
    Input(f'{PRE_OVERVIEW}-store-load', 'data'),
)
def display_applications(filter_status, load_dt):
    applications = ApplicationHelper.get_all(status=filter_status)

    children = []
    for a in applications:
        application_layout = get_application_overview_layout(a)
        children.append(application_layout)

    return children


@callback(
    [
        Output(f"{PRE_DETAILS}-drawer", "opened", allow_duplicate=True),
        Output(f"{PRE_DETAILS}-store-current", "data"),
    ],
    Input({'type': f'{PRE_OVERVIEW}-application-details', 'index': ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def toggle_drawer(buttons):
    all_n_clicks = [b for b in buttons if b]
    if len(all_n_clicks) == 0:
        return dash.no_update, dash.no_update

    input_id = dash.callback_context.triggered[0]["prop_id"].split(".n_clicks")[0]
    input_type = json.loads(input_id)["type"]
    input_index = json.loads(input_id)["index"]

    reload_dt = datetime.datetime.utcnow().isoformat()

    return (
        True,
        {'application_id': input_index, 'load_dt': reload_dt},
    )


@callback(
    [
        Output(f"{PRE_DETAILS}-job-title", "children"),
        Output(f"{PRE_DETAILS}-company", "children"),
        Output(f"{PRE_DETAILS}-city", "children"),
        Output(f"{PRE_DETAILS}-application-date", "children"),
        Output(f"{PRE_DETAILS}-via", "children"),
        Output(f"{PRE_DETAILS}-offer-link", "children"),
        Output(f"{PRE_DETAILS}-map-link", "children"),
        Output(f"{PRE_DETAILS}-notes", "children"),
    ],
    Input(f'{PRE_DETAILS}-store-current', 'data'),
    prevent_initial_call=True,
)
def update_application_summary(details_load_dt):
    app_id = details_load_dt.get('application_id')
    application = ApplicationHelper.get(application_id=app_id)

    job_title = dash.no_update
    company = dash.no_update
    city = dash.no_update
    application_date = dash.no_update
    via = dash.no_update
    offer_link = dash.no_update
    map_link = dash.no_update
    notes = dash.no_update

    if application is None:
        return (
            job_title, company, city,
            application_date, via,
            offer_link, map_link, notes,
        )

    job_title = application.job_title
    company = application.company
    city = application.city
    application_date = get_written_days_from_date(application.application_date, include_date=True)
    via = application.via
    offer_link = application.offer_link
    map_link = application.map_link
    notes = application.notes

    via_mapping = {
        'website': 'Website',
        'linkedin': 'Linkedin'
    }
    via = f'via {via_mapping[via]}'

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
            ], href=offer_link, target='_blank')
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
            ], href=map_link, target='_blank')
        ])

    return (
        job_title, company, city,
        application_date, via,
        anchor_offer_link, anchor_map_link, notes
    )


@callback(
    Output(f"{PRE_DETAILS}-contacts", "children"),
    Input(f'{PRE_DETAILS}-store-current', 'data'),
    prevent_initial_call=True,
)
def update_application_contacts(details_load_dt):
    app_id = details_load_dt.get('application_id')
    application = ApplicationHelper.get(application_id=app_id)

    contacts_table = dash.no_update
    if application is None:
        return contacts_table

    if application.contacts:
        rows = [
            dmc.TableTr(
                [
                    dmc.TableTd(c.name),
                    dmc.TableTd(c.position),
                    dmc.TableTd(c.notes),
                    dmc.TableTd(
                        children=[
                            dmc.Menu(
                                [
                                    dmc.MenuTarget(dmc.ActionIcon(DashIconify(icon="mage:dots"), variant='subtle', color='violet')),
                                    dmc.MenuDropdown([
                                        dmc.MenuItem("Edit", id={'type': f'{PRE_DETAILS}-contact-edit', 'index': c.id}, leftSection=DashIconify(icon="mi:edit")),
                                        dmc.MenuItem("Delete", id={'type': f'{PRE_DETAILS}-contact-delete', 'index': c.id}, leftSection=DashIconify(icon="mi:delete"))
                                    ]),
                                ],
                            )
                        ],
                        style={'width': '1%'}
                    ),
                ]
            )
            for c in application.contacts
        ]
    else:
        rows = [
            dmc.TableTr(
                [
                    dmc.TableTd(dmc.Skeleton(h=10, radius="xl", mt=10, w='70%')),
                    dmc.TableTd(dmc.Skeleton(h=10, radius="xl", mt=10, w='70%')),
                    dmc.TableTd(dmc.Skeleton(h=10, radius="xl", mt=10, w='70%')),
                    dmc.TableTd(dmc.Skeleton(h=10, radius="xl", mt=10, w='70%')),
                ]
            )
        ]

    head = dmc.TableThead(
        dmc.TableTr(
            [
                dmc.TableTh("Name"),
                dmc.TableTh("Position"),
                dmc.TableTh("Notes"),
                dmc.TableTh(""),
            ]
        )
    )
    body = dmc.TableTbody(rows)
    contacts_table = dmc.Table([head, body])

    return contacts_table


def generate_layout_timeline_item(s, line_variant):
    via_map = {
        'on_site': 'On-site',
        'phone_call': 'Phone Call',
        'video_call': 'Video Call',
        'home': 'At Home',
        'other': 'Other',
    }
    via = via_map.get(s.via)
    via = '' if not via else f' - {via}'

    new_step = dmc.TimelineItem(
        title=s.name,
        lineVariant=line_variant,
        children=[
            dmc.Group(
                children=[
                    dmc.Stack(
                        children=[
                            dmc.Text(
                                children=[f'{get_written_days_from_date(s.scheduled_date, include_date=True)}{via}'],
                                c="dimmed",
                                size="sm",
                            ),
                        ]
                    ),
                    dmc.Stack([
                        dmc.Menu(
                            [
                                dmc.MenuTarget(
                                    dmc.ActionIcon(DashIconify(icon="mage:dots"), variant='subtle', color='violet')),
                                dmc.MenuDropdown([
                                    dmc.MenuItem("Edit", id={'type': f'{PRE_DETAILS}-timeline-edit', 'index': s.id},
                                                 leftSection=DashIconify(icon="mi:edit")),
                                    dmc.MenuItem("Delete", id={'type': f'{PRE_DETAILS}-timeline-delete', 'index': s.id},
                                                 leftSection=DashIconify(icon="mi:delete"))
                                ]),
                            ],
                        )
                    ]),
                ],
                justify='space-between'
            ),
            dmc.Text('Notes', fw=500, c='dimmed', size='md', style={'width': '100%', 'margin-top': '10px'}),
            dmc.ScrollArea(
                children=[
                    dmc.Code(s.notes, block=True)
                ],
                offsetScrollbars=False,
                style={'max-height': '107px'}
            )
        ],
    )

    return new_step


@callback(
    Output(f"{PRE_DETAILS}-timeline", "children"),
    Input(f'{PRE_DETAILS}-store-current', 'data'),
    prevent_initial_call=True,
)
def update_application_timeline(details_load_dt):
    app_id = details_load_dt.get('application_id')
    application = ApplicationHelper.get(application_id=app_id)

    timeline = dash.no_update
    if application is None:
        return timeline

    step_0 = dmc.TimelineItem(
        title="Application",
        children=[
            dmc.Group(children=[]),
            dmc.Text(
                children=[get_written_days_from_date(application.application_date, include_date=True)],
                c="dimmed",
                size="sm",
            ),
        ],
    )

    steps = [step_0]
    active = 0

    # Sort steps, None last
    application_steps = sorted(application.application_steps, key=lambda x: (x is None, x.scheduled_date))
    # If declined, ignore steps after
    if application.decline_date:
        application_steps_before_decline = [s for s in application_steps if s.scheduled_date <= application.decline_date]
        application_steps_after_decline = [s for s in application_steps if s.scheduled_date > application.decline_date]
    else:
        application_steps_before_decline = [s for s in application_steps]
        application_steps_after_decline = []

    for s in application_steps_before_decline:
        line_variant = 'solid'
        if s.scheduled_date >= datetime.date.today() and not application.decline_date:
            line_variant = 'dashed'
        else:
            active += 1

        new_step = generate_layout_timeline_item(s, line_variant)
        steps.append(new_step)

    if application.decline_date:
        decline_step = dmc.TimelineItem(
            title="Declined",
            children=[
                dmc.Text(
                    [get_written_days_from_date(application.decline_date, include_date=True)],
                    c="dimmed",
                    size="sm",
                ),
            ],
        )
        steps.append(decline_step)
        active += 1

    for s in application_steps_after_decline:
        line_variant = 'solid'
        if s.scheduled_date >= datetime.date.today() and not application.decline_date:
            line_variant = 'dashed'

        new_step = generate_layout_timeline_item(s, line_variant)
        steps.append(new_step)

    none_step = dmc.TimelineItem(
        title="_", lineVariant="dashed",
        children=[dmc.Text(['_'], size="sm", style={'color': 'transparent'})],
        style={'color': 'transparent'}
    )

    steps.append(none_step)
    steps = steps[::-1]

    timeline = dmc.Timeline(
        active=active,
        bulletSize=17,
        lineWidth=2,
        reverseActive=True,
        color='violet',
        style={'width': '100%'},
        children=steps
    )

    return timeline


@callback(
    Output(f'{PRE_APP_NEW}-modal-application-create', "opened"),
    Output(f'{PRE_APP_NEW}-application-create-job-title', "value"),
    Output(f'{PRE_APP_NEW}-application-create-company', "value"),
    Output(f'{PRE_APP_NEW}-application-create-city', "value"),
    Output(f'{PRE_APP_NEW}-application-create-date', "value"),
    Output(f'{PRE_APP_NEW}-application-create-via', "value"),
    Output(f'{PRE_APP_NEW}-application-create-link', "value"),
    Output(f'{PRE_APP_NEW}-application-create-notes', "value"),
    Output(f'{PRE_APP_NEW}-application-create-map-link', "value"),
    Output(f'{PRE_APP_NEW}-application-new-errors', "children"),
    Output(f'{PRE_OVERVIEW}-store-load', 'data', allow_duplicate=True),

    Input(f'{PRE_OVERVIEW}-application-new', "n_clicks"),
    Input(f'{PRE_APP_NEW}-application-new-cancel', "n_clicks"),
    Input(f'{PRE_APP_NEW}-application-new-submit', "n_clicks"),

    State(f'{PRE_APP_NEW}-application-create-job-title', "value"),
    State(f'{PRE_APP_NEW}-application-create-company', "value"),
    State(f'{PRE_APP_NEW}-application-create-city', "value"),
    State(f'{PRE_APP_NEW}-application-create-date', "value"),
    State(f'{PRE_APP_NEW}-application-create-via', "value"),
    State(f'{PRE_APP_NEW}-application-create-link', "value"),
    State(f'{PRE_APP_NEW}-application-create-notes', "value"),
    State(f'{PRE_APP_NEW}-application-create-map-link', "value"),
    prevent_initial_call=True,
)
def modal_application_create(
        nc1, nc2, nc3,
        job_title, company, city, application_date, via, offer_link,
        notes, map_link
):
    is_open = dash.no_update
    new_job_title = dash.no_update
    new_company = dash.no_update
    new_city = dash.no_update
    new_application_date = dash.no_update
    new_via = dash.no_update
    new_offer_link = dash.no_update
    new_notes = dash.no_update
    new_map_link = dash.no_update
    new_errors = dash.no_update
    store_load = dash.no_update

    input_id = dash.callback_context.triggered[0]["prop_id"].split(".n_clicks")[0]

    if input_id.endswith('application-new'):
        is_open = True
        new_job_title = None
        new_company = None
        new_city = None
        new_application_date = datetime.date.today()
        new_offer_link = None
        new_notes = None
        new_map_link = None
        new_errors = None
    elif input_id.endswith('application-new-cancel'):
        is_open = False
    elif input_id.endswith('application-new-submit'):
        if not job_title or not company or not city or not application_date or not via:
            new_errors = dmc.Text('Missing required fields.', c='red')
        else:
            new_application = {
                'job_title': job_title,
                'company': company,
                'city': city,
                'application_date': datetime.datetime.fromisoformat(application_date).date(),
                'via': via,
                'offer_link': offer_link,
                'notes': notes,
                'map_link': map_link,
            }
            ApplicationHelper.create(**new_application)
            is_open = False
            reload_dt = datetime.datetime.utcnow().isoformat()
            store_load = {'load_dt': reload_dt}

    return (
        is_open,
        new_job_title, new_company, new_city, new_application_date, new_via, new_offer_link,
        new_notes, new_map_link,
        new_errors,
        store_load
    )


@callback(
    Output(f'{PRE_APP_EDIT}-modal-application-edit', "opened"),
    Output(f'{PRE_APP_EDIT}-application-edit-job-title', "value"),
    Output(f'{PRE_APP_EDIT}-application-edit-company', "value"),
    Output(f'{PRE_APP_EDIT}-application-edit-city', "value"),
    Output(f'{PRE_APP_EDIT}-application-edit-date', "value"),
    Output(f'{PRE_APP_EDIT}-application-edit-decline-date', "value"),
    Output(f'{PRE_APP_EDIT}-application-edit-via', "value"),
    Output(f'{PRE_APP_EDIT}-application-edit-link', "value"),
    Output(f'{PRE_APP_EDIT}-application-edit-notes', "value"),
    Output(f'{PRE_APP_EDIT}-application-edit-map-link', "value"),
    Output(f'{PRE_APP_EDIT}-application-edit-errors', "children"),
    Output(f'{PRE_OVERVIEW}-store-load', 'data', allow_duplicate=True),
    Output(f'{PRE_DETAILS}-store-current', 'data', allow_duplicate=True),

    Input(f'{PRE_DETAILS}-application-edit', "n_clicks"),
    Input(f'{PRE_APP_EDIT}-application-edit-cancel', "n_clicks"),
    Input(f'{PRE_APP_EDIT}-application-edit-submit', "n_clicks"),

    State(f'{PRE_APP_EDIT}-application-edit-job-title', "value"),
    State(f'{PRE_APP_EDIT}-application-edit-company', "value"),
    State(f'{PRE_APP_EDIT}-application-edit-city', "value"),
    State(f'{PRE_APP_EDIT}-application-edit-date', "value"),
    State(f'{PRE_APP_EDIT}-application-edit-decline-date', "value"),
    State(f'{PRE_APP_EDIT}-application-edit-via', "value"),
    State(f'{PRE_APP_EDIT}-application-edit-link', "value"),
    State(f'{PRE_APP_EDIT}-application-edit-notes', "value"),
    State(f'{PRE_APP_EDIT}-application-edit-map-link', "value"),
    State(f'{PRE_DETAILS}-store-current', "data"),
    prevent_initial_call=True,
)
def modal_application_edit(
        nc1, nc2, nc3,
        job_title, company, city, application_date, decline_date, via, offer_link,
        notes, map_link,
        current_app
):
    is_open = dash.no_update
    new_job_title = dash.no_update
    new_company = dash.no_update
    new_city = dash.no_update
    new_application_date = dash.no_update
    new_decline_date = dash.no_update
    new_via = dash.no_update
    new_offer_link = dash.no_update
    new_notes = dash.no_update
    new_map_link = dash.no_update
    new_errors = dash.no_update
    store_load = dash.no_update
    store_current = dash.no_update

    input_id = dash.callback_context.triggered[0]["prop_id"].split(".n_clicks")[0]

    if input_id.endswith('application-edit'):
        app_id = current_app.get('application_id')
        application = ApplicationHelper.get(application_id=app_id)
        is_open = True
        new_job_title = application.job_title
        new_company = application.company
        new_city = application.city
        new_application_date = application.application_date
        new_decline_date = application.decline_date
        new_offer_link = application.offer_link
        new_notes = application.notes
        new_map_link = application.map_link
        new_errors = None
    elif input_id.endswith('application-edit-cancel'):
        is_open = False
    elif input_id.endswith('application-edit-submit'):
        if not job_title or not company or not city or not application_date or not via:
            new_errors = dmc.Text('Missing required fields.', c='red')
        else:
            new_application = {
                'job_title': job_title,
                'company': company,
                'city': city,
                'application_date': datetime.datetime.fromisoformat(application_date).date(),
                'decline_date': datetime.datetime.fromisoformat(decline_date).date() if decline_date else None,
                'via': via,
                'offer_link': offer_link,
                'notes': notes,
                'map_link': map_link,
            }

            app_id = current_app.get('application_id')
            ApplicationHelper.update(application_id=app_id, **new_application)
            is_open = False

            reload_dt = datetime.datetime.utcnow().isoformat()
            store_load = {'load_dt': reload_dt}

            reload_dt = datetime.datetime.utcnow().isoformat()
            store_current = {'application_id': app_id, 'load_dt': reload_dt}

    return (
        is_open,
        new_job_title, new_company, new_city, new_application_date, new_decline_date, new_via, new_offer_link,
        new_notes, new_map_link,
        new_errors,
        store_load, store_current
    )


@callback(
    Output(f'{PRE_DETAILS}-modal-application-delete', "opened"),
    Output(f'{PRE_DETAILS}-drawer', "opened", allow_duplicate=True),
    Output(f'{PRE_DETAILS}-application-delete-name', "children"),
    Output(f'{PRE_OVERVIEW}-store-load', 'data', allow_duplicate=True),


    Input(f'{PRE_DETAILS}-application-delete', "n_clicks"),
    Input(f'{PRE_DETAILS}-application-delete-cancel', "n_clicks"),
    Input(f'{PRE_DETAILS}-application-delete-submit', "n_clicks"),

    State(f'{PRE_DETAILS}-store-current', "data"),
    prevent_initial_call=True,
)
def modal_application_delete(nc1, nc2, nc3, current_app):
    is_open = dash.no_update
    is_open_drawer = dash.no_update
    app_job_title = dash.no_update
    store_load = dash.no_update

    input_id = dash.callback_context.triggered[0]["prop_id"].split(".n_clicks")[0]

    if input_id.endswith('application-delete-cancel'):
        is_open = False

        return (
            is_open, is_open_drawer,
            app_job_title,
            store_load
        )

    if input_id.endswith('application-delete'):
        app_id = current_app.get('application_id')
        application = ApplicationHelper.get(application_id=app_id)
        is_open = True
        app_job_title = application.job_title
    elif input_id.endswith('application-delete-submit'):
        app_id = current_app.get('application_id')
        ApplicationHelper.delete(application_id=app_id)
        is_open = False
        is_open_drawer = False
        reload_dt = datetime.datetime.utcnow().isoformat()
        store_load = {'load_dt': reload_dt}

    return (
        is_open, is_open_drawer,
        app_job_title,
        store_load
    )


@callback(
    Output(f'{PRE_DETAILS}-modal-contact-create', "opened"),
    Output(f'{PRE_DETAILS}-contact-new-name', "value"),
    Output(f'{PRE_DETAILS}-contact-new-position', "value"),
    Output(f'{PRE_DETAILS}-contact-new-notes', "value"),
    Output(f'{PRE_DETAILS}-store-current', 'data', allow_duplicate=True),

    Input(f'{PRE_DETAILS}-contact-new', "n_clicks"),
    Input(f'{PRE_DETAILS}-contact-new-cancel', "n_clicks"),
    Input(f'{PRE_DETAILS}-contact-new-submit', "n_clicks"),

    State(f'{PRE_DETAILS}-contact-new-name', "value"),
    State(f'{PRE_DETAILS}-contact-new-position', "value"),
    State(f'{PRE_DETAILS}-contact-new-notes', "value"),
    State(f'{PRE_DETAILS}-store-current', "data"),
    prevent_initial_call=True,
)
def modal_contact_create(nc1, nc2, nc3, name, position, notes, current_app):
    is_open = dash.no_update
    new_name = dash.no_update
    new_position = dash.no_update
    new_notes = dash.no_update
    store_current = dash.no_update

    input_id = dash.callback_context.triggered[0]["prop_id"].split(".n_clicks")[0]

    if input_id.endswith('contact-new'):
        is_open = True
        new_name = None
        new_position = None
        new_notes = None
    elif input_id.endswith('contact-new-cancel'):
        is_open = False
    elif input_id.endswith('contact-new-submit'):
        app_id = current_app.get('application_id')
        new_contact = {
            'application_id': app_id,
            'name': name,
            'position': position,
            'notes': notes
        }
        ContactHelper.create(**new_contact)
        is_open = False
        reload_dt = datetime.datetime.utcnow().isoformat()
        store_current = {'application_id': app_id, 'load_dt': reload_dt}

    return (
        is_open,
        new_name, new_position, new_notes,
        store_current
    )


@callback(
    Output(f'{PRE_DETAILS}-modal-contact-edit', "opened"),
    Output(f'{PRE_DETAILS}-contact-edit-name', "value"),
    Output(f'{PRE_DETAILS}-contact-edit-position', "value"),
    Output(f'{PRE_DETAILS}-contact-edit-notes', "value"),
    Output(f'{PRE_DETAILS}-store-current', 'data', allow_duplicate=True),
    Output(f'{PRE_DETAILS}-contact-edit-submit-div', 'children'),

    Input({'type': f'{PRE_DETAILS}-contact-edit', 'index': ALL}, "n_clicks"),
    Input(f'{PRE_DETAILS}-contact-edit-cancel', "n_clicks"),
    Input({'type': f'{PRE_DETAILS}-contact-edit-submit', 'index': ALL}, "n_clicks"),

    State(f'{PRE_DETAILS}-contact-edit-name', "value"),
    State(f'{PRE_DETAILS}-contact-edit-position', "value"),
    State(f'{PRE_DETAILS}-contact-edit-notes', "value"),
    State(f'{PRE_DETAILS}-store-current', "data"),
    prevent_initial_call=True,
)
def modal_contact_edit(nc1, nc2, nc3, name, position, notes, current_app):
    is_open = dash.no_update
    new_name = dash.no_update
    new_position = dash.no_update
    new_notes = dash.no_update
    store_current = dash.no_update
    submit_button = dash.no_update

    all_edit_clicks = [b for b in nc1 if b]
    if len(all_edit_clicks) == 0:
        return (
            is_open,
            new_name, new_position, new_notes,
            store_current, submit_button
        )

    input_id = dash.callback_context.triggered[0]["prop_id"].split(".n_clicks")[0]

    if input_id.endswith('contact-edit-cancel'):
        is_open = False

        return (
            is_open,
            new_name, new_position, new_notes,
            store_current, submit_button
        )

    input_type = json.loads(input_id)["type"]
    input_index = json.loads(input_id)["index"]

    if input_type.endswith('contact-edit'):
        contact = ContactHelper.get(contact_id=input_index)
        is_open = True
        new_name = contact.name
        new_position = contact.position
        new_notes = contact.notes
        submit_button = dmc.Button('Save', id={'type': f'{PRE_DETAILS}-contact-edit-submit', 'index': contact.id}, color='violet')
    elif input_type.endswith('contact-edit-submit'):
        app_id = current_app.get('application_id')
        update_contact = {
            'application_id': app_id,
            'name': name,
            'position': position,
            'notes': notes
        }
        ContactHelper.update(contact_id=input_index, **update_contact)
        is_open = False
        reload_dt = datetime.datetime.utcnow().isoformat()
        store_current = {'application_id': app_id, 'load_dt': reload_dt}

    return (
        is_open,
        new_name, new_position, new_notes,
        store_current, submit_button
    )


@callback(
    Output(f'{PRE_DETAILS}-modal-contact-delete', "opened"),
    Output(f'{PRE_DETAILS}-contact-delete-name', "children"),
    Output(f'{PRE_DETAILS}-store-current', 'data', allow_duplicate=True),
    Output(f'{PRE_DETAILS}-contact-delete-submit-div', 'children'),

    Input({'type': f'{PRE_DETAILS}-contact-delete', 'index': ALL}, "n_clicks"),
    Input(f'{PRE_DETAILS}-contact-delete-cancel', "n_clicks"),
    Input({'type': f'{PRE_DETAILS}-contact-delete-submit', 'index': ALL}, "n_clicks"),

    State(f'{PRE_DETAILS}-store-current', "data"),
    prevent_initial_call=True,
)
def modal_contact_delete(nc1, nc2, nc3, current_app):
    is_open = dash.no_update
    contact_name = dash.no_update
    store_current = dash.no_update
    submit_button = dash.no_update

    all_edit_clicks = [b for b in nc1 if b]
    if len(all_edit_clicks) == 0:
        return (
            is_open,
            contact_name,
            store_current, submit_button
        )

    input_id = dash.callback_context.triggered[0]["prop_id"].split(".n_clicks")[0]

    if input_id.endswith('contact-delete-cancel'):
        is_open = False

        return (
            is_open,
            contact_name,
            store_current, submit_button
        )

    input_type = json.loads(input_id)["type"]
    input_index = json.loads(input_id)["index"]

    if input_type.endswith('contact-delete'):
        contact = ContactHelper.get(contact_id=input_index)
        is_open = True
        contact_name = contact.name
        submit_button = dmc.Button('Delete', id={'type': f'{PRE_DETAILS}-contact-delete-submit', 'index': contact.id}, color='#fa5252')
    elif input_type.endswith('contact-delete-submit'):
        app_id = current_app.get('application_id')
        ContactHelper.delete(contact_id=input_index)
        is_open = False
        reload_dt = datetime.datetime.utcnow().isoformat()
        store_current = {'application_id': app_id, 'load_dt': reload_dt}

    return (
        is_open,
        contact_name,
        store_current, submit_button
    )

@callback(
    Output(f'{PRE_DETAILS}-modal-timeline-create', "opened"),
    Output(f'{PRE_DETAILS}-timeline-new-name', "value"),
    Output(f'{PRE_DETAILS}-timeline-new-via', "value"),
    Output(f'{PRE_DETAILS}-timeline-new-scheduled-at', "value"),
    Output(f'{PRE_DETAILS}-timeline-new-notes', "value"),
    Output(f'{PRE_DETAILS}-store-current', 'data', allow_duplicate=True),
    Output(f'{PRE_OVERVIEW}-store-load', 'data', allow_duplicate=True),

    Input(f'{PRE_DETAILS}-timeline-new', "n_clicks"),
    Input(f'{PRE_DETAILS}-timeline-new-cancel', "n_clicks"),
    Input(f'{PRE_DETAILS}-timeline-new-submit', "n_clicks"),

    State(f'{PRE_DETAILS}-timeline-new-name', "value"),
    State(f'{PRE_DETAILS}-timeline-new-via', "value"),
    State(f'{PRE_DETAILS}-timeline-new-scheduled-at', "value"),
    State(f'{PRE_DETAILS}-timeline-new-notes', "value"),
    State(f'{PRE_DETAILS}-store-current', "data"),
    prevent_initial_call=True,
)
def modal_timeline_create(nc1, nc2, nc3, name, via, scheduled_at, notes, current_app):
    is_open = dash.no_update
    new_name = dash.no_update
    new_via = dash.no_update
    new_scheduled_at = dash.no_update
    new_notes = dash.no_update
    store_current = dash.no_update
    store_load = dash.no_update

    input_id = dash.callback_context.triggered[0]["prop_id"].split(".n_clicks")[0]

    if input_id.endswith('timeline-new'):
        is_open = True
        new_name = None
        new_via = 'on_site'
        new_scheduled_at = datetime.date.today()
        new_notes = None
    elif input_id.endswith('timeline-new-cancel'):
        is_open = False
    elif input_id.endswith('timeline-new-submit'):
        app_id = current_app.get('application_id')
        new_step = {
            'application_id': app_id,
            'name': name,
            'scheduled_date': datetime.datetime.fromisoformat(scheduled_at).date(),
            'via': via,
            'notes': notes
        }
        ApplicationStepHelper.create(**new_step)
        is_open = False
        reload_dt = datetime.datetime.utcnow().isoformat()
        store_current = {'application_id': app_id, 'load_dt': reload_dt}
        store_load = {'load_dt': reload_dt}

    return (
        is_open,
        new_name, new_via, new_scheduled_at, new_notes,
        store_current, store_load
    )


@callback(
    Output(f'{PRE_DETAILS}-modal-timeline-edit', "opened"),
    Output(f'{PRE_DETAILS}-timeline-edit-name', "value"),
    Output(f'{PRE_DETAILS}-timeline-edit-via', "value"),
    Output(f'{PRE_DETAILS}-timeline-edit-scheduled-at', "value"),
    Output(f'{PRE_DETAILS}-timeline-edit-notes', "value"),
    Output(f'{PRE_DETAILS}-store-current', 'data', allow_duplicate=True),
    Output(f'{PRE_OVERVIEW}-store-load', 'data', allow_duplicate=True),
    Output(f'{PRE_DETAILS}-timeline-edit-submit-div', 'children'),

    Input({'type': f'{PRE_DETAILS}-timeline-edit', 'index': ALL}, "n_clicks"),
    Input(f'{PRE_DETAILS}-timeline-edit-cancel', "n_clicks"),
    Input({'type': f'{PRE_DETAILS}-timeline-edit-submit', 'index': ALL}, "n_clicks"),

    State(f'{PRE_DETAILS}-timeline-edit-name', "value"),
    State(f'{PRE_DETAILS}-timeline-edit-via', "value"),
    State(f'{PRE_DETAILS}-timeline-edit-scheduled-at', "value"),
    State(f'{PRE_DETAILS}-timeline-edit-notes', "value"),
    State(f'{PRE_DETAILS}-store-current', "data"),
    prevent_initial_call=True,
)
def modal_timeline_edit(nc1, nc2, nc3, name, via, scheduled_at, notes, current_app):
    is_open = dash.no_update
    new_name = dash.no_update
    new_via = dash.no_update
    new_scheduled_at = dash.no_update
    new_notes = dash.no_update
    store_current = dash.no_update
    store_load = dash.no_update
    submit_button = dash.no_update

    all_edit_clicks = [b for b in nc1 if b]
    if len(all_edit_clicks) == 0:
        return (
            is_open,
            new_name, new_via, new_scheduled_at, new_notes,
            store_current, store_load, submit_button
        )

    input_id = dash.callback_context.triggered[0]["prop_id"].split(".n_clicks")[0]

    if input_id.endswith('timeline-edit-cancel'):
        is_open = False

        return (
            is_open,
            new_name, new_via, new_scheduled_at, new_notes,
            store_current, store_load, submit_button
        )

    input_type = json.loads(input_id)["type"]
    input_index = json.loads(input_id)["index"]

    if input_type.endswith('timeline-edit'):
        step = ApplicationStepHelper.get(step_id=input_index)
        is_open = True
        new_name = step.name
        new_via = step.via
        new_scheduled_at = step.scheduled_date
        new_notes = step.notes
        submit_button = dmc.Button('Save', id={'type': f'{PRE_DETAILS}-timeline-edit-submit', 'index': step.id}, color='violet')
    elif input_type.endswith('timeline-edit-submit'):
        app_id = current_app.get('application_id')
        update_step = {
            'application_id': app_id,
            'name': name,
            'scheduled_date': datetime.datetime.fromisoformat(scheduled_at).date(),
            'via': via,
            'notes': notes
        }
        ApplicationStepHelper.update(step_id=input_index, **update_step)
        is_open = False
        reload_dt = datetime.datetime.utcnow().isoformat()
        store_current = {'application_id': app_id, 'load_dt': reload_dt}
        store_load = {'load_dt': reload_dt}

    return (
        is_open,
        new_name, new_via, new_scheduled_at, new_notes,
        store_current, store_load, submit_button
    )


@callback(
    Output(f'{PRE_DETAILS}-modal-timeline-delete', "opened"),
    Output(f'{PRE_DETAILS}-timeline-delete-name', "children"),
    Output(f'{PRE_DETAILS}-store-current', 'data', allow_duplicate=True),
    Output(f'{PRE_OVERVIEW}-store-load', 'data', allow_duplicate=True),
    Output(f'{PRE_DETAILS}-timeline-delete-submit-div', 'children'),

    Input({'type': f'{PRE_DETAILS}-timeline-delete', 'index': ALL}, "n_clicks"),
    Input(f'{PRE_DETAILS}-timeline-delete-cancel', "n_clicks"),
    Input({'type': f'{PRE_DETAILS}-timeline-delete-submit', 'index': ALL}, "n_clicks"),

    State(f'{PRE_DETAILS}-store-current', "data"),
    prevent_initial_call=True,
)
def modal_timeline_delete(nc1, nc2, nc3, current_app):
    is_open = dash.no_update
    step_name = dash.no_update
    store_current = dash.no_update
    store_load = dash.no_update
    submit_button = dash.no_update

    all_edit_clicks = [b for b in nc1 if b]
    if len(all_edit_clicks) == 0:
        return (
            is_open,
            step_name,
            store_current, store_load, submit_button
        )

    input_id = dash.callback_context.triggered[0]["prop_id"].split(".n_clicks")[0]

    if input_id.endswith('timeline-delete-cancel'):
        is_open = False

        return (
            is_open,
            step_name,
            store_current, store_load, submit_button
        )

    input_type = json.loads(input_id)["type"]
    input_index = json.loads(input_id)["index"]

    if input_type.endswith('timeline-delete'):
        step = ApplicationStepHelper.get(step_id=input_index)
        is_open = True
        step_name = step.name
        submit_button = dmc.Button('Delete', id={'type': f'{PRE_DETAILS}-timeline-delete-submit', 'index': step.id}, color='#fa5252')
    elif input_type.endswith('timeline-delete-submit'):
        app_id = current_app.get('application_id')
        ApplicationStepHelper.delete(step_id=input_index)
        is_open = False
        reload_dt = datetime.datetime.utcnow().isoformat()
        store_current = {'application_id': app_id, 'load_dt': reload_dt}
        store_load = {'load_dt': reload_dt}

    return (
        is_open,
        step_name,
        store_current, store_load, submit_button
    )