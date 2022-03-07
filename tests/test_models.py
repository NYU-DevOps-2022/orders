"""
Test cases for YourResourceModel Model

"""
import logging
import unittest
import os
import flask_sqlalchemy
from  werkzeug import exceptions
from service.models import YourResourceModel, DataValidationError, db

######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################
class TestYourResourceModel(unittest.TestCase):
    """ Test Cases for YourResourceModel Model """

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
        self.your_resource_model = YourResourceModel()

    def tearDown(self):
        """ This runs after each test """
        self.your_resource_model = None

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create(self):
        """ Test the create method in YourResourceModel.
        Currently this test only tests the return value of the create method.
        #TODO(ELF): check that the db has been properly updated 
        # as a result of this function call."""
        self.assertIsNone(self.your_resource_model.create())

    # def test_save(self):
    #     """Test the save method in YourResourceModel."""
    #     self.assertIsNone(self.yrm.save())

    # def test_delete(self):
    #     """Test the save method in YourResourceModel."""
    #     self.assertIsNone(self.yrm.delete())

    def test_serialize(self):
        self.your_resource_model.id = "12345"
        self.your_resource_model.name = "Ed"
        self.assertEqual({"id": "12345", "name": "Ed"}, self.your_resource_model.serialize())

    def test_deserialize(self):
        self.assertEqual(self.your_resource_model, self.your_resource_model.deserialize({"id": "12345", "name": "Ed"}))
        self.assertEqual("Ed", self.your_resource_model.name)
    
    def test_init_db(self):
        self.your_resource_model.init_db=unittest.mock.MagicMock(return_value=None)
        app=unittest.mock.Mock()
        self.assertIsNone(self.your_resource_model.init_db(app))

    def test_all(self):
        self.your_resource_model.all=unittest.mock.MagicMock(return_value=None)
        self.assertEqual(None, self.your_resource_model.all())

    def test_find(self):
        self.your_resource_model.find=unittest.mock.MagicMock(return_value=None)
        self.assertEqual(None, self.your_resource_model.find())

    def test_find_or_404(self):
        # self.your_resource_model.find_or_404=unittest.mock.MagicMock(return_value=None)
        with self.assertRaises(exceptions.NotFound):
            self.your_resource_model.find_or_404(123) 
        # self.assertEqual(None, self.your_resource_model.find_or_404(123))

    #TODO: FIX find_by_name

    def test_find_by_name(self):
        pass
        # self.your_resource_model.query.filter=unittest.mock.MagicMock(return_value=None)
        # things=flask_sqlalchemy.BaseQuery()
        # things.filter=unittest.mock.MagicMock(return_value=None)
        # self.assertEqual(things, self.your_resource_model.find_by_name("margarita"))

