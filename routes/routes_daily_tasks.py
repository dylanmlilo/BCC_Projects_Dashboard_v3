from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_cors import CORS
from flask_login import login_required
from models.daily_tasks import DailyTask
from models.engine.database import session
from models.date import today_date
from decimal import Decimal
from datetime import datetime
from plot_functions.daily_tasks_charts import plot_daily_tasks_chart


daily_tasks_bp = Blueprint('daily_tasks', __name__)
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


@daily_tasks_bp.route("/daily_tasks_data", strict_slashes=False)
@login_required
def daily_tasks_data():
    tasks_data, latest_week_ending = DailyTask.get_latest_week_tasks()
    daily_tasks_graphJSON, formatted_week_ending = plot_daily_tasks_chart()
    formatted_date = today_date()
    return render_template("daily_tasks_data.html", tasks_data=tasks_data,
                                        latest_week_ending=latest_week_ending,
                                        today_date=formatted_date,
                                        daily_tasks_graphJSON=daily_tasks_graphJSON,
                                        formatted_week_ending=formatted_week_ending)

@daily_tasks_bp.route("/insert_daily_task", methods=["POST"])
@login_required
def insert_daily_task():
    if request.method == "POST":
        try:
            new_task = DailyTask(
                task = request.form.get("task"),
                number_done = Decimal(request.form.get("number_done")),
                week_ending = datetime.strptime(request.form.get("week_ending"), "%Y-%m-%d").date(),
                responsible_person = request.form.get("responsible_person"),
                section = request.form.get("section")
            )

            session.add(new_task)
            session.commit()
            flash('Strategic task added successfully!', 'success')
            return redirect(url_for("daily_tasks.daily_tasks_data"))
        
        except Exception as e:
            flash(f'An error occurred while adding the task: {str(e)}', 'error')
            session.rollback()
            return redirect(url_for("daily_tasks.daily_tasks_data"))
        
        finally:
            session.close()

    return redirect(url_for("daily_tasks.daily_tasks_data"))


@daily_tasks_bp.route("/update_daily_task/int:daily_task_id", methods=["POST"])
@login_required
def update_daily_task(daily_task_id):
    try:
        task =  session.query(DailyTask).filter_by(id=daily_task_id).first()
        if task:
            task.task = request.form.get("task")
            task.number_done = Decimal(request.form.get("number_done"))
            task.week_ending = datetime.strptime(request.form.get("week_ending"), "%Y-%m-%d").date()
            task.responsible_person = request.form.get("responsible_person")
            task.section = request.form.get("section")

            session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('daily_tasks.daily_tasks_data'))
        
        else:
            flash('Task not found.', 'error')
            return redirect(url_for('daily_tasks.daily_tasks_data'))
    
    except Exception as e:
        flash(f'An error occurred while updating the task: {str(e)}', 'error')
        session.rollback()
        return redirect(url_for('daily_tasks.daily_tasks_data'))
    
    finally:
        session.close()


@daily_tasks_bp.route("/delete_daily_task/<int:daily_task_id>")
@login_required
def delete_daily_task(daily_task_id):
    try:
        task = session.query(DailyTask).filter_by(id=daily_task_id).first()
        if task:
            session.delete(task)
            session.commit()
            flash('Task deleted successfully!', 'success')
        else:
            flash('Task not found.', 'error')

        return redirect(url_for('daily_tasks.daily_tasks_data'))

    except Exception as e:
        flash(f'An error occurred while deleting the task: {str(e)}', 'error')
        session.rollback()
        return redirect(url_for('daily_tasks.daily_tasks_data'))
    
    finally:
        session.close()
