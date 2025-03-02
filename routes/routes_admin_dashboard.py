from flask import Blueprint, render_template
from flask_login import login_required
from models.decorators import required_roles


admin_dashboard_bp = Blueprint('admin_dashboard', __name__)


@admin_dashboard_bp.route("/admin_dashboard", strict_slashes=False)
@login_required
@required_roles('admin', 'admin_gis', 'admin_strategic_planning', 'admin_projects',
                'admin_sanitation', 'admin_electromechanical', 'admin_water_quality',
                'admin_water', 'admin_daily_tasks')
def admin_dashboard():
    """
    Renders the admin dashboard page.

    Returns:
        flask.Response: The rendered admin dashboard template.
    """
    return render_template("admin_dashboard.html")
