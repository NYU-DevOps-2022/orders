"""
Test cases for YourResourceModel Model

"""
import logging
import unittest
import os
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
        

