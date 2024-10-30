import pandas as pd
import json
import plotly
import plotly_express as px
from models.gis import gis_data_to_dict_list


def plot_gis_task_by_output():
    task_data = gis_data_to_dict_list()
    df = pd.DataFrame(task_data)

    df['percentage_of_activity'] = df['percentage_of_activity'].fillna(0)
    output_names = df['output_name'].unique()
    charts = []

    bg_colors = ['rgba(0, 0, 0, 0.1)', 'rgba(47, 182, 182, 0.2)']
    color_index = 0

    color_map = {
        "Not Started": "rgba(72, 203, 243, 0.9)",
        "Overdue": "rgba(255, 0, 0, 0.9)",
        "Complete": "rgba(10, 141, 10, 0.9)",
        "In Progress": "rgba(154, 205, 50, 0.9)"
    }

    for output_name in output_names:
        output_df = df[df['output_name'] == output_name]

        responsible_person = output_df['responsible_person'].iloc[0] if not output_df['responsible_person'].isnull().all() else "Unknown"
        title_text = f"{output_name} - Responsible Person: {responsible_person}"

        # Conditionally truncate long task descriptions
        output_df['display_task'] = output_df['task_description'].apply(
            lambda x: x if x is not None and len(x) <= 15 else (x[:15] + '...' if x else 'No description')
        )
        output_df['hover_text'] = output_df['task_description'].fillna('No description')  # Full description or default text for hover


        # Create a bar chart with custom colors based on task status
        fig = px.bar(
            output_df,
            x="display_task",  # Use truncated descriptions
            y="percentage_of_activity",
            color="task_status",
            title=title_text,
            color_discrete_map=color_map,
            hover_name="hover_text"  # Full task description in hover tooltip
        )

        fig.update_layout(
            legend_title="Status",
            bargap=0.6,
            title={
                'text': title_text,
                'x': 0.5,
                'y': 0.9,
                'font': {
                    'size': 20,
                    'family': 'Arial'
                }
            },
            xaxis_title_text="Tasks",
            yaxis_title_text="Percentage Progress (%)",
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
