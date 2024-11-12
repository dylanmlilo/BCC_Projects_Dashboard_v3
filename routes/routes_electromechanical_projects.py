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


electromechanical_projects_bp = Blueprint('electromechahical_projects', __name__)


@electromechanical_projects_bp.route("/electromechanical_projects", strict_slashes=False)
@login_required
def electromechanical_projects():
    """
    Function to handle electromechahical projects data retrieval and rendering.

    Retrieves electromechahical projects data and today's date, then
    renders the electromechahical_projects.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "electromechahical_projects.html" with today's
    date and electromechahical projects data.

    """
    electromechanical_projects_data = ProjectsData.projects_data_to_dict_list(section_id=5)
    electromechanical_projects_charts_JSON = plot_projects_by_manager_for_section(section_id=5)
    formatted_date = today_date()
    return render_template("electromechanical_projects.html", today_date=formatted_date,
                           electromechanical_projects_data=electromechanical_projects_data,
                           electromechanical_projects_charts_JSON=electromechanical_projects_charts_JSON)


@electromechanical_projects_bp.route("/electromechanical_projects_data", strict_slashes=False)
@login_required
@required_roles('admin', 'admin_electromechanical')
def electromechanical_projects_data():
    """
    Function to handle electromechahical projects data retrieval and rendering.

    Retrieves electromechahical projects data and today's date, then
    renders the electromechahical_projects_data.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "electromechahical_projects_data.html" with today's
    date and electromechahical projects data.

    """
    electromechanical_projects_data = ProjectsData.projects_data_to_dict_list(section_id=5)
    project_managers = (
    ProjectManagers.project_managers_to_dict_list("Electromechanical")
    )
    sections = Section.section_data_to_dict_list()
    formatted_date = today_date()
    return render_template("electromechanical_projects_data.html", today_date=formatted_date,
                           electromechanical_projects_data=electromechanical_projects_data,
                           sections=sections, project_managers=project_managers)