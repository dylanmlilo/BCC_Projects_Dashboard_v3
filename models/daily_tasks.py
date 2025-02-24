from sqlalchemy import Column, Integer, String, Date, func
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
    def daily_tasks_to_dict_list(cls) -> tuple[list[dict], str]:
        """Fetch tasks for the latest week-ending date"""
        try:
            latest_week = session.query(func.max(cls.week_ending)).scalar()
            if latest_week:
                tasks = session.query(cls).filter(cls.week_ending == latest_week).all()
                tasks_list = [task.to_dict() for task in tasks]
                return tasks_list, latest_week.strftime("%d %b %Y")
            return [], None
        except Exception as e:
            print(f"An error occurred: {e}")
            session.rollback()
            return [], None
        finally:
            session.close()

    @classmethod
    def get_latest_week_tasks(cls):
        try:
            latest_week = session.query(cls.week_ending).order_by(cls.week_ending.desc()).first()
            latest_week = latest_week[0] if latest_week else None

            if latest_week:
                formatted_week = latest_week.strftime("%d %b %Y")
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