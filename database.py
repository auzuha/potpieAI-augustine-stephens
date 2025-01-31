from sqlalchemy.orm import declarative_base, sessionmaker ,scoped_session
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine(
                        'sqlite:///db.db'
                     )

Session = sessionmaker(bind=engine)

def get_db():
    global Session
    session = scoped_session(Session)
    return session
def init_db():
    Base.metadata.create_all(bind=engine)

def add_to_db(object):
    global Session
    session = scoped_session(Session)
    session.add(object)
    session.commit()
    session.close()