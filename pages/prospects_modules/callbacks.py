import datetime
import json

import dash
from dash import Output, Input, State, callback, ALL
import dash_mantine_components as dmc
from dash_iconify import DashIconify

from database.controllers_prospects import ProspectHelper


PRE_OVERVIEW = 'prospects-overview'


def get_anchor_from_link(l, name=None):
    anchor = dmc.Anchor(name if name else l, href=l, target='_blank')

    return anchor


def get_notes_block(notes):
    notes_block = None
    if notes:
        notes_block = dmc.Code(notes, block=True)

    return notes_block


@callback(
    Output(f'{PRE_OVERVIEW}-prospects-list', 'children'),
    Input(f'{PRE_OVERVIEW}-store-load-time', "data"),
)
def display_prospects(load_time):
    """ Display prospects list everytime the list is modified (create, edit, delete)
    """

    prospects = ProspectHelper.get_all()

    if prospects:
        rows = [
            dmc.TableTr(
                [
                    dmc.TableTd(p.name),
                    dmc.TableTd(get_anchor_from_link(p.url)),
                    dmc.TableTd(get_notes_block(p.notes)),
                    dmc.TableTd(
                        children=[
                            dmc.Menu(
                                [
                                    dmc.MenuTarget(dmc.ActionIcon(DashIconify(icon="mage:dots"), variant='subtle', color='violet')),
                                    dmc.MenuDropdown([
                                        dmc.MenuItem(
                                            "Edit",
                                            id={'type': f'{PRE_OVERVIEW}-prospect-edit', 'index': p.id},
                                            leftSection=DashIconify(icon="mi:edit")
                                        ),
                                        dmc.MenuItem(
                                            "Delete",
                                            id={'type': f'{PRE_OVERVIEW}-prospect-delete', 'index': p.id},
                                            leftSection=DashIconify(icon="mi:delete"))
                                    ]),
                                ],
                            )
                        ],
                        style={'width': '1%'}
                    ),
                ]
            )
            for p in prospects
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
                dmc.TableTh("URL"),
                dmc.TableTh("Notes"),
                dmc.TableTh(""),
            ]
        )
    )
    body = dmc.TableTbody(rows)
    contacts_table = dmc.Table([head, body])

    return contacts_table


@callback(
    Output(f'{PRE_OVERVIEW}-modal-prospect-create', "opened"),
    Output(f'{PRE_OVERVIEW}-prospect-new-name', "value"),
    Output(f'{PRE_OVERVIEW}-prospect-new-url', "value"),
    Output(f'{PRE_OVERVIEW}-prospect-new-notes', "value"),
    Output(f'{PRE_OVERVIEW}-store-load-time', 'data', allow_duplicate=True),

    Input(f'{PRE_OVERVIEW}-prospect-new', "n_clicks"),
    Input(f'{PRE_OVERVIEW}-prospect-new-cancel', "n_clicks"),
    Input(f'{PRE_OVERVIEW}-prospect-new-submit', "n_clicks"),

    State(f'{PRE_OVERVIEW}-prospect-new-name', "value"),
    State(f'{PRE_OVERVIEW}-prospect-new-url', "value"),
    State(f'{PRE_OVERVIEW}-prospect-new-notes', "value"),
    prevent_initial_call=True,
)
def modal_prospect_create(nc1, nc2, nc3, name, url, notes):
    """ Handle all interactions with the modal used for creating a new prospect
    """
    is_open = dash.no_update
    new_name = dash.no_update
    new_url = dash.no_update
    new_notes = dash.no_update
    store_load = dash.no_update

    input_id = dash.callback_context.triggered[0]["prop_id"].split(".n_clicks")[0]

    if input_id.endswith('prospect-new'):
        is_open = True
        new_name = None
        new_url = None
        new_notes = None
    elif input_id.endswith('prospect-new-cancel'):
        is_open = False
    elif input_id.endswith('prospect-new-submit'):
        new_contact = {
            'name': name,
            'url': url,
            'notes': notes
        }
        ProspectHelper.create(**new_contact)
        is_open = False
        reload_dt = datetime.datetime.utcnow().isoformat()
        store_load = {'load_dt': reload_dt}

    return (
        is_open,
        new_name, new_url, new_notes,
        store_load
    )


@callback(
    Output(f'{PRE_OVERVIEW}-modal-prospect-edit', "opened"),
    Output(f'{PRE_OVERVIEW}-prospect-edit-name', "value"),
    Output(f'{PRE_OVERVIEW}-prospect-edit-url', "value"),
    Output(f'{PRE_OVERVIEW}-prospect-edit-notes', "value"),
    Output(f'{PRE_OVERVIEW}-store-load-time', 'data', allow_duplicate=True),
    Output(f'{PRE_OVERVIEW}-prospect-edit-submit-div', 'children'),

    Input({'type': f'{PRE_OVERVIEW}-prospect-edit', 'index': ALL}, "n_clicks"),
    Input(f'{PRE_OVERVIEW}-prospect-edit-cancel', "n_clicks"),
    Input({'type': f'{PRE_OVERVIEW}-prospect-edit-submit', 'index': ALL}, "n_clicks"),

    State(f'{PRE_OVERVIEW}-prospect-edit-name', "value"),
    State(f'{PRE_OVERVIEW}-prospect-edit-url', "value"),
    State(f'{PRE_OVERVIEW}-prospect-edit-notes', "value"),
    prevent_initial_call=True,
)
def modal_contact_edit(nc1, nc2, nc3, name, url, notes):
    """ Handle all interactions with the modal used for editing an existing prospect
    """
    is_open = dash.no_update
    new_name = dash.no_update
    new_url = dash.no_update
    new_notes = dash.no_update
    store_load = dash.no_update
    submit_button = dash.no_update

    all_edit_clicks = [b for b in nc1 if b]
    if len(all_edit_clicks) == 0:
        return (
            is_open,
            new_name, new_url, new_notes,
            store_load, submit_button
        )

    input_id = dash.callback_context.triggered[0]["prop_id"].split(".n_clicks")[0]

    if input_id.endswith('prospect-edit-cancel'):
        is_open = False

        return (
            is_open,
            new_name, new_url, new_notes,
            store_load, submit_button
        )

    input_type = json.loads(input_id)["type"]
    input_index = json.loads(input_id)["index"]

    if input_type.endswith('prospect-edit'):
        prospect = ProspectHelper.get(prospect_id=input_index)
        is_open = True
        new_name = prospect.name
        new_url = prospect.url
        new_notes = prospect.notes
        submit_button = dmc.Button('Save', id={'type': f'{PRE_OVERVIEW}-prospect-edit-submit', 'index': prospect.id}, color='violet')
    elif input_type.endswith('prospect-edit-submit'):
        update_contact = {
            'name': name,
            'url': url,
            'notes': notes
        }
        ProspectHelper.update(prospect_id=input_index, **update_contact)
        is_open = False
        reload_dt = datetime.datetime.utcnow().isoformat()
        store_load = {'load_dt': reload_dt}

    return (
        is_open,
        new_name, new_url, new_notes,
        store_load, submit_button
    )


@callback(
    Output(f'{PRE_OVERVIEW}-modal-prospect-delete', "opened"),
    Output(f'{PRE_OVERVIEW}-prospect-delete-name', "children"),
    Output(f'{PRE_OVERVIEW}-store-load-time', 'data', allow_duplicate=True),
    Output(f'{PRE_OVERVIEW}-prospect-delete-submit-div', 'children'),

    Input({'type': f'{PRE_OVERVIEW}-prospect-delete', 'index': ALL}, "n_clicks"),
    Input(f'{PRE_OVERVIEW}-prospect-delete-cancel', "n_clicks"),
    Input({'type': f'{PRE_OVERVIEW}-prospect-delete-submit', 'index': ALL}, "n_clicks"),
    prevent_initial_call=True,
)
def modal_contact_delete(nc1, nc2, nc3):
    """ Handle all interactions with the modal used for deleting an existing prospect
    """
    is_open = dash.no_update
    prospect_name = dash.no_update
    store_load = dash.no_update
    submit_button = dash.no_update

    all_edit_clicks = [b for b in nc1 if b]
    if len(all_edit_clicks) == 0:
        return (
            is_open,
            prospect_name,
            store_load, submit_button
        )

    input_id = dash.callback_context.triggered[0]["prop_id"].split(".n_clicks")[0]

    if input_id.endswith('prospect-delete-cancel'):
        is_open = False

        return (
            is_open,
            prospect_name,
            store_load, submit_button
        )

    input_type = json.loads(input_id)["type"]
    input_index = json.loads(input_id)["index"]

    if input_type.endswith('prospect-delete'):
        prospect = ProspectHelper.get(prospect_id=input_index)
        is_open = True
        prospect_name = prospect.name
        submit_button = dmc.Button('Delete', id={'type': f'{PRE_OVERVIEW}-prospect-delete-submit', 'index': prospect.id}, color='#fa5252')
    elif input_type.endswith('prospect-delete-submit'):
        ProspectHelper.delete(prospect_id=input_index)
        is_open = False
        reload_dt = datetime.datetime.utcnow().isoformat()
        store_load = {'load_dt': reload_dt}

    return (
        is_open,
        prospect_name,
        store_load, submit_button
    )
