import pandas as pd
import json
import plotly
import plotly_express as px
import plotly.graph_objects as go
from models.daily_tasks import DailyTask


def plot_daily_tasks_chart():
    """
    Generates a JSON representation of the Daily Tasks bar chart.

    Returns:
    graphJSON (str): JSON representation of the daily tasks bar chart.
    """
    # Get daily tasks for the latest week ending
    tasks_data, latest_week_ending = DailyTask.get_latest_week_tasks()

    # Convert to DataFrame
    df = pd.DataFrame(tasks_data)

    if df.empty:
        return json.dumps(None)  # Return empty if no data is available

    # Create a bar chart
    fig = px.bar(
        df,
        x="task",
        y="number_done",
        color="responsible_person",
        title=f"Daily Tasks Completed (Week Ending {latest_week_ending})",
        hover_data={"task": True, "number_done": True, "responsible_person": True}
    )

    # Update layout
    fig.update_layout(
        legend_title_text='Responsible Person',
        title={'x': 0.5, 'y': 0.93, 'font': {'size': 22, 'family': 'Arial'}},
        xaxis_title_text="Task",
        yaxis_title_text="Number Completed",
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        legend_title_font={'size': 14},
        margin=dict(r=50, l=90, t=70, b=50),
        paper_bgcolor='rgba(0, 0, 0, 0.1)'
    )

    # Convert to JSON for Flask rendering
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON, latest_week_ending