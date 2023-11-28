from uuid import UUID

from sqlalchemy.orm.attributes import flag_modified

from .models import db
from .models.sessions import Session


def create_session(session_id: str) -> None:
    session = Session(id=session_id, cart=[])
    db.session.add(session)
    db.session.commit()


def get_cart(session_id: UUID) -> list[dict]:
    session = Session.query.filter_by(id=session_id).first()
    return session.cart


def delete_cart(session_id: UUID):
    session = Session.query.filter_by(id=session_id).first()
    session.cart = []
    db.session.commit()
    return session.cart


def delete_from_cart(session_id: UUID, product_id: UUID):
    session = Session.query.filter_by(id=session_id).first()

    updated_cart = []
    for p in session.cart:
        if p["id"] == product_id:
            p["quantity"] -= 1

            if p["quantity"] <= 0:
                continue

        updated_cart.append(p)

    session.cart = updated_cart
    flag_modified(session, "cart")
    db.session.commit()

    return session.cart


def add_product_to_cart(session_id: UUID, product: dict) -> list[dict]:
    session = Session.query.filter_by(id=session_id).first()

    if not session.cart:
        session.cart = []

    for item in session.cart:
        if item["id"] == product["id"]:
            item["quantity"] += 1
            break
    else:
        session.cart.append({**product, "quantity": 1})

    flag_modified(session, "cart")
    db.session.commit()

    return session.cart
