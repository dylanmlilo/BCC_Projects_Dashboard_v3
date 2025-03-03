from sqlalchemy import Column, Integer, String, Date
from models.basemodel import BaseModel
from models.engine.database import session


class DailyTask(BaseModel):
    __tablename__ = 'daily_tasks'

    id = Column(Integer, primary_key=True)
    task = Column(String(200), nullable=False)
    number_done = Column(Integer)
    week_ending = Column(Date)
    responsible_person = Column(String(100))
    section = Column(String(50))

    def __repr__(self):
        return f"<DailyTask(task={self.task}, responsible_person={self.responsible_person}, week_ending={self.week_ending})>"

    @classmethod
    def get_all_tasks_to_dict_list(cls):
        try:
            all_tasks = session.query(DailyTask).all()
            all_tasks_dict = [task.to_dict() for task in all_tasks]
            return all_tasks_dict
        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()
            return []
        finally:
            session.close()
    
    @classmethod
    def get_latest_week_tasks(cls):
        try:
            latest_week = session.query(cls.week_ending).order_by(cls.week_ending.desc()).first()
            latest_week = latest_week[0] if latest_week else None

            if latest_week:
                formatted_week = latest_week.strftime("%A, %d %b %Y")
            else:
                formatted_week = "N/A"

            tasks_list = session.query(cls).filter(cls.week_ending == latest_week).all()
            tasks_list = [task.to_dict() for task in tasks_list]

            return tasks_list, formatted_week
        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()
            return [], "N/A"
        finally:
            session.close()

    @classmethod
    def get_weekending_dates(cls):
            # Fetch all existing Fridays in the database
            existing_fridays = session.query(DailyTask.week_ending).distinct().order_by(DailyTask.week_ending.desc()).all()
            existing_fridays = [date[0] for date in existing_fridays]  # Convert to list of dates
            return existing_fridays