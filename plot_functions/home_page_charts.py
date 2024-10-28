from flask import abort
import pandas as pd
import json
import plotly
import plotly_express as px
import plotly.graph_objects as go
from models.projects import ProjectsData


def plot_home_page_charts():
    """
    Generates and returns JSON representations of
    various plots for projects data

    Returns:
    graph1JSON (str): JSON representation of the physical progress plot.
    graph2JSON (str): JSON representation of the reservoir levels plot.
    """
    projects_data = ProjectsData.projects_data_to_dict_list()
    df = pd.DataFrame(projects_data)

    df_filtered_fig1 = df[df['physical_progress_percentage'].notnull()]

    fig1 = px.bar(
        df_filtered_fig1,
        x='contract_number',
        y='physical_progress_percentage',
        color='project_manager',
        title="Physical Progress of Works",
        hover_data={
            'contract_name': True,  # Display full contract name with default label
            'physical_progress_percentage': ':.2f',  # Show two decimal places
            'project_manager': True  # Include project manager name without header
        }
    )
    fig1.update_layout(
        legend_title_text='Project Managers',
        title={'x': 0.5, 'y': 0.93, 'font': {'size': 25, 'family': 'Arial'}},
        xaxis_title_text="Contract Number",
        yaxis_title_text="Physical Progress (%)",
        xaxis_title_font_size=17,
        yaxis_title_font_size=17,
        legend_title_font={'size': 16},
        margin=dict(r=50, l=90, t=80, b=50),
        paper_bgcolor='rgba(0, 0, 0, 0.1)'
    )


    df_filtered_fig2 = df[df['financial_progress_percentage'].notnull()]

    fig2 = px.bar(
        df_filtered_fig2,
        x='contract_number',
        y='financial_progress_percentage',
        color='contract_type',
        title="Financial Progress of Works",
        hover_data={'contract_name': True}
    )
    fig2.update_layout(
        legend_title_text='Contract Type',
        title={'x': 0.5, 'y': 0.93, 'font': {'size': 25, 'family': 'Arial'}},
        xaxis_title_text="Contract Number",
        yaxis_title_text="Financial Progress (%)",
        xaxis_title_font_size=17,
        yaxis_title_font_size=17,
        legend_title_font={'size': 16},
        margin=dict(r=50, l=90, t=80, b=50),
        paper_bgcolor='rgba(47, 182, 182, 0.2)'
    )

    projects_by_year = (
      df.groupby("year")
      .size()
      .reset_index(name="number_of_projects")
      )

    fig3 = px.pie(projects_by_year, values='number_of_projects', names='year',
                  title='Distribution of Projects by Year')

    fig3.update_layout(
      title={
          'x': 0.5,
          'y': 0.95,
          'font': {
              'size': 25,
              'family': 'Arial'
          }
      },
      margin=dict(t=60, b=20),
      paper_bgcolor='rgba(47, 182, 182, 0.2)'
      )

    projects_by_status = (
      df.groupby('project_status')
      .size().reset_index(name='number_of_projects')
      )

    color_map = {
        'Completed': '#109618',
        'Stopped': '#FB0D0D',
        'In Progress': '#00A08B',
        'Retendered': 'orange',
        'Yet to start': 'rgb(255, 166, 71)'
    }

    fig4 = px.treemap(projects_by_status,
                      path=['project_status'],
                      values='number_of_projects',
                      color='project_status',
                      color_discrete_map=color_map,
                      title='Distribution of Projects by Status')

    fig4.update_layout(
      title={
          'x': 0.5,
          'y': 0.93,
          'font': {
              'size': 22.5,
              'family': 'Arial'
          }
      },
      margin=dict(r=5, l=5, t=60, b=60),
      paper_bgcolor='rgba(0, 0, 0, 0.1)'
      )

    projects_by_manager = df['project_manager'].value_counts().reset_index()
    projects_by_manager.columns = ['project_manager', 'number_of_projects']

    fig5 = px.sunburst(projects_by_manager, path=['project_manager'],
                       values='number_of_projects',
                       title='Distribution of Projects by Project Managers')

    fig5.update_layout(
      title={
          'x': 0.5,
          'y': 0.95,
          'font': {
              'size': 22,
              'family': 'Arial'
          }
      },
      margin=dict(t=60, b=20),
      paper_bgcolor='rgba(47, 182, 182, 0.2)'
      )
    
    # List to store JSON data for each section chart
    section_chart_json_list = []
    bg_colors = ['rgba(0, 0, 0, 0.1)', 'rgba(47, 182, 182, 0.2)']
    color_index = 0

    for section in df['section'].unique():
        # Filter the data for the section and build the chart
        df_section = df[(df['section'] == section) & df['physical_progress_percentage'].notnull()]
        fig = px.scatter(
            df_section,
            x='contract_number',
            y='physical_progress_percentage',
            color='project_manager',
            title=f"{section} Section Projects",
            hover_data={
                'contract_name': True,               # Display full contract name with default label
                'physical_progress_percentage': ':.2f',  # Show two decimal places
                'project_manager': True              # Include project manager name without header
            }
        )

        # Adjust size of the scatter dots
        fig.update_traces(marker=dict(size=10))

        # Apply consistent layout styling and set alternating background color
        fig.update_layout(
            legend_title_text='Project Managers',
            title={'x': 0.5, 'y': 0.93, 'font': {'size': 25, 'family': 'Arial'}},
            xaxis_title_text="Contract Number",
            yaxis_title_text="Project Progress (%)",
            xaxis_title_font_size=17,
            yaxis_title_font_size=17,
            legend_title_font={'size': 16},
            margin=dict(r=50, l=90, t=80, b=50),
            paper_bgcolor=bg_colors[color_index]  # Set alternating background color
        )

        # Toggle color index for the next chart
        color_index = (color_index + 1) % len(bg_colors)

        # Convert Plotly figure to JSON for JavaScript parsing
        section_chart_json_list.append(json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder))



    graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    graph5JSON = json.dumps(fig5, cls=plotly.utils.PlotlyJSONEncoder)

    return graph1JSON, graph2JSON, graph3JSON, graph4JSON, graph5JSON, section_chart_json_list