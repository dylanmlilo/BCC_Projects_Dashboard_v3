from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_cors import CORS
from flask_login import login_required
from models.decorators import required_roles
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
    formatted_date = today_date()
    return render_template("daily_tasks.html", tasks_data=tasks_data,
                                        latest_week_ending=latest_week_ending,
                                        today_date=formatted_date,
                                        daily_tasks_graphJSON=daily_tasks_graphJSON,
                                        formatted_week_ending=formatted_week_ending,)


@daily_tasks_bp.route("/daily_tasks_data", strict_slashes=False)
@login_required
@required_roles("admin", "admin_daily_tasks")
def daily_tasks_data():
    all_tasks_data = DailyTask.get_all_tasks_to_dict_list()
    existing_fridays = DailyTask.get_weekending_dates()
    formatted_date = today_date()
    return render_template("daily_tasks_data.html", all_tasks_data=all_tasks_data,
                                        today_date=formatted_date,
                                        existing_fridays=existing_fridays)


@daily_tasks_bp.route("/insert_daily_task", methods=["POST"])
@login_required
@required_roles("admin", "admin_daily_tasks")
def insert_daily_task():
    try:
        task_name = request.form.get("task")
        number_done = int(request.form.get("number_done"))
        user_date = datetime.strptime(request.form.get("week_ending"), "%Y-%m-%d").date()
        responsible_person = request.form.get("responsible_person")
        section = request.form.get("section")

        # Validate that the date is actually a Friday
        if user_date.weekday() != 4:  # 4 means Friday
            flash("Invalid date! Only Fridays are allowed.", "error")
            return redirect(url_for("daily_tasks.daily_tasks_data"))

        new_task = DailyTask(
            task=task_name,
            number_done=number_done,
            week_ending=user_date,
            responsible_person=responsible_person,
            section=section
        )

        session.add(new_task)
        session.commit()
        flash("Task added successfully!", "success")

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        session.rollback()
    
    finally:
        session.close()

    return redirect(url_for("daily_tasks.daily_tasks_data"))


@daily_tasks_bp.route("/update_daily_task/<int:daily_task_id>", methods=["POST"])
@login_required
@required_roles("admin", "admin_daily_tasks")
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
@required_roles("admin", "admin_daily_tasks")
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
