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
from datetime import datetime
from decimal import Decimal


projects_bp = Blueprint('projects', __name__)


@projects_bp.route("/projects_data", strict_slashes=False)
@login_required
@required_roles('admin', 'admin_projects')
def projects_data():
    """
    Function to handle projects data retrieval and rendering.

    Retrieves projects data and today's date, then
    renders the projects_data.html template.

    Parameters:
    - None

    Returns:
    - Rendered template "projects_data.html" with today's
    date and projects data.

    """
    projects_data = ProjectsData.projects_data_to_dict_list()
    project_managers = ProjectManagers.project_managers_to_dict_list()
    sections = Section.section_data_to_dict_list()
    formatted_date = today_date()
    return render_template("projects_data.html", today_date=formatted_date,
                           projects_data=projects_data, sections=sections,
                           project_managers=project_managers)


@projects_bp.route("/insert_project_manager", methods=['POST'])
@login_required
@required_roles('admin', 'admin_projects', 'admin_struts')
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


@projects_bp.route(
    "/update_projects_project_manager/<int:project_manager_id>",
    methods=['POST'])
@login_required
@required_roles('admin', 'admin_projects', 'admin_struts')
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


@projects_bp.route("/delete_projects_project_manager/<int:project_manager_id>")
@login_required
@required_roles('admin', 'admin_projects', 'admin_struts')
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


@projects_bp.route('/insert_projects_data', methods=['POST'])
@login_required
@required_roles('admin', 'admin_projects')
def insert_projects_data():
    if request.method == "POST":   
        try:
            new_data = ProjectsData(
                contract_number=request.form.get("contract_number"),
                contract_name=request.form.get("contract_name"),
                contract_type_id=int(request.form.get("contract_type_id", 0)),
                project_manager_id=int(request.form.get("project_manager_id", 0)),
                section_id=int(request.form.get("section_id", 0)),
                contractor=request.form.get("contractor"),
                year=request.form.get("year"),
                date_contract_signed=datetime.strptime(request.form.get("date_contract_signed"), "%Y-%m-%d").date() if request.form.get("date_contract_signed") else None,
                date_contract_signed_by_bcc=datetime.strptime(request.form.get("date_contract_signed_by_bcc"), "%Y-%m-%d").date() if request.form.get("date_contract_signed_by_bcc") else None,
                early_start_date=datetime.strptime(request.form.get("early_start_date"), "%Y-%m-%d").date() if request.form.get("early_start_date") else None,
                contract_duration_weeks=Decimal(request.form.get("contract_duration_weeks")) if request.form.get("contract_duration_weeks") else None,
                contract_duration_months=Decimal(request.form.get("contract_duration_months")) if request.form.get("contract_duration_months") else None,
                early_finish_date=datetime.strptime(request.form.get("early_finish_date"), "%Y-%m-%d").date() if request.form.get("early_finish_date") else None,
                extension_of_time=datetime.strptime(request.form.get("extension_of_time"), "%Y-%m-%d").date() if request.form.get("extension_of_time") else None,
                project_status=request.form.get("project_status"),
                contract_value_including_ten_percent_contingency=Decimal(request.form.get("contract_value_including_ten_percent_contingency")) if request.form.get("contract_value_including_ten_percent_contingency") else None,
                performance_guarantee_value=Decimal(request.form.get("performance_guarantee_value")) if request.form.get("performance_guarantee_value") else None,
                performance_guarantee_expiry_date=datetime.strptime(request.form.get("performance_guarantee_expiry_date"), "%Y-%m-%d").date() if request.form.get("performance_guarantee_expiry_date") else None,
                advance_payment_value=Decimal(request.form.get("advance_payment_value")) if request.form.get("advance_payment_value") else None,
                advance_payment_guarantee_expiry_date=datetime.strptime(request.form.get("advance_payment_guarantee_expiry_date"), "%Y-%m-%d").date() if request.form.get("advance_payment_guarantee_expiry_date") else None,
                total_certified_interim_payments_to_date=Decimal(request.form.get("total_certified_interim_payments_to_date")) if request.form.get("total_certified_interim_payments_to_date") else None,
                financial_progress_percentage=Decimal(request.form.get("financial_progress_percentage")) if request.form.get("financial_progress_percentage") else None,
                roads_progress=Decimal(request.form.get("roads_progress")) if request.form.get("roads_progress") else None,
                water_progress=Decimal(request.form.get("water_progress")) if request.form.get("water_progress") else None,
                sewer_progress=Decimal(request.form.get("sewer_progress")) if request.form.get("sewer_progress") else None,
                storm_drainage_progress=Decimal(request.form.get("storm_drainage_progress")) if request.form.get("storm_drainage_progress") else None,
                public_lighting_progress=Decimal(request.form.get("public_lighting_progress")) if request.form.get("public_lighting_progress") else None,
                physical_progress_percentage=Decimal(request.form.get("physical_progress_percentage")) if request.form.get("physical_progress_percentage") else None,
                tax_clearance_validation=request.form.get("tax_clearance_validation"),
                link=request.form.get("link")
            )

            session.add(new_data)
            session.commit()
            flash('Projects Data inserted successfully!', 'success')
            return redirect(request.referrer)

        
        except Exception as e:
            flash(f'An error occurred while inserting the projects data: {str(e)}', 'error')
            session.rollback()
            return redirect(request.referrer)


        finally:
            session.rollback()

    return redirect(request.referrer)



@projects_bp.route('/update_projects_data/<int:projects_data_id>', methods=['POST'])
@login_required
@required_roles('admin', 'admin_projects')
def update_projects_data(projects_data_id):
    if request.method == "POST":
        try:    
            existing_data = session.query(ProjectsData).get(projects_data_id)

            if not existing_data:
                flash('Projects Data not found!', 'error')
                return redirect(url_for('projects.projects_data'))

            existing_data.contract_number = request.form.get("contract_number")
            existing_data.contract_name = request.form.get("contract_name")
            existing_data.contract_type_id = int(request.form.get("contract_type_id", 0))
            existing_data.project_manager_id = int(request.form.get("project_manager_id", 0))
            existing_data.section_id = int(request.form.get("section_id", 0))
            existing_data.contractor = request.form.get("contractor")
            existing_data.year = request.form.get("year")
            existing_data.date_contract_signed = (
                datetime.strptime(request.form.get("date_contract_signed"), "%Y-%m-%d").date()
                if request.form.get("date_contract_signed") else None
            )
            existing_data.date_contract_signed_by_bcc = (
                datetime.strptime(request.form.get("date_contract_signed_by_bcc"), "%Y-%m-%d").date()
                if request.form.get("date_contract_signed_by_bcc") else None
            )
            existing_data.early_start_date = (
                datetime.strptime(request.form.get("early_start_date"), "%Y-%m-%d").date()
                if request.form.get("early_start_date") else None
            )
            existing_data.contract_duration_weeks = (
                Decimal(request.form.get("contract_duration_weeks"))
                if request.form.get("contract_duration_weeks") else None
            )
            existing_data.contract_duration_months = (
                Decimal(request.form.get("contract_duration_months"))
                if request.form.get("contract_duration_months") else None
            )
            existing_data.early_finish_date = (
                datetime.strptime(request.form.get("early_finish_date"), "%Y-%m-%d").date()
                if request.form.get("early_finish_date") else None
            )
            existing_data.extension_of_time = (
                Decimal(request.form.get("extension_of_time"))
                if request.form.get("extension_of_time") else None
            )
            existing_data.project_status = request.form.get("project_status")
            existing_data.contract_value_including_ten_percent_contingency = (
                Decimal(request.form.get("contract_value_including_ten_percent_contingency"))
                if request.form.get("contract_value_including_ten_percent_contingency") else None
            )
            existing_data.performance_guarantee_value = (
                Decimal(request.form.get("performance_guarantee_value"))
                if request.form.get("performance_guarantee_value") else None
            )
            existing_data.performance_guarantee_expiry_date = (
                datetime.strptime(request.form.get("performance_guarantee_expiry_date"), "%Y-%m-%d").date()
                if request.form.get("performance_guarantee_expiry_date") else None
            )
            existing_data.advance_payment_value = (
                Decimal(request.form.get("advance_payment_value"))
                if request.form.get("advance_payment_value") else None
            )
            existing_data.advance_payment_guarantee_expiry_date = (
                datetime.strptime(request.form.get("advance_payment_guarantee_expiry_date"), "%Y-%m-%d").date()
                if request.form.get("advance_payment_guarantee_expiry_date") else None
            )
            existing_data.total_certified_interim_payments_to_date = (
                Decimal(request.form.get("total_certified_interim_payments_to_date"))
                if request.form.get("total_certified_interim_payments_to_date") else None
            )
            existing_data.financial_progress_percentage = (
                Decimal(request.form.get("financial_progress_percentage"))
                if request.form.get("financial_progress_percentage") else None
            )
            existing_data.roads_progress = (
                Decimal(request.form.get("roads_progress"))
                if request.form.get("roads_progress") else None
            )
            existing_data.water_progress = (
                Decimal(request.form.get("water_progress"))
                if request.form.get("water_progress") else None
            )
            existing_data.sewer_progress = (
                Decimal(request.form.get("sewer_progress"))
                if request.form.get("sewer_progress") else None
            )
            existing_data.storm_drainage_progress = (
                Decimal(request.form.get("storm_drainage_progress"))
                if request.form.get("storm_drainage_progress") else None
            )
            existing_data.public_lighting_progress = (
                Decimal(request.form.get("public_lighting_progress"))
                if request.form.get("public_lighting_progress") else None
            )
            existing_data.physical_progress_percentage = (
                Decimal(request.form.get("physical_progress_percentage"))
                if request.form.get("physical_progress_percentage") else None
            )
            existing_data.tax_clearance_validation = request.form.get("tax_clearance_validation")
            existing_data.link = request.form.get("link")

            session.commit()
            flash('Projects Data updated successfully!', 'success')
            return redirect(request.referrer)
        
        except Exception as e:
            flash(f'An error occurred while updating the projects data: {str(e)}', 'error')
            session.rollback()
            return redirect(request.referrer)
        
        finally:
            session.close()

    return redirect(request.referrer)


@projects_bp.route("/delete_projects_data/<int:project_data_id>")
@login_required
@required_roles('admin', 'admin_projects')
def delete_projects_data(project_data_id):
    try:
        project_data = session.query(ProjectsData).filter_by(id=project_data_id).first()
        if not project_data:
            flash('Projects Data not found!', 'error')
            return redirect(url_for('projects.projects_data'))

        session.delete(project_data)
        session.commit()
        flash('Project data deleted successfully!', 'success')

    except Exception as e:
        flash(f'An error occurred while deleting the projects data: {str(e)}', 'error')
        session.rollback()
        return redirect(request.referrer)
    
    finally:
        session.close()
        
    return redirect(request.referrer)