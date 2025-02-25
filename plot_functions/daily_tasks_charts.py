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


def plot_daily_tasks_gauge_chart():
    """
    Generates gauge charts for daily tasks.

    Returns:
    gauges (list): A list of Plotly gauge charts for each task.
    """
    # Get daily tasks for the latest week ending
    tasks_data, latest_week_ending = DailyTask.get_latest_week_tasks()

    # Convert to DataFrame
    df = pd.DataFrame(tasks_data)

    if df.empty:
        return []  # Return empty list if no data is available

    # Create a gauge chart for each task
    gauges = []
    for _, row in df.iterrows():
        task_name = row["task"]
        number_done = row["number_done"]
        responsible_person = row["responsible_person"]

        # Create a gauge chart
        gauge = go.Indicator(
            mode="gauge+number",
            value=number_done,
            title={"text": f"{task_name}<br><span style='font-size:0.8em;color:gray'>{responsible_person}</span>"},
            gauge={
                "axis": {"range": [None, 10]},  # Adjust range based on your data
                "bar": {"color": "blue"},
                "steps": [
                    {"range": [0, 5], "color": "lightgray"},
                    {"range": [5, 8], "color": "gray"},
                    {"range": [8, 10], "color": "darkgray"}
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": number_done
                }
            }
        )
        gauges.append(gauge)
        gauge_charts_json = json.dumps(gauges, cls=plotly.utils.PlotlyJSONEncoder)

    return gauge_charts_json