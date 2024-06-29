from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text


DB_NAME = "hostname_server_app"
DB_USER = "hostname_server_app"
DB_PASS = "wGARcPWf4H7p8bxKrGACpQdbHz5GXGEs"
DB_HOST = "db"
DB_PORT = "5432"

db_string = "postgresql://{}:{}@{}:{}/{}".format(
    DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
)
engine = create_engine(db_string)

db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import hostname_server.models

    Base.metadata.create_all(bind=engine)


def test_db():
    import hostname_server.models

    db_session.execute(text("SELECT 1"))
