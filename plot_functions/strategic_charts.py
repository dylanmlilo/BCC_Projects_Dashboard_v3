import pandas as pd
import plotly
import plotly.express as px
import json
from models.strategic import StrategicTask


def plot_strategic_tasks_by_manager():
    task_data = StrategicTask.strategic_tasks_to_dict_list()
    df = pd.DataFrame(task_data)

    bg_colors = ['rgba(0, 0, 0, 0.1)', 'rgba(47, 182, 182, 0.2)']
    color_index = 0

    df['percentage_done'] = df['percentage_done'].fillna(0).astype(float)
    color_map = {
        "Not Started": "#6C757D",
        "Overdue": "#DC3545",
        "Complete": "#198754",
        "In Progress": "#0D6EFD"
    }

    managers = df['project_manager'].unique()
    charts = []

    for manager in managers:
        manager_df = df[df['project_manager'] == manager]

        # Conditionally truncate long task names and set hover text for all tasks
        manager_df['display_task'] = manager_df['task'].apply(lambda x: x if len(x) <= 15 else x[:15] + '...')
        manager_df['hover_text'] = manager_df['task']  # Full task name for hover

        fig = px.bar(
            manager_df,
            x="display_task",  # Use conditionally shortened task names
            y="percentage_done",
            color="status",
            title=f"Strategic Planning Tasks for {manager}",
            color_discrete_map=color_map,
            hover_name="hover_text"  # Full task name in hover tooltip
        )

        fig.update_layout(
            legend_title="Status",
            bargap=0.8,
            title={
                'text': f"Strategic Planning Tasks for {manager}",
                'x': 0.5,
                'y': 0.9,
                'font': {
                    'size': 20,
                    'family': 'Arial'
                }
            },
            xaxis_title_text="Tasks",
            yaxis_title_text="Percentage Done",
            xaxis_title_font_size=17,
            yaxis_title_font_size=17,
            legend_title_font={'size': 16},
            paper_bgcolor=bg_colors[color_index],
            xaxis_tickangle=-45  # Rotate task names for readability
        )

        color_index = (color_index + 1) % len(bg_colors)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        charts.append(graphJSON)

    return charts
