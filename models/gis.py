from sqlalchemy import Column, Integer, String, Text, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import select
from models.base import BaseModel
from models.engine.database import session


class ResponsiblePerson(BaseModel):
    __tablename__ = "responsiblepeople"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    designation = Column(String(255), nullable=False)


    @classmethod
    def gis_responsible_person_data_to_dict_list(cls):
        """
        Queries the database for ResponsiblePerson data and
        converts it to a list of dictionaries.

        Returns:
            list: A list of dictionaries containing responsible person data.
        """
        try:
            query = session.query(cls).all()
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            session.close()

        responsible_person_list = [row.to_dict() for row in query]

        return responsible_person_list


class Output(BaseModel):
    __tablename__ = "output"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


    @classmethod
    def gis_output_data_to_dict_list(cls):
        """
        Queries the database for Output data and
        converts it to a list of dictionaries.

        Returns:
            list: A list of dictionaries containing output data.
        """
        try:
            query = session.query(Output).all()
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            session.close()

        output_list = [row.to_dict() for row in query]

        return output_list


class Activity(BaseModel):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    activity = Column(String(255), nullable=False)
    output_id = Column(Integer, ForeignKey("output.id"))
    responsible_person_id = Column(Integer, ForeignKey("responsiblepeople.id"))

    output = relationship("Output", backref="activities")
    responsible_person = relationship("ResponsiblePerson",
                                      backref="activities")


    @classmethod
    def gis_activity_data_to_dict_list(cls):
        """
        Queries the database for Activity data and
        converts it to a list of dictionaries.
        Returns:
            list: A list of dictionaries containing activity data.
        """
        try:
            query = session.query(cls).all()
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            session.close()

        activity_list = [row.to_dict() for row in query]

        return activity_list


class Task(BaseModel):
    """ Represents a task. """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey("activities.id"))
    description = Column(Text, nullable=False)
    percentage_of_activity = Column(DECIMAL(5, 2), nullable=True)
    status = Column(String(255), nullable=False)
    link = Column(Text, nullable=True)

    activity = relationship("Activity", backref="tasks")


    @classmethod
    def gis_task_data_to_dict_list(cls):
        """
        Queries the database for GIS task data and
        converts it to a list of dictionaries.

        Returns:
            list: A list of dictionaries containing GIS task data.
        """
        try:
            tasks = session.query(cls).all()
        except Exception as e:
            session.rollback()
            print(f"An error occurred: {e}")
        finally:
            session.close()

        task_list = [task.to_dict() for task in tasks]
        return task_list


def gis_data_to_dict_list():
    """
    Returns a list of dictionaries containing GIS data.

    This function queries the database to retrieve GIS data,
    including output information, activity details, responsible person
    information, and task descriptions. It then constructs a list of
    dictionaries, where each dictionary represents a single GIS data
    point. The function handles potential database errors and ensures
    that the session is properly closed.

    Returns:
        A list of dictionaries for GIS Data
    """
    try:
        query = select(
            Output.id,
            Output.name,
            Activity.activity,
            ResponsiblePerson.name,
            ResponsiblePerson.designation,
            Task.description,
            Task.status,
            Task.percentage_of_activity,
            Task.link
        ).select_from(
            Output
        ).outerjoin(
            Activity, Output.id == Activity.output_id
        ).outerjoin(
            ResponsiblePerson,
            Activity.responsible_person_id == ResponsiblePerson.id
        ).outerjoin(
            Task, Activity.id == Task.activity_id
        )

        results = session.execute(query).fetchall()

        gis_data = []
        for row in results:
            gis_dict = {
                "output_id": row[0],
                "output_name": row[1],
                "activity": row[2],
                "responsible_person": row[3],
                "designation": row[4],
                "task_description": row[5],
                "task_status": row[6],
                "percentage_of_activity": row[7],
                "link": row[8]
            }
            gis_data.append(gis_dict)

    except Exception as e:
        session.rollback()
        print(f"An error occurred: {e}")

    return gis_data