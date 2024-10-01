from database.models import Prospect

from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database\\database.db')
Session = sessionmaker(bind=engine)
session = Session()


class ProspectHelper:
    @staticmethod
    def create(**kwargs):
        p = Prospect(
            **kwargs
        )

        session.add(p)
        session.commit()

    @staticmethod
    def get(prospect_id):
        prospect = session.query(Prospect).get(prospect_id)

        return prospect

    @staticmethod
    def get_all():
        alldata = session.query(Prospect).all()

        return alldata

    @staticmethod
    def update(prospect_id, **kwargs):
        session.query(Prospect).filter(Prospect.id == prospect_id).update(dict(kwargs))
        session.commit()
        session.flush()

    @staticmethod
    def delete(prospect_id):
        session.query(Prospect).filter(Prospect.id == prospect_id).delete()
        session.commit()
        session.flush()
