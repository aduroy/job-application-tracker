from pages.applications_modules.overview import APPLICATION_LOAD, ADD_NEW_APPLICATION, FILTER_SORT, APPLICATION_LIST
from pages.applications_modules.application_details import DRAWER
from pages.applications_modules.application_new import APPLICATION_NEW_MODAL
from pages.applications_modules.callbacks import *

dash.register_page(__name__)

layout = dmc.Stack(
    children=[
        APPLICATION_LOAD,
        APPLICATION_NEW_MODAL,
        ADD_NEW_APPLICATION,
        FILTER_SORT,
        APPLICATION_LIST,
        DRAWER
    ]
)