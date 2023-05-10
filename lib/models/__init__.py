from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def import_models():
    from .documents import Document  # noqa
    from .products import Product  # noqa
    from .sessions import Session  # noqa


def init_db(app):
    import_models()

    db.init_app(app)
