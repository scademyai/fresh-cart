from flask_sqlalchemy import SQLAlchemy
from pgvector.psycopg2 import register_vector
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()


def import_models():
    from .products import Product  # noqa
    from .sessions import Session  # noqa


def init_db(app):
    import_models()

    db.init_app(app)


@event.listens_for(Engine, "connect")
def connect(dbapi_connection, _):
    register_vector(dbapi_connection)
