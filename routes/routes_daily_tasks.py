from flask import Blueprint, render_template
from flask_cors import CORS
from flask_login import login_required
from models.daily_tasks import DailyTask
from models.date import today_date
from plot_functions.daily_tasks_charts import plot_daily_tasks_chart, plot_daily_tasks_gauge_chart
import json


daily_tasks_bp = Blueprint('daily_task', __name__)
CORS(daily_tasks_bp)


@daily_tasks_bp.route("/daily_tasks", strict_slashes=False)
@login_required
def daily_tasks():
    tasks_data, latest_week_ending = DailyTask.get_latest_week_tasks()
    daily_tasks_graphJSON, formatted_week_ending = plot_daily_tasks_chart()
    # gauge_charts_graphJSON = json.dumps(plot_daily_tasks_gauge_chart())
    formatted_date = today_date()
    return render_template("daily_tasks.html", tasks_data=tasks_data,
                                        latest_week_ending=latest_week_ending,
                                        today_date=formatted_date,
                                        daily_tasks_graphJSON=daily_tasks_graphJSON,
                                        formatted_week_ending=formatted_week_ending)
