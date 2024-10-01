from sqlalchemy import *

from database.models import Base


if __name__ == '__main__':
    engine = create_engine('sqlite:///database.db')
    Base.metadata.create_all(engine)