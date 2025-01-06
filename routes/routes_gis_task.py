from flask import Blueprint, request, redirect, url_for, flash
from models.engine.database import session
from models.gis import Task
from flask_login import login_required
from models.decorators import required_roles


gis_task_bp = Blueprint('gis_task', __name__)


@gis_task_bp.route("/insert_gis_task_data", methods=['POST'])
@login_required
@required_roles("admin", "admin_gis")
def insert_gis_task_data():
    """
    Function to handle the insertion of new GIS task data.

    Returns:
    - A redirect response to the GIS data page.
    """
    if request.method == "POST":
        try:
            activity_id = request.form.get('activity_id')
            description = request.form.get('description')
            percentage_of_activity = request.form.get('percentage_of_activity')

            if not activity_id:
                flash('Activity ID is required.', 'error')
                return redirect(url_for('gis_data.gis_data'))

            percentage_of_activity = float(percentage_of_activity) if percentage_of_activity else None
            status = request.form.get('status') or None
            link = request.form.get('link') or None

            new_task = Task(
                activity_id=activity_id,
                description=description,
                percentage_of_activity=percentage_of_activity,
                status=status,
                link=link
            )

            session.add(new_task)
            session.commit()

            flash('Data inserted successfully!', 'success')
            return redirect(url_for('gis_data.gis_data'))

        except Exception as e:
            session.rollback()
            flash('An error occurred while inserting the data. Please try again.', 'error')
            return redirect(url_for('gis_data.gis_data'))
        
        finally:
            session.close()

    return redirect(url_for('gis_data.gis_data'))


@gis_task_bp.route("/update_gis_task_data/<int:gis_task_data_id>", methods=['POST'])
@login_required
@required_roles("admin", "admin_gis")
def update_gis_task_data(gis_task_data_id):
    """
    Updates the GIS task data in the database and redirects to the GIS data page.

    Args:
        gis_task_data_id (int): The ID of the GIS task data to be updated.

    Returns:
        flask.Response: A redirect response to the GIS data page or
        a JSON response with an error message.
    """
    if request.method == 'POST':
        try:
            task = session.query(Task).filter_by(id=gis_task_data_id).first()
            if task:
                task.activity_id = request.form.get('activity_id')
                task.description = request.form.get('description')
                
                percentage_of_activity = request.form.get('percentage_of_activity')
                task.percentage_of_activity = float(percentage_of_activity) if percentage_of_activity else None
                
                task.status = request.form.get('status') or None
                task.link = request.form.get('link') or None

                session.commit()
                flash('Data updated successfully!', 'success')
            else:
                flash('Task not found.', 'error')

            return redirect(url_for('gis_data.gis_data'))

        except Exception as e:
            flash('An error occurred while updating the data. Please try again.', 'error')
            session.rollback()
            return redirect(url_for('gis_data.gis_data'))

        finally:
            session.close()

    return redirect(url_for('gis_data.gis_data'))


@gis_task_bp.route("/delete_gis_task_data/<int:gis_task_data_id>")
@login_required
@required_roles("admin", "admin_gis")
def delete_gis_task_data(gis_task_data_id):
    """
    Deletes the GIS task data from the database and redirects to the GIS data page.

    Args:
        gis_task_data_id (int): The ID of the GIS task data to be deleted.

    Returns:
        flask.Response: A redirect response to the GIS data page or
        a JSON response with an error message.
    """
    try:
        task = session.query(Task).filter_by(id=gis_task_data_id).first()
        if task:
            session.delete(task)
            session.commit()
            flash('Data deleted successfully!', 'success')
        else:
            flash('Task not found.', 'error')

        return redirect(url_for('gis_data.gis_data'))

    except Exception as e:
        flash(f'An error occurred while deleting data: {str(e)}', 'error')
        session.rollback()
        return redirect(url_for('gis_data.gis_data'))
    
    finally:
        session.close()