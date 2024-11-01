from flask import Blueprint, render_template
from flask_login import login_required
from models.projects import ProjectsData
from models.date import today_date
from plot_functions.servicing_page_charts import plot_servicing_page_charts


contract_type_bp = Blueprint('sections', __name__)


@contract_type_bp.route("/Servicing", strict_slashes=False)
@login_required
def servicing():
    """
    Renders the 'servicing.html' template with project
    data for servicing contracts.

    This function fetches project data for servicing contracts,
    generates a bar chart,
    and renders the 'servicing.html' template with the necessary data.

    Returns:
        Flask.Response: The rendered template.
    """
    projects_data = ProjectsData.projects_data_to_dict_list(contract_type_id=1)
    servicing_data_JSON = plot_servicing_page_charts()
    formatted_date = today_date()
    return render_template("servicing.html", projects_data=projects_data,
                           today_date=formatted_date,
                           servicing_data_JSON=servicing_data_JSON)


@contract_type_bp.route("/Goods", strict_slashes=True)
@login_required
def goods():
    """
    Function to handle /Goods route.

    Retrieves projects data and today's date,
    then renders the goods.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "goods.html" with today's date and projects data.

    """
    projects_data = ProjectsData.projects_data_to_dict_list(contract_type_id=3)
    formatted_date = today_date()
    return render_template("goods.html", today_date=formatted_date,
                           projects_data=projects_data)


@contract_type_bp.route("/Works", strict_slashes=False)
@login_required
def works():
    """
    Function to handle works data retrieval and rendering.

    Retrieves projects data and today's date,
    then renders the works.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "works.html" with today's date and projects data.
    """
    projects_data = ProjectsData.projects_data_to_dict_list(contract_type_id=4)
    formatted_date = today_date()
    return render_template("works.html", today_date=formatted_date,
                           projects_data=projects_data)


@contract_type_bp.route("/Services", strict_slashes=False)
@login_required
def services():
    """
    Function to handle Services route.

    Retrieves projects data and today's date,
    then renders the services.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "services.html" with today's date and projects data.

    """
    projects_data = ProjectsData.projects_data_to_dict_list(contract_type_id=2)
    formatted_date = today_date()
    return render_template("services.html", today_date=formatted_date,
                           projects_data=projects_data)
