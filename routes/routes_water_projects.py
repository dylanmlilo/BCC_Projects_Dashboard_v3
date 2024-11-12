from flask import (
    Blueprint, render_template
)
from flask_login import login_required
from models.date import today_date
from models.projects import (
    ProjectsData, ProjectManagers, Section
)
from models.decorators import required_roles
from plot_functions.sections_page_charts import plot_projects_by_manager_for_section


water_projects_bp = Blueprint('water_projects', __name__)


@water_projects_bp.route("/water_projects", strict_slashes=False)
@login_required
def water_projects():
    """
    Function to handle water projects data retrieval and rendering.

    Retrieves water projects data and today's date, then
    renders the water_projects.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "water_projects.html" with today's
    date and water projects data.

    """
    water_projects_data = ProjectsData.projects_data_to_dict_list(section_id=2)
    water_projects_charts_JSON = plot_projects_by_manager_for_section(section_id=2)
    formatted_date = today_date()
    return render_template("water_projects.html", today_date=formatted_date,
                           water_projects_data=water_projects_data,
                           water_projects_charts_JSON=water_projects_charts_JSON)


@water_projects_bp.route("/water_projects_data", strict_slashes=False)
@login_required
@required_roles('admin', 'admin_water')
def water_projects_data():
    """
    Function to handle water projects data retrieval and rendering.

    Retrieves water projects data and today's date, then
    renders the water_projects_data.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "water_projects_data.html" with today's
    date and water projects data.

    """
    water_projects_data = ProjectsData.projects_data_to_dict_list(section_id=2)
    project_managers = (
    ProjectManagers.project_managers_to_dict_list("Water")
    )
    formatted_date = today_date()
    return render_template("water_projects_data.html", today_date=formatted_date,
                           water_projects_data=water_projects_data,
                           project_managers=project_managers)