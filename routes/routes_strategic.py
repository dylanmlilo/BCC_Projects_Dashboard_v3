from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, jsonify
    )
from flask_login import login_required
from decimal import Decimal
from models.date import today_date
from models.engine.database import session
from models.strategic import StrategicTask
from models.projects import ProjectManagers
from models.decorators import required_roles
from plot_functions.strategic_charts import plot_strategic_tasks_by_manager


strategic_bp = Blueprint('strategic', __name__)


@strategic_bp.route("/StrategicPlanning", strict_slashes=False)
@login_required
def strategic_planning():
    """
    Function to handle Strategic Planning route.

    Retrieves strategic data list and today's date,
    then renders the strategic_planning.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "strategic_planning.html"
    with today's date and strategic data list.

    """
    strategic_data_list = StrategicTask.strategic_tasks_to_dict_list()
    strategic_data_JSON = plot_strategic_tasks_by_manager()
    formatted_date = today_date()
    return render_template("strategic_planning.html",
                           today_date=formatted_date,
                           strategic_data_list=strategic_data_list,
                           strategic_data_JSON=strategic_data_JSON)


@strategic_bp.route("/strategic_planning_data", strict_slashes=False)
@login_required
@required_roles('admin', 'admin_struts')
def strategic_planning_data():
    """
    Function to handle Strategic Planning data route.

    Retrieves strategic data list and renders
    the strategic_planning.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "strategic_planning.html" with strategic data list.
    """
    formatted_date = today_date()
    strategic_data_list = StrategicTask.strategic_tasks_to_dict_list()
    project_managers = (
        ProjectManagers.project_managers_to_dict_list("strategic planning")
        )
    return render_template("strategic_planning_data.html",
                           strategic_data_list=strategic_data_list,
                           today_date=formatted_date,
                           project_managers=project_managers)


@strategic_bp.route("/insert_strategic_data", methods=['POST'])
@login_required
@required_roles('admin', 'admin_struts')
def insert_strategic_data():
    """
    Function to handle insertion of strategic data.

    Parameters:
    - None

    Returns:
    - Redirect to "strategic_planning_data" with success or error message.
    """
    if request.method == 'POST':
        try:
            new_task = StrategicTask(
                task=request.form.get('task'),
                description=request.form.get('description') or None,
                deliverables=request.form.get('deliverables') or None,
                assigned_to=request.form.get('assigned_to'),
                deadline=request.form.get('deadline') or None,
                status=request.form.get('status'),
                priority=request.form.get('priority'),
                percentage_done=(Decimal(request.form.get('percentage_done'))
                                    if request.form.get('percentage_done') else None),
                fixed_cost=(Decimal(request.form.get('fixed_cost'))
                            if request.form.get('fixed_cost') else None),
                estimated_hours=(Decimal(request.form.get('estimated_cost'))
                                    if request.form.get('estimated_cost') else None),
                actual_hours=(Decimal(request.form.get('actual_cost'))
                                if request.form.get('actual_cost') else None),
                link=request.form.get('link') or None
            )
            
            session.add(new_task)
            session.commit()
            flash('Strategic task added successfully!', 'success')
            return redirect(url_for('strategic.strategic_planning_data'))

        except Exception as e:
            flash(f'An error occurred while adding the task: {str(e)}', 'error')
            session.rollback()
            return redirect(url_for('strategic.strategic_planning_data'))
        
        finally:
            session.close()
        
    return redirect(url_for('strategic.strategic_planning_data'))


@strategic_bp.route("/update_strategic_data/<int:strategic_data_id>", methods=['POST'])
@login_required
@required_roles('admin', 'admin_struts')
def update_strategic_data(strategic_data_id):
    """
    Function to handle updating strategic data.

    Parameters:
    - strategic_data_id: The ID of the strategic data to update.

    Returns:
    - Redirect to "strategic_planning_data" with success or error message.
    """
    try:
        task = session.query(StrategicTask).filter_by(id=strategic_data_id).first()
        if task:
            task.task = request.form.get('task')
            task.description = request.form.get('description') or None
            task.deliverables = request.form.get('deliverables') or None
            task.assigned_to = request.form.get('assigned_to')
            task.deadline = request.form.get('deadline') or None
            task.status = request.form.get('status')
            task.priority = request.form.get('priority')
            task.percentage_done = (Decimal(request.form.get('percentage_done'))
                                    if request.form.get('percentage_done') else None)
            task.fixed_cost = (Decimal(request.form.get('fixed_cost'))
                                if request.form.get('fixed_cost') else None)
            task.estimated_hours = (Decimal(request.form.get('estimated_cost'))
                                    if request.form.get('estimated_cost') else None)
            task.actual_hours = (Decimal(request.form.get('actual_cost'))
                                    if request.form.get('actual_cost') else None)
            task.link = request.form.get('link') or None

            session.commit()
            flash('Strategic task updated successfully!', 'success')
            return redirect(url_for('strategic.strategic_planning_data'))
        else:
            flash('Task not found.', 'error')
            return redirect(url_for('strategic.strategic_planning_data'))

    except Exception as e:
        flash(f'An error occurred while updating the task: {str(e)}', 'error')
        session.rollback()
        return redirect(url_for('strategic.strategic_planning_data'))
    
    finally:
        session.close()


@strategic_bp.route("/delete_strategic_data/<int:strategic_data_id>")
@login_required
@required_roles('admin', 'admin_struts')
def delete_strategic_data(strategic_data_id):
    """
    Function to handle deleting strategic data.

    Parameters:
    - strategic_data_id: The ID of the strategic data to delete.

    Returns:
    - Redirect to "strategic_planning_data" with success or error message.
    """
    try:
        task = session.query(StrategicTask).filter_by(id=strategic_data_id).first()
        if task:
            session.delete(task)
            session.commit()
            flash('Strategic task deleted successfully!', 'success')
        else:
            flash('Task not found.', 'error')

        return redirect(url_for('strategic.strategic_planning_data'))

    except Exception as e:
        flash(f'An error occurred while deleting the task: {str(e)}', 'error')
        session.rollback()
        return redirect(url_for('strategic.strategic_planning_data'))
    
    finally:
        session.close()
