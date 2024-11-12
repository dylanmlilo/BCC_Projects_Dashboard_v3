import pandas as pd
import plotly
import plotly.express as px
import json
from models.projects import ProjectsData

def plot_projects_by_manager_for_section(section_id=None, section_name=None):
    """
    Plots bar charts showing each project manager's projects for a given section, colored by project status.

    Args:
        section_id (int, optional): The ID of the section to filter projects by.
        section_name (str, optional): The name of the section to filter projects by.

    Returns:
        tuple: A tuple containing a list of JSON strings representing the Plotly bar charts 
               and a list of unique project managers for the specified section.
    """
    # Retrieve projects based on section_id or section_name
    if section_id is not None:
        project_data = ProjectsData.projects_data_to_dict_list(section_id=section_id)
    elif section_name is not None:
        project_data = ProjectsData.projects_data_to_dict_list(section_name=section_name)
    else:
        raise ValueError("Either section_id or section_name must be provided.")

    df = pd.DataFrame(project_data)

    # Filter for projects with non-null project managers
    df = df.dropna(subset=["project_manager"])

    bg_colors = ['rgba(0, 0, 0, 0.1)', 'rgba(47, 182, 182, 0.2)']
    color_index = 0

    # Define color map for project status
    color_map = {
        "Yet to start": "rgba(72, 203, 243, 0.9)",
        "Stopped": "rgba(255, 0, 0, 0.9)",
        "Completed": "rgba(10, 141, 10, 0.9)",
        "In Progress": "rgba(154, 205, 50, 0.9)",
        "Retendered": "rgba(255, 165, 0, 0.9)"
    }

    # Sort by project manager for grouped charts
    df = df.sort_values(by='project_manager')

    managers = df['project_manager'].unique()
    charts = []

    for manager in managers:
        manager_df = df[df['project_manager'] == manager]

        # Conditionally truncate long contract names and set hover text
        manager_df['display_contract'] = manager_df['contract_name'].apply(
            lambda x: x if len(x) <= 15 else x[:15] + '...')
        manager_df['hover_text'] = manager_df['contract_name']

        fig = px.bar(
            manager_df,
            x="display_contract",
            y="physical_progress_percentage",
            color="project_status",
            title=f"Project Manager: {manager}",
            color_discrete_map=color_map,
            hover_name="hover_text"
        )

        fig.update_layout(
            legend_title_text="Project Status",
            bargap=0.9,
            title={
                'text': f"Project Manager: {manager}",
                'x': 0.5,
                'y': 0.9,
                'font': {
                    'size': 20,
                    'family': 'Arial'
                }
            },
            xaxis_title_text="Contract Name",
            yaxis_title_text="Physical Progress (%)",
            xaxis_title_font_size=17,
            yaxis_title_font_size=17,
            paper_bgcolor=bg_colors[color_index],
            xaxis_tickangle=-45
        )

        color_index = (color_index + 1) % len(bg_colors)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        charts.append(graphJSON)

    return charts
