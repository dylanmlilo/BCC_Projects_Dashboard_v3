import json
import plotly
import plotly_express as px
from models.projects import ContractType


def plot_servicing_page_charts():
    """
    Generates a list of JSON representations of bar charts
    displaying project progress with colors.

    Returns:
        list: A list of JSON strings representing the Plotly charts,
        one for each project.
    """

    servicing_data = ContractType.contract_type_data_dict(1)
    servicing_charts = []

    if not servicing_data:
        return servicing_charts

    bg_colors = ['rgba(0, 0, 0, 0.1)', 'rgba(47, 182, 182, 0.2)']
    color_index = 0

    for project_data in servicing_data:
        contract_name = project_data.get("contract_name")
        contractor = project_data.get("contractor")
        link = project_data.get("link")
        progress_data = {
          "Progress Type": [
            "Water", "Sewer", "Roads", "Storm Drainage",
            "Public Lighting", "Total Progress"
          ],
          "Progress Percentage": [
            project_data["water_progress"],
            project_data["sewer_progress"],
            project_data["roads_progress"],
            project_data["storm_drainage_progress"],
            project_data["public_lighting_progress"],
            project_data["physical_progress_percentage"]
          ]
        }

        color_list = ['royalblue', 'goldenrod', 'grey',
                      'green', 'orange', 'red']

        fig = px.bar(progress_data, x="Progress Type", y="Progress Percentage",
                     title=contract_name, color=progress_data["Progress Type"],
                     color_discrete_sequence=color_list)
        fig.update_layout(
          legend_title="Progress Type",
          bargap=0.6,
          title={
            'text': contract_name,
            'x': 0.5,
            'y': 0.9,
            'font': {
              'size': 20,
              'family': 'Arial'
            }
          },
          xaxis_title_text=(
            "Contractor - {} -- <a href='{}'>Link to Google Drive Folder</a>"
            .format(contractor, link)
          ),
          yaxis_title_text="Progress Percentage(%)",
          xaxis_title_font_size=17,
          yaxis_title_font_size=17,
          legend_title_font={'size': 16},
          paper_bgcolor=bg_colors[color_index]
        )

        color_index = (color_index + 1) % len(bg_colors)

        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        servicing_charts.append(graphJSON)

    return servicing_charts
