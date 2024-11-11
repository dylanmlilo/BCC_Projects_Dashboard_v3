from flask import (
    Blueprint, render_template
)
from flask_login import login_required
from models.date import today_date
from models.projects import (
    ProjectsData, ProjectManagers, Section
)
from models.decorators import required_roles


sanitation_projects_bp = Blueprint('sanitation_projects', __name__)


@sanitation_projects_bp.route("/sanitation_projects_data", strict_slashes=False)
@login_required
@required_roles('admin', 'admin_sanitation')
def saniation_projects_data():
    """
    Function to handle sanitation projects data retrieval and rendering.

    Retrieves sanitation projects data and today's date, then
    renders the sanitation_projects_data.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "sanitation_projects_data.html" with today's
    date and sanitation projects data.

    """
    sanitation_projects_data = ProjectsData.projects_data_to_dict_list(section_id=3)
    project_managers = (
    ProjectManagers.project_managers_to_dict_list("Sanitation")
    )
    sections = Section.section_data_to_dict_list()
    formatted_date = today_date()
    return render_template("sanitation_projects_data.html", today_date=formatted_date,
                           sanitation_projects_data=sanitation_projects_data,
                           sections=sections, project_managers=project_managers)