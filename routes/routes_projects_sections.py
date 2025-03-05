from flask import Blueprint, request, flash, redirect
from models.engine.database import session
from models.projects import Section

projects_sections_bp = Blueprint('projects_sections', __name__)


@projects_sections_bp.route('/insert_projects_section', methods=["POST"])
def insert_projects_section():
    if request.method == "POST":
        try:
            name = request.form.get("name")

            new_section = Section(name=name)
            session.add(new_section)
            session.commit()
            flash('Project manager added successfully!', 'success')
            return redirect(request.referrer)

        except Exception as e:
            flash(f'An error occurred while adding the section: {str(e)}', 'error')
            session.rollback()
            return redirect(request.referrer)
        
        finally:
            session.close()

    return redirect(request.referrer)



@projects_sections_bp.route('/update_projects_section/<int:section_id>', methods=["POST"])
def update_projects_section(section_id):
    if request.method == "POST":
        try:
            section = session.query(Section).filter_by(id=section_id).first()
            if section:
                section.name = request.form.get("name")
                session.commit()
                flash('Section updated successfully!', 'success')
            else:
                flash('Section not found!', 'error')

            return redirect(request.referrer)

        except Exception as e:
            flash(f'An error occurred while updating the section: {str(e)}', 'error')
            session.rollback()
            return redirect(request.referrer)
        finally:        
            session.close()

    return redirect(request.referrer)


@projects_sections_bp.route('/delete_projects_section/<int:section_id>')
def delete_projects_section(section_id):
    try:
        section = session.query(Section).filter_by(id=section_id).first()
        if section:
            session.delete(section)
            session.commit()
            flash('Section deleted successfully!', 'success')
        else:
            flash('Section not found!', 'error')

        return redirect(request.referrer)

    except Exception as e:
        flash(f'An error occurred while deleting the section: The section is linked to a project.', 'error')
        return redirect(request.referrer)
    
    finally:
        session.close()
