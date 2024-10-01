from sqlalchemy import event, Column, ForeignKey, Integer, String, Date, DateTime, Boolean, Text, Numeric
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, backref
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLite3Connection


Base = declarative_base()

# - Specific to SQLite, used for CASCADE delete
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


class Application(Base):
    __tablename__ = "application"

    id = Column(Integer, primary_key=True)
    job_title = Column(String, nullable=True)
    company = Column(String, nullable=True)
    city = Column(String, nullable=True)
    application_date = Column(Date, nullable=True)
    decline_date = Column(Date, nullable=True)
    via = Column(String, nullable=True)
    offer_link = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    map_link = Column(Text, nullable=True)
    created_at_utc = Column(DateTime, nullable=True)

    def __init__(self, job_title=None, company=None, city=None, application_date=None, decline_date=None,
                 via=None, offer_link=None, notes=None, map_link=None, created_at_utc=None):
        self.job_title = job_title
        self.company = company
        self.city = city
        self.application_date = application_date
        self.decline_date = decline_date
        self.via = via
        self.offer_link = offer_link
        self.notes = notes
        self.map_link = map_link
        self.created_at_utc = created_at_utc

    def __repr__(self):
        return f"Application({self.job_title}, {self.company}, {self.application_date})"


class ApplicationStep(Base):
    __tablename__ = "application_step"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("application.id", ondelete='CASCADE'))

    name = Column(String, nullable=True)
    scheduled_date = Column(Date, nullable=True)
    via = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    created_at_utc = Column(DateTime, nullable=True)

    application = relationship("Application", backref=backref("application_steps", passive_deletes=True, cascade='all, delete-orphan'), lazy=False)

    def __init__(self, application_id=None, name=None, scheduled_date=None, via=None, notes=None, created_at_utc=None):
        self.application_id = application_id
        self.name = name
        self.scheduled_date = scheduled_date
        self.via = via
        self.notes = notes
        self.created_at_utc = created_at_utc

    def __repr__(self):
        return f"ApplicationStep({self.name}, {self.scheduled_date}, {self.application_id})"


class Contact(Base):
    __tablename__ = "contact"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("application.id", ondelete='CASCADE'))

    name = Column(String, nullable=True)
    position = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    application = relationship("Application", backref=backref("contacts", passive_deletes=True, cascade='all, delete-orphan'), lazy=False)

    def __init__(self, application_id=None, name=None, position=None, notes=None):
        self.application_id = application_id
        self.name = name
        self.position = position
        self.notes = notes

    def __repr__(self):
        return f"Contact({self.name})"


class Prospect(Base):
    __tablename__ = "prospect"

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=True)
    url = Column(String, nullable=True)
    notes = Column(Text, nullable=True)

    def __init__(self, name=None, url=None, notes=None):
        self.name = name
        self.url = url
        self.notes = notes

    def __repr__(self):
        return f"Prospect({self.name})"