import datetime

from dash import Output, Input, callback
import pandas as pd
import plotly.graph_objs as go

from database.controllers_applications import ApplicationHelper, ApplicationStepHelper


PRE_OVERVIEW = 'insights-overview'


@callback(
    Output(f'{PRE_OVERVIEW}-from', 'value'),
    Output(f'{PRE_OVERVIEW}-to', 'value'),
    Input(f'{PRE_OVERVIEW}-reset', 'n_clicks'),
)
def reset_dates(n_clicks):
    """ Reset input dates (from, to) to (min_date, today)
    """
    min_date = ApplicationHelper.get_min_application_date()
    from_ = min_date
    to_ = datetime.date.today()

    return from_, to_


@callback(
    Output(f'{PRE_OVERVIEW}-applications-total', 'children'),
    Input(f'{PRE_OVERVIEW}-from', 'value'),
    Input(f'{PRE_OVERVIEW}-to', 'value'),
    prevent_initial_call=True,
)
def display_applications_total(from_, to_):
    """ Display total number of applications
    """
    applications_total = ApplicationHelper.get_total(from_=from_, to_=to_)

    return applications_total


@callback(
    Output(f'{PRE_OVERVIEW}-steps-total', 'children'),
    Input(f'{PRE_OVERVIEW}-from', 'value'),
    Input(f'{PRE_OVERVIEW}-to', 'value'),
    prevent_initial_call=True,
)
def display_steps_total(from_, to_):
    """ Display total number of application steps
    """
    steps_total = ApplicationStepHelper.get_total(from_=from_, to_=to_)

    return steps_total


@callback(
    Output(f'{PRE_OVERVIEW}-applications-only', 'children'),
    Input(f'{PRE_OVERVIEW}-from', 'value'),
    Input(f'{PRE_OVERVIEW}-to', 'value'),
    prevent_initial_call=True,
)
def display_applications_only(from_, to_):
    """ Display total number of applications having no steps
    """
    applications_total = ApplicationHelper.get_total_no_step(from_=from_, to_=to_)

    return applications_total


@callback(
    Output(f'{PRE_OVERVIEW}-days-first-step', 'children'),
    Input(f'{PRE_OVERVIEW}-from', 'value'),
    Input(f'{PRE_OVERVIEW}-to', 'value'),
    prevent_initial_call=True,
)
def display_days_first_step(from_, to_):
    """ Display average number of days between an application and its first step
    """
    applications = ApplicationHelper.get_all_at_least_a_step(from_=from_, to_=to_)

    days_until_first_step = [
        (a.application_steps[0].scheduled_date - a.application_date).days
        for a in applications
    ]

    days_first_step = 'Unknown'
    if len(days_until_first_step) > 0:
        d = "{:.0f}".format(sum(days_until_first_step) / len(days_until_first_step))
        days_first_step = f'{d} days'

    return days_first_step


@callback(
    Output(f'{PRE_OVERVIEW}-days-between-steps', 'children'),
    Input(f'{PRE_OVERVIEW}-from', 'value'),
    Input(f'{PRE_OVERVIEW}-to', 'value'),
    prevent_initial_call=True,
)
def display_days_between_steps(from_, to_):
    """ Display average number of days between an application's steps
    """
    steps = ApplicationStepHelper.get_all(from_=from_, to_=to_, sort_by='application_id')

    days_between_steps = []
    last_application_id = None
    last_step = None
    for s in steps:
        if last_application_id is None or last_application_id != s.application_id:
            pass
        else:
            delta_days = (s.scheduled_date - last_step.scheduled_date).days
            days_between_steps.append(delta_days)

        last_application_id = s.application_id
        last_step = s

    days_btw_steps = 'Unknown'
    if len(days_between_steps) > 0:
        d = "{:.0f}".format(sum(days_between_steps) / len(days_between_steps))
        days_btw_steps = f'{d} days'

    return days_btw_steps


@callback(
    Output(f'{PRE_OVERVIEW}-days-decline', 'children'),
    Input(f'{PRE_OVERVIEW}-from', 'value'),
    Input(f'{PRE_OVERVIEW}-to', 'value'),
    prevent_initial_call=True,
)
def display_days_decline(from_, to_):
    """ Display average number of days between an application and the decline date
    """
    applications = ApplicationHelper.get_all_declined(from_=from_, to_=to_)

    days_until_decline = [
        (a.decline_date - a.application_date).days
        for a in applications
    ]

    days_decline = 'Unknown'
    if len(days_until_decline) > 0:
        d = "{:.0f}".format(sum(days_until_decline) / len(days_until_decline))
        days_decline = f'{d} days'

    return days_decline


def generate_chart_params(from_, to_, by_):
    """ Generate parameters used by Plotly's figure to draw charts, based on X-axis type
    """
    tickformat = None
    dtick = None
    type_ = None
    category_order = None
    category_array = None
    range_ = None
    if by_ == 'day':
        if from_: from_ = datetime.datetime.strptime(from_, '%Y-%m-%d') - datetime.timedelta(days=1)
        if to_: to_ = datetime.datetime.strptime(to_, '%Y-%m-%d') + datetime.timedelta(days=1)
        range_ = [from_, to_]
    elif by_ == 'week':
        tickformat = "%Y-%W"
    elif by_ == 'month':
        tickformat = "%Y-%m"
        dtick = 'M1'
    elif by_ == 'weekday':
        tickformat = "%a"
        type_ = 'category'
        category_order = 'array'
        category_array = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    elif by_ == 'monthday':
        range_ = [0, 32]

    return (
        tickformat, dtick,
        type_, category_order, category_array,
        range_
    )


def generate_chart_data(df, by_):
    """ Generate dataset to draw charts, based on X-axis type
    """
    if by_ == 'week':
        df['date'] = df['date'].apply(lambda x: x.strftime('%G-W%V'))
    elif by_ == 'month':
        df['date'] = df['date'].apply(lambda x: x.strftime('%Y-%m'))
    elif by_ == 'weekday':
        df['date'] = df['date'].apply(lambda x: x.strftime('%A'))
    elif by_ == 'monthday':
        df['date'] = pd.to_datetime(df['date']).dt.day

    df = df.groupby(['date'])['total'].sum().reset_index()

    return df


@callback(
    Output(f'{PRE_OVERVIEW}-graph-applications-steps-decline', 'figure'),
    Input(f'{PRE_OVERVIEW}-from', 'value'),
    Input(f'{PRE_OVERVIEW}-to', 'value'),
    Input(f'{PRE_OVERVIEW}-by', 'value'),
    prevent_initial_call=True,
)
def display_graph_applications_steps_decline(from_, to_, by_):
    """ Generate the chart displaying applications/steps/decline over time period/scale
    """
    fig = go.Figure()

    (
        tickformat, dtick,
        type_, category_order, category_array,
        range_
    ) = generate_chart_params(from_, to_, by_=by_)

    applications_applied = ApplicationHelper.get_total_by_application_date(from_=from_, to_=to_)
    applications_applied = pd.DataFrame(applications_applied, columns=['date', 'total'])
    applications_applied = generate_chart_data(df=applications_applied, by_=by_)
    fig.add_trace(
        go.Bar(name="Applied", x=applications_applied["date"], y=applications_applied["total"], marker_color='#7950f2'),
    )

    applications_steps = ApplicationStepHelper.get_total_by_scheduled_date(from_=from_, to_=to_)
    applications_steps = pd.DataFrame(applications_steps, columns=['date', 'total'])
    applications_steps = generate_chart_data(df=applications_steps, by_=by_)
    fig.add_trace(
        go.Bar(name="Step", x=applications_steps["date"], y=applications_steps["total"], marker_color='#228be6'),
    )

    applications_declined = ApplicationHelper.get_total_by_decline_date(from_=from_, to_=to_)
    applications_declined = pd.DataFrame(applications_declined, columns=['date', 'total'])
    applications_declined = generate_chart_data(df=applications_declined, by_=by_)
    fig.add_trace(
        go.Bar(name="Declined", x=applications_declined["date"], y=applications_declined["total"], marker_color='#fa5252'),
    )

    fig.update_layout(
        xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(82, 82, 82)',
            linewidth=1,
            ticks='outside',
            tickfont=dict(
                size=12,
                color='rgb(82, 82, 82)',
            ),
            tickformat=tickformat,
            dtick=dtick,
            type=type_,
            categoryorder=category_order,
            categoryarray=category_array,
            range=range_
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        ),
        # autosize=False,
        margin=dict(
            autoexpand=False,
            l=25,
            r=0,
            t=25,
            b=25
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        showlegend=True,
        plot_bgcolor='white',
        barmode='stack',
        height=240
    )

    return fig