from sqlalchemy import Column, Integer, String, Text, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from models.projects import ProjectManagers
from models.base import BaseModel
from models.engine.database import session


class StrategicTask(BaseModel):
    __tablename__ = 'strategic_tasks'

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(String(255))
    priority = Column(String(255))
    deadline = Column(String(255))
    task = Column(Text)
    description = Column(Text)
    assigned_to = Column(Integer, ForeignKey('project_managers.id'))
    deliverables = Column(Text)
    percentage_done = Column(DECIMAL(10, 2))
    fixed_cost = Column(DECIMAL(10, 2))
    estimated_hours = Column(DECIMAL(10, 2))
    actual_hours = Column(DECIMAL(10, 2))
    link = Column(Text)


    @classmethod
    def strategic_tasks_to_dict_list(cls) -> list:
        try:
            query = (
                session.query(cls, ProjectManagers.name, ProjectManagers.section)
                .join(ProjectManagers, cls.assigned_to == ProjectManagers.id)
            )
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            session.close()

        results = query.all()

        task_list = [
            {
                **task.StrategicTask.to_dict(),
                'project_manager': task.name,
                'section': task.section
            }
            for task in results
        ]

        return task_list