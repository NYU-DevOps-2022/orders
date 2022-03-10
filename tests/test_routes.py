"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
from unittest import TestCase

import werkzeug
from flask import Flask, request
from service import status  # HTTP Status Codes
from service.routes import app, init_db, list_orders, check_content_type, get_order
from .factories import OrderFactory

# DATABASE_URI = os.getenv(
#     "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
# )


BASE_URL = "/orders"
CONTENT_TYPE_JSON = "application/json"


######################################################################
#  T E S T   C A S E S
######################################################################
class order(TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        pass

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        pass

    def _create_order(self, count):
        """Factory method to create orders in bulk"""
        orders = []
        for _ in range(count):
            test_order = OrderFactory()
            resp = self.app.post(
                BASE_URL, json=test_order.serialize(), content_type=CONTENT_TYPE_JSON
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test order"
            )
            new_order = resp.get_json()
            test_order.id_order = new_order["id_order"]
            orders.append(test_order)
        return orders

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    # TODO(ELF): test modifying order

    def test_list_orders(self):
        """Test a list of orders"""
        self.assertEqual(b'[]\n', list_orders().data)
        test_order = self._create_order(1)[0]
        self.assertTrue(list_orders().data)
        resp = self.app.delete(
            f"{BASE_URL}/{test_order.id_order}", content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(b'[]\n', list_orders().data)

    def test_delete_order(self):
        """Delete an Order"""
        init_db()
        test_order = self._create_order(1)[0]
        resp = self.app.delete(
            f"{BASE_URL}/{test_order.id_order}", content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)
        # make sure they are deleted
        resp = self.app.get(
            f"{BASE_URL}/{test_order.id_order}", content_type=CONTENT_TYPE_JSON
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_check_content_type(self):
        # with self.assertRaises(RuntimeError):
        #     check_content_type("blah")
        with app.test_request_context():
            with self.assertRaises(werkzeug.exceptions.UnsupportedMediaType):
                check_content_type("blah")

    # def test_get_order(self):
    #     test_order = self._create_order(1)[0]
    #     self.assertEqual("a", get_order(test_order.id_order))
