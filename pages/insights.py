import dash
import dash_mantine_components as dmc

from pages.insights_modules.overview import FILTERS, MAIN_LAYOUT
from pages.insights_modules.callbacks import *


dash.register_page(__name__)

PREFIX = 'insights-overview'

layout = dmc.Stack(
    children=[
        FILTERS,
        dmc.Space(h=40),
        MAIN_LAYOUT
    ]
)