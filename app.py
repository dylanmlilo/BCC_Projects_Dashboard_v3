from flask import Flask
from flask_login import LoginManager
from models.engine.database import session
from models.users import Users
from routes.routes_home import home_bp
from routes.routes_strategic import strategic_bp
from routes.routes_gis_data import gis_data_bp
from routes.routes_landing import landing_bp
from routes.routes_admin_dashboard import admin_dashboard_bp
from routes.routes_projects import projects_bp
from routes.routes_gis_activity import gis_activity_bp
from routes.routes_gis_task import gis_task_bp
from routes.routes_gis_resp_person import gis_resp_person_bp
from routes.routes_APIs import api_bp
from routes.routes_gis_output import gis_output_bp
from routes.routes_users import users_bp
from routes.routes_water_projects import water_projects_bp
from routes.routes_electromechanical_projects import electromechanical_projects_bp
from routes.routes_sanitation_projects import sanitation_projects_bp
from routes.routes_water_quality_projects import water_quality_projects_bp
from routes.routes_projects_sections import projects_sections_bp
from routes.routes_projects_managers import project_manager_bp
import os
from dotenv import load_dotenv


load_dotenv()


app = Flask(__name__)
app.register_blueprint(home_bp)
app.register_blueprint(strategic_bp)
app.register_blueprint(gis_data_bp)
app.register_blueprint(gis_activity_bp)
app.register_blueprint(gis_task_bp)
app.register_blueprint(gis_resp_person_bp)
app.register_blueprint(gis_output_bp)
app.register_blueprint(landing_bp)
app.register_blueprint(admin_dashboard_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(api_bp)
app.register_blueprint(users_bp)
app.register_blueprint(water_projects_bp)
app.register_blueprint(electromechanical_projects_bp)
app.register_blueprint(sanitation_projects_bp)
app.register_blueprint(water_quality_projects_bp)
app.register_blueprint(projects_sections_bp)
app.register_blueprint(project_manager_bp)
app.secret_key = os.getenv("SECRET_KEY")


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'landing.login'


@login_manager.user_loader
def load_user(user_id):
    """Loads a user object from the database based on the user ID."""
    try:
        user = session.get(Users, int(user_id))
        return user
    except Exception as e:
        print(f"An error occurred while loading user: {e}")
        session.rollback()
        return None


if __name__ == "__main__":
    app.run(debug=True, port=4000)
