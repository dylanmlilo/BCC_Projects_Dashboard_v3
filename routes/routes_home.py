from flask import Blueprint, render_template, request
from flask_login import login_required
from models.date import today_date
from models.projects import ProjectsData
from models.daily_tasks import DailyTask
from plot_functions.home_page_charts import plot_home_page_charts, plot_daily_tasks_chart


home_bp = Blueprint('home', __name__)


@home_bp.route("/home", strict_slashes=False)
@login_required
def index():
    tasks_data, latest_week_ending = DailyTask.get_latest_week_tasks()
    projects_data = ProjectsData.projects_data_to_dict_list()
    graph1JSON, graph2JSON, graph3JSON, graph4JSON, graph5JSON, graph6JSON = plot_home_page_charts()
    daily_tasks_graphJSON, formatted_week_ending = plot_daily_tasks_chart()
    formatted_date = today_date()
    return render_template("home.html", graph1JSON=graph1JSON, tasks_data=tasks_data,
                                        latest_week_ending=latest_week_ending,
                                        today_date=formatted_date, 
                                        graph2JSON=graph2JSON, graph3JSON=graph3JSON,
                                        graph4JSON=graph4JSON, projects_data=projects_data,
                                        graph5JSON=graph5JSON, graph6JSON=graph6JSON,
                                        daily_tasks_graphJSON=daily_tasks_graphJSON,
                                        formatted_week_ending=formatted_week_ending)