# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Test cases for Order Model

Test cases can be run with:
    nosetests
    coverage report -m

While debugging just these tests it's convenient to use this:
    nosetests --stop tests/test_orders.py:TestPetModel

"""
# from asyncio.windows_events import NULL
from asyncio.log import logger
import logging
import os
import unittest
from werkzeug.exceptions import NotFound

import flask_sqlalchemy
from werkzeug.exceptions import NotFound

from service import app
from service.models import Order, OrderItem, db, DataValidationError
from .factories import OrderFactory, OrderItemFactory, OrderWithItemsFactory

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  Order   M O D E L   T E S T   C A S E S
######################################################################
class TestOrderModel(unittest.TestCase):
    """Test Cases for Order Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Order.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """This runs once after the entire test suite"""
        db.session.close()

    def setUp(self):
        """This runs before each test"""
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """This runs after each test"""
        db.session.remove()
        db.drop_all()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_order(self):
        """Create an order and assert that it exists"""
        order = Order(id=1, 
        date_order='02/22/2022', customer_id=1)

        self.assertIsNotNone(order)
        self.assertEqual(order.id, 1)
        self.assertEqual(order.date_order, '02/22/2022')

    def test_add_a_order(self):
        """Create an order and add it to the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        order = Order(id=1, date_order='02/22/2022', customer_id=1, items=[
            OrderItem(order_id=1, product_id=3, product_price = 10, product_quantity=20),
            OrderItem(order_id=1, product_id=5, product_price = 15, product_quantity=10)
        ])
        order.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(order.id, 1)
        self.assertEqual(len(order.items), 2)
        orders = Order.all()
        self.assertEqual(len(orders), 1)

    def test_add_an_order_using_item_list(self):
        """Create an order using item_list"""
        orders = Order.all()
        self.assertEqual(orders, [])
        order = Order(id=1, date_order='02/22/2022', customer_id=1)

        order.item_list = [
            dict({"product_id": 1, "product_quantity": 3, "product_price": 5}),
            dict({"product_id": 5, "product_quantity": 10, "product_price": 20})
            ] 

        order.create()


        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(order.id, 1)
        self.assertEqual(len(order.items), 2)
        orders = Order.all()
        self.assertEqual(len(orders), 1)
    
    def test_find_order(self):
        """Find an Order by ID"""
        orders = OrderFactory.create_batch(3)
        for order in orders:
            order.create()
        logging.debug(orders)
        # make sure they got saved
        self.assertEqual(len(Order.all()), 3)
        # find the 2nd order in the list
        order = Order.find(orders[1].id)
        self.assertIsNot(order, None)
        self.assertEqual(order.id, orders[1].id)
        self.assertEqual(order.customer_id, orders[1].customer_id)
        # TODO(ELF): Fix this so that it works with the date_order
        # self.assertEqual(order.date_order, orders[1].date_order)

    def test_create_order_with_items(self):
        """Create order with multiple items"""
        order = OrderWithItemsFactory(items=5)
        self.assertIsInstance(order, Order)
        self.assertTrue(len(order.items) == 5)
        for item in order.items:
            self.assertIsInstance(item, OrderItem)
    
    def test_update_order(self):
        """Update an order with empty id"""
        order = OrderFactory()
        order.create()
        item1 = OrderItemFactory.create(order=order)
        item2 = OrderItemFactory.create(order=order)
        
        self.assertEqual(order.id, 1)
        self.assertEqual(len(order.items), 2)

    def test_update_order_item_quantity(self):
        """Create order with multiple items"""
        order = OrderWithItemsFactory(items=1)
        order.create()

        self.assertIsInstance(order, Order)
        self.assertTrue(len(order.items) == 1)
        for item in order.items:
            self.assertIsInstance(item, OrderItem)
        
        origin_quantity = order.items[0].product_quantity 
        order.items[0].product_quantity =  order.items[0].product_quantity + 20 
        order.items[0].update()
        
        updated_order = Order.find_or_404(order.id)

        self.assertNotEqual(origin_quantity, updated_order.items[0].product_quantity)

    def test_delete_order_item(self):
        """Delete an order item"""
        order = OrderWithItemsFactory(items=2)
        order.create()

        self.assertIsInstance(order, Order)
        self.assertTrue(len(order.items) == 2)
        
        order.items[0].delete()
        
        updated_order = Order.find_or_404(order.id)

        self.assertEqual(len(updated_order.items), 1)

    def test_update_order_empty_id(self):
        """Update an order with empty id"""
        order = OrderFactory()
        order.create()
        self.assertEqual(order.id, 1)
        # Change it and save it
        original_id = order.id
        order.id = None
        
        with self.assertRaises(Exception) as e:
            order.update()


    def test_delete_a_order(self):
        """Delete an Order"""
        order = OrderFactory()
        order.create()
        self.assertEqual(len(Order.all()), 1)
        # delete the order and make sure it isn't in the database
        order.delete()
        self.assertEqual(len(Order.all()), 0)

    def test_serialize_a_order(self):
        """Test serialization of an Order"""
        order = OrderFactory()
        data = order.serialize()
        self.assertNotEqual(data, None)
        self.assertEqual(data["id"], order.id)
        self.assertIn("date_order", data)
        self.assertEqual(data["date_order"], order.date_order)
        self.assertIn("customer_id", data)

    def test_deserialize_an_order(self):
        """Test deserialization of an Order"""
        data = {
            "id": 1,
            "date_order": "02/22/2022",
            "customer_id": "2",
        }
        order = Order()
        order.deserialize(data)
        self.assertNotEqual(order, None)    
        self.assertEqual(order.date_order, "02/22/2022")
        self.assertEqual(order.customer_id, "2")

    def test_deserialize_an_order_item(self):
        """Test deserialization of an Order Item"""
        data = {
            "order_id": 1,
            "product_id": "5",
            "product_price": "10",
            "product_quantity": "2",
        }

        item = OrderItem()
        item.deserialize(data)
        self.assertNotEqual(item, None)    
        self.assertEqual(item.product_id, "5")
        self.assertEqual(item.product_price, "10")
        self.assertEqual(item.product_quantity, "2")

    def test_deserialize_an_order_item_missing_data(self):
        """Test deserialize of an Order Item"""
        data = {
            "order_id": 1,
            "product_price": "10",
            "product_quantity": "2",
        }

        item = OrderItem()
        self.assertRaises(DataValidationError, item.deserialize, data)
    
    def test_deserialize_order_item_bad_data(self):
        """Test deserialize of bad data"""
        data = "this is not a dictionary"
        item = OrderItem()
        self.assertRaises(DataValidationError, item.deserialize, data)

    def test_deserialize_missing_data(self):
        """Test deserialize of a Order with missing data"""
        data = {"id": 1, "customer_id": "1"}

        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, data)

    def test_deserialize_bad_data(self):
        """Test deserialize of bad data"""
        data = "this is not a dictionary"
        order = Order()
        self.assertRaises(DataValidationError, order.deserialize, data)

    def test_find_or_404_found(self):
        """Find or return 404 found"""
        orders = OrderFactory.create_batch(3)
        for order in orders:
            order.create()

        order = Order.find_or_404(orders[1].id)
        self.assertIsNot(order, None)
        self.assertEqual(order.id, orders[1].id)
        self.assertEqual(order.date_order, orders[1].date_order)
        self.assertEqual(order.customer_id, orders[1].customer_id)

    def test_find_or_404_not_found(self):
        """Find or return 404 NOT found"""
        self.assertRaises(NotFound, Order.find_or_404, 0)
