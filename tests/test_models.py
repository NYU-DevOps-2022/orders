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
import logging
import os
import unittest
from werkzeug.exceptions import NotFound
from service.models import Order, DataValidationError, db
from service import app
from service.models import Order, db

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/testdb"
)


######################################################################
#  P E T   M O D E L   T E S T   C A S E S
######################################################################
class TestPetModel(unittest.TestCase):
    """Test Cases for Order Model"""

    @classmethod
    def setUpClass(cls):
        """This runs once before the entire test suite"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
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
        order = Order(id_order=1, date_order='02/22/2022', id_customer_order=1)
        self.assertIsNotNone(order)
        self.assertEqual(order.id_order, 1)
        self.assertEqual(order.date_order, '02/22/2022')

    def test_add_a_order(self):
        """Create a order and add it to the database"""
        orders = Order.all()
        self.assertEqual(orders, [])
        order = Order(id_order=1, date_order='02/22/2022', id_customer_order=1)
        order.create()
        # Asert that it was assigned an id and shows up in the database
        self.assertEqual(order.id_order, 1)
        orders = Order.all()
        self.assertEqual(len(orders), 1)


    def test_find_order(self):
        """Find a Order by ID"""
        orders = OrderFactory.create_batch(3)
        for order in orders:
            order.create()
        logging.debug(orders)
        # make sure they got saved
        self.assertEqual(len(Order.all()), 3)
        # find the 2nd order in the list
        order = Order.find(orders[1].id_order)
        self.assertIsNot(order, None)
        self.assertEqual(order.id_order, orders[1].id_order)
        self.assertEqual(order.id_customer_order, orders[1].id_customer_order)
        self.assertEqual(order.date_order, orders[1].date_order)


    # def test_update_a_order(self):
    #     """Update a Pet"""
    #     order = PetFactory()
    #     logging.debug(order)
    #     order.create()
    #     logging.debug(order)
    #     self.assertEqual(order.id, 1)
    #     # Change it an save it
    #     order.category = "k9"
    #     original_id = order.id
    #     order.update()
    #     self.assertEqual(order.id, original_id)
    #     self.assertEqual(order.category, "k9")
    #     # Fetch it back and make sure the id hasn't changed
    #     # but the data did change
    #     orders = Pet.all()
    #     self.assertEqual(len(orders), 1)
    #     self.assertEqual(orders[0].id, 1)
    #     self.assertEqual(orders[0].category, "k9")

    # def test_delete_a_order(self):
    #     """Delete a Pet"""
    #     order = PetFactory()
    #     order.create()
    #     self.assertEqual(len(Pet.all()), 1)
    #     # delete the order and make sure it isn't in the database
    #     order.delete()
    #     self.assertEqual(len(Pet.all()), 0)

    # def test_serialize_a_order(self):
    #     """Test serialization of a Pet"""
    #     order = PetFactory()
    #     data = order.serialize()
    #     self.assertNotEqual(data, None)
    #     self.assertIn("id", data)
    #     self.assertEqual(data["id"], order.id)
    #     self.assertIn("name", data)
    #     self.assertEqual(data["name"], order.name)
    #     self.assertIn("category", data)
    #     self.assertEqual(data["category"], order.category)
    #     self.assertIn("available", data)
    #     self.assertEqual(data["available"], order.available)
    #     self.assertIn("gender", data)
    #     self.assertEqual(data["gender"], order.gender.name)

    # def test_deserialize_a_order(self):
    #     """Test deserialization of a Pet"""
    #     data = {
    #         "id": 1,
    #         "name": "kitty",
    #         "category": "cat",
    #         "available": True,
    #         "gender": "Female",
    #     }
    #     order = Pet()
    #     order.deserialize(data)
    #     self.assertNotEqual(order, None)
    #     self.assertEqual(order.id, None)
    #     self.assertEqual(order.name, "kitty")
    #     self.assertEqual(order.category, "cat")
    #     self.assertEqual(order.available, True)
    #     self.assertEqual(order.gender, Gender.Female)

    # def test_deserialize_missing_data(self):
    #     """Test deserialization of a Pet with missing data"""
    #     data = {"id": 1, "name": "kitty", "category": "cat"}
    #     order = Pet()
    #     self.assertRaises(DataValidationError, order.deserialize, data)

    # def test_deserialize_bad_data(self):
    #     """Test deserialization of bad data"""
    #     data = "this is not a dictionary"
    #     order = Pet()
    #     self.assertRaises(DataValidationError, order.deserialize, data)

    # def test_deserialize_bad_available(self):
    #     """ Test deserialization of bad available attribute """
    #     test_order = PetFactory()
    #     data = test_order.serialize()
    #     data["available"] = "true"
    #     order = Pet()
    #     self.assertRaises(DataValidationError, order.deserialize, data)

    # def test_deserialize_bad_gender(self):
    #     """ Test deserialization of bad gender attribute """
    #     test_order = PetFactory()
    #     data = test_order.serialize()
    #     data["gender"] = "male" # wrong case
    #     order = Pet()
    #     self.assertRaises(DataValidationError, order.deserialize, data)


    # def test_find_by_category(self):
    #     """Find Pets by Category"""
    #     Pet(name="fido", category="dog", available=True).create()
    #     Pet(name="kitty", category="cat", available=False).create()
    #     orders = Pet.find_by_category("cat")
    #     self.assertEqual(orders[0].category, "cat")
    #     self.assertEqual(orders[0].name, "kitty")
    #     self.assertEqual(orders[0].available, False)

    # def test_find_by_name(self):
    #     """Find a Pet by Name"""
    #     Pet(name="fido", category="dog", available=True).create()
    #     Pet(name="kitty", category="cat", available=False).create()
    #     orders = Pet.find_by_name("kitty")
    #     self.assertEqual(orders[0].category, "cat")
    #     self.assertEqual(orders[0].name, "kitty")
    #     self.assertEqual(orders[0].available, False)

    # def test_find_by_availability(self):
    #     """Find Pets by Availability"""
    #     Pet(name="fido", category="dog", available=True).create()
    #     Pet(name="kitty", category="cat", available=False).create()
    #     Pet(name="fifi", category="dog", available=True).create()
    #     orders = Pet.find_by_availability(False)
    #     order_list = [order for order in orders]
    #     self.assertEqual(len(order_list), 1)
    #     self.assertEqual(orders[0].name, "kitty")
    #     self.assertEqual(orders[0].category, "cat")
    #     orders = Pet.find_by_availability(True)
    #     order_list = [order for order in orders]
    #     self.assertEqual(len(order_list), 2)

    # def test_find_by_gender(self):
    #     """Find Pets by Gender"""
    #     Pet(name="fido", category="dog", available=True, gender=Gender.Male).create()
    #     Pet(
    #         name="kitty", category="cat", available=False, gender=Gender.Female
    #     ).create()
    #     Pet(name="fifi", category="dog", available=True, gender=Gender.Male).create()
    #     orders = Pet.find_by_gender(Gender.Female)
    #     order_list = [order for order in orders]
    #     self.assertEqual(len(order_list), 1)
    #     self.assertEqual(orders[0].name, "kitty")
    #     self.assertEqual(orders[0].category, "cat")
    #     orders = Pet.find_by_gender(Gender.Male)
    #     order_list = [order for order in orders]
    #     self.assertEqual(len(order_list), 2)

    # def test_find_or_404_found(self):
    #     """Find or return 404 found"""
    #     orders = PetFactory.create_batch(3)
    #     for order in orders:
    #         order.create()

    #     order = Pet.find_or_404(orders[1].id)
    #     self.assertIsNot(order, None)
    #     self.assertEqual(order.id, orders[1].id)
    #     self.assertEqual(order.name, orders[1].name)
    #     self.assertEqual(order.available, orders[1].available)

    # def test_find_or_404_not_found(self):
    #     """Find or return 404 NOT found"""
    #     self.assertRaises(NotFound, Pet.find_or_404, 0)
