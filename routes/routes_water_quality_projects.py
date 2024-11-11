from flask import (
    Blueprint, render_template
)
from flask_login import login_required
from models.date import today_date
from models.projects import (
    ProjectsData, ProjectManagers, Section
)
from models.decorators import required_roles


water_quality_projects_bp = Blueprint('water_quality_projects', __name__)


@water_quality_projects_bp.route("/water_quality_projects_data", strict_slashes=False)
@login_required
@required_roles('admin', 'admin_water_quality')
def water_projects_data():
    """
    Function to handle water quality projects data retrieval and rendering.

    Retrieves water quality projects data and today's date, then
    renders the water_quality_projects_data.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "water_quality_projects_data.html" with today's
    date and water quality projects data.

    """
    water_quality_projects_data = ProjectsData.projects_data_to_dict_list(section_id=2)
    project_managers = (
    ProjectManagers.project_managers_to_dict_list("Water Quality")
    )
    sections = Section.section_data_to_dict_list()
    formatted_date = today_date()
    return render_template("water_quality_projects_data.html", today_date=formatted_date,
                           water_quality_projects_data=water_quality_projects_data,
                           sections=sections, project_managers=project_managers)