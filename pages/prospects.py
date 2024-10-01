from pages.prospects_modules.overview import (
    PROSPECTS_LOAD, PROSPECT_LIST, ADD_NEW_PROSPECT,
    PROSPECTS_MODAL_EDIT, PROSPECTS_MODAL_CREATE, PROSPECTS_MODAL_DELETE
)
from pages.prospects_modules.callbacks import *

dash.register_page(__name__)

PREFIX = 'prospects-overview'

layout = dmc.Stack(
    children=[
        PROSPECTS_LOAD,
        PROSPECTS_MODAL_EDIT,
        PROSPECTS_MODAL_CREATE,
        PROSPECTS_MODAL_DELETE,
        ADD_NEW_PROSPECT,
        PROSPECT_LIST,
    ]
)