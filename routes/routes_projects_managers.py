from flask import (
    Blueprint, render_template, abort,
    jsonify, request, redirect, url_for, flash
)
from flask_login import login_required
from models.engine.database import session
from models.date import today_date
from models.projects import (
    ProjectsData, ProjectManagers, Section
)
from models.decorators import required_roles


project_manager_bp = Blueprint('project_manager', __name__)


@project_manager_bp.route("/insert_project_manager", methods=['POST'])
@login_required
@required_roles('admin', 'admin_projects', 'admin_strategic_planning',
                'admin_sanitation', 'admin_electromechanical', 'admin_water_quality')
def insert_project_manager():
    """
    Function to handle insert project manager route.
    """
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            section = request.form.get('section')

            new_project_manager = ProjectManagers(name=name, section=section)
            session.add(new_project_manager)
            session.commit()
            flash('Project manager added successfully!', 'success')
            return redirect(request.referrer)

        except Exception as e:
            flash(f'An error occurred while adding the project manager: {str(e)}', 'error')
            session.rollback()
            return redirect(request.referrer)
        
        finally:
            session.close()

    return redirect(request.referrer)


@project_manager_bp.route(
    "/update_projects_project_manager/<int:project_manager_id>",
    methods=['POST'])
@login_required
@required_roles('admin', 'admin_projects', 'admin_strategic_planning',
                'admin_sanitation', 'admin_electromechanical', 'admin_water_quality')
def update_projects_project_manager(project_manager_id):
    """
    Function to handle update project manager route.
    """
    if request.method == 'POST':    
        try:
            project_manager = (
                session.query(ProjectManagers)
                .filter_by(id=project_manager_id)
                .first()
            )
            if project_manager:
                project_manager.name = request.form.get('name')
                project_manager.section = request.form.get('section')
                session.commit()
                flash('Project manager updated successfully!', 'success')
            else:
                flash('Project manager not found.', 'error')

            return redirect(request.referrer)

        except Exception as e:
            flash(f'An error occurred while updating the project manager: {str(e)}', 'error')
            session.rollback()
            return redirect(request.referrer)

        finally:
            session.close()

    return redirect(request.referrer)


@project_manager_bp.route("/delete_projects_project_manager/<int:project_manager_id>")
@login_required
@required_roles('admin', 'admin_projects', 'admin_strategic_planning',
                'admin_sanitation', 'admin_electromechanical', 'admin_water_quality')
def delete_projects_project_manager(project_manager_id):
    """
    Function to handle delete project manager route.

    Parameters:
    - project_manager_id: The ID of the project manager to be deleted.

    Returns:
    - A redirect response to the projects data page.
    """
    try:
        project_manager = (
            session.query(ProjectManagers)
            .filter_by(id=project_manager_id)
            .first()
        )
        if project_manager:
            session.delete(project_manager)
            session.commit()
            flash('Project manager deleted successfully!', 'success')
        else:
            flash('Project manager not found.', 'error')
        
        return redirect(request.referrer)

    except Exception as e:
        flash(f'An error occurred while deleting the project manager: Project manager is linked to a project', 'error')
        session.rollback()
        return redirect(request.referrer)
    
    finally:
        session.close()