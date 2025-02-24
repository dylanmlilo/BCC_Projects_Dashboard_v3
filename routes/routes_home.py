from flask import Blueprint, render_template
from flask_login import login_required
from models.date import today_date
from models.projects import ProjectsData
from plot_functions.home_page_charts import plot_home_page_charts


home_bp = Blueprint('home', __name__)


@home_bp.route("/home", strict_slashes=False)
@login_required
def index():
    projects_data = ProjectsData.projects_data_to_dict_list()
    graph1JSON, graph2JSON, graph3JSON, graph4JSON, graph5JSON, graph6JSON = plot_home_page_charts()
    formatted_date = today_date()
    return render_template("home.html", graph1JSON=graph1JSON,
                                        today_date=formatted_date, 
                                        graph2JSON=graph2JSON, graph3JSON=graph3JSON,
                                        graph4JSON=graph4JSON, projects_data=projects_data,
                                        graph5JSON=graph5JSON, graph6JSON=graph6JSON)