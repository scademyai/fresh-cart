from uuid import uuid4

from truth.truth import AssertThat

from freshcart.lib.models import db
from freshcart.lib.models.sessions import Session
from freshcart.lib.session import (
    add_product_to_cart,
    create_session,
    delete_cart,
    delete_from_cart,
    get_cart,
)
from freshcart.tests import AppTestCase, DbMixin


class TestSession(DbMixin, AppTestCase):
    def test_create_session_works(self) -> None:
        session_id = uuid4()

        create_session(session_id)

        session = Session.query.first()

        AssertThat(session.id).IsEqualTo(session_id)

    def test_get_cart_returns_cart_contents(self) -> None:
        session_id = uuid4()
        cart = [{"id": 1, "quantity": 2}, {"id": 2, "quantity": 3}]
        session = Session(id=session_id, cart=cart)
        db.session.add(session)
        db.session.commit()

        cart_contents = get_cart(session_id)

        AssertThat(cart_contents).IsEqualTo(cart)

    def test_add_product_to_cart_adds_new_item(self) -> None:
        session_id = uuid4()
        cart = [{"id": 1, "quantity": 1}, {"id": 2, "quantity": 1}]
        session = Session(id=session_id, cart=cart)
        db.session.add(session)
        db.session.commit()

        new_item = {"id": 3}
        add_product_to_cart(session_id, new_item)

        session_from_db = Session.query.first()

        AssertThat(session_from_db.cart).IsEqualTo(
            [
                {"id": 1, "quantity": 1},
                {"id": 2, "quantity": 1},
                {"id": 3, "quantity": 1},
            ]
        )

    def test_add_product_to_cart_increases_quantity_of_existing_item(
        self,
    ) -> None:
        session_id = uuid4()
        cart = [{"id": 1, "quantity": 1}, {"id": 2, "quantity": 1}]
        session = Session(id=session_id, cart=cart)
        db.session.add(session)
        db.session.commit()

        new_item = {"id": 2}
        add_product_to_cart(session_id, new_item)

        session_from_db = Session.query.first()

        AssertThat(session_from_db.cart).IsEqualTo(
            [{"id": 1, "quantity": 1}, {"id": 2, "quantity": 2}]
        )

    def test_add_product_to_cart_returns_updated_cart(self) -> None:
        session_id = uuid4()
        cart = [{"id": 1, "quantity": 1}, {"id": 2, "quantity": 1}]
        session = Session(id=session_id, cart=cart)
        db.session.add(session)
        db.session.commit()

        new_item = {"id": 3}
        updated_cart = add_product_to_cart(session_id, new_item)

        AssertThat(updated_cart).IsEqualTo(
            [
                {"id": 1, "quantity": 1},
                {"id": 2, "quantity": 1},
                {"id": 3, "quantity": 1},
            ]
        )

    def test_delete_cart_returns_empty_cart(self) -> None:
        session_id = uuid4()
        cart = [{"id": 1, "quantity": 2}, {"id": 2, "quantity": 3}]
        session = Session(id=session_id, cart=cart)
        db.session.add(session)
        db.session.commit()

        deleted_cart = delete_cart(session.id)
        AssertThat(deleted_cart).IsEqualTo([])

    def test_delete_from_cart_removes_one_item_from_cart(self) -> None:
        session_id = uuid4()
        cart = [{"id": 1, "quantity": 2}, {"id": 2, "quantity": 3}]
        session = Session(id=session_id, cart=cart)
        db.session.add(session)
        db.session.commit()

        delete_from_cart(session.id, 1)

        session_from_db = Session.query.first()

        AssertThat(session_from_db.cart).IsEqualTo(
            [{"id": 1, "quantity": 1}, {"id": 2, "quantity": 3}]
        )

    def test_delete_from_cart_removes_last_item_from_cart(self) -> None:
        session_id = uuid4()
        cart = [{"id": 1, "quantity": 1}, {"id": 2, "quantity": 3}]
        session = Session(id=session_id, cart=cart)
        db.session.add(session)
        db.session.commit()

        delete_from_cart(session.id, 1)

        session_from_db = Session.query.first()

        AssertThat(session_from_db.cart).IsEqualTo([{"id": 2, "quantity": 3}])

    def test_delete_from_cart_returns_updated_cart(self) -> None:
        session_id = uuid4()
        cart = [{"id": 1, "quantity": 2}, {"id": 2, "quantity": 3}]
        session = Session(id=session_id, cart=cart)
        db.session.add(session)
        db.session.commit()

        filtered_cart = delete_from_cart(session.id, 1)

        AssertThat(filtered_cart).IsEqualTo(
            [{"id": 1, "quantity": 1}, {"id": 2, "quantity": 3}]
        )
