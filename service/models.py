"""
Models for orders

All of the models are stored in this module
"""
from curses import has_key
import json
import logging
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from . import app
# logger = logging.getLogger("flask.app")
logger = app.logger

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

def init_db(app):
    """Initialize the SQLAlchemy app"""
    Order.init_db(app)


class DataValidationError(Exception):
    """ Used for a data validation errors when deserializing """

    pass


class Order(db.Model):
    """
    Class that represents a <your resource model name>
    """
    app = None

    # Table Schema
    id_order = db.Column(db.Integer, primary_key=True)
    date_order = db.Column(db.DateTime(), default=datetime.now)
    id_customer_order = db.Column(db.Integer, nullable=False)

    # Relationship
    items = db.relationship("OrderItem", back_populates="order", cascade="all, delete",passive_deletes=True)

    def __repr__(self):
        return f"<order id=[{self.id_order}]>"

    def create(self):
        """
        Creates a order_header to the database
        """
        logger.info("Creating %s", self.id_order)
        #todo: Change id_order to id
        self.id_order = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

        if hasattr(self,'item_list'):
            for item in self.item_list:
                order_item = OrderItem()
                item['order_id'] = self.id_order
                order_item.deserialize(item)
                order_item.create()

    def update(self):
        """
        Updates an Order to the database
        """
        logger.info("Saving %s", self.id_order)
        if not self.id_order:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes an order_header from the data store """
        logger.info("Deleting %s", self.id_order)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes an order_header into a dictionary """
        return {
            "id_order": self.id_order,
            "date_order": self.date_order,
            "id_customer_order": self.id_customer_order,
            "items" : [item.serialize() for item in self.items]
        }

    def deserialize(self, data):
        """
        Deserializes an order_header from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.date_order = data["date_order"]
            self.id_customer_order = data["id_customer_order"]

            if hasattr(data, "item_list"):
                self.item_list = data["item_list"]

        except KeyError as error:
            raise DataValidationError(
                "Invalid order_header: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid order_header: body of request contained bad or no data"
            )
        return self

    @classmethod
    def init_db(cls, app):
        """ Initializes the database session """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the order_headers in the database """
        logger.info("Processing all order_header")
        return cls.query.all()

    @classmethod
    def find(cls, id_order):
        """ Finds an order_header by its ID """
        logger.info("Processing lookup for id %s ...", id_order)
        return cls.query.get(id_order)

    @classmethod
    def find_or_404(cls, id_order):
        """ Find an order_header by its id """
        logger.info("Processing lookup or 404 for id %s ...", id_order)
        return cls.query.get_or_404(id_order)

    @classmethod
    def find_by_customer(cls, id_customer_order):
        """ Returns all order_header with the given customer id """
        logger.info("Processing name query for %s ...", id_customer_order)
        return cls.query.filter(cls.id_customer_order == id_customer_order)

class OrderItem(db.Model):
    """
    Class that represents a <your resource model name>
    """
    app = None

    # Table Schema
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id_order', ondelete="CASCADE"))
    product_id = db.Column(db.Integer, nullable=False)
    product_price = db.Column(db.DECIMAL(10, 2), default=0)
    product_quantity = db.Column(db.Integer, nullable=False)

    # Relationship
    order = db.relationship("Order", back_populates="items")
    
    def __repr__(self):
        return f"<id=[{self.id}]>"

    def create(self):
        logger.info("Creating %s", self.id)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()


    def update(self):
        """
        Updates an orderitem to the database
        """
        logger.info("Saving %s", self.id)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes an orderitem from the data store """
        logger.info("Deleting %s", self.id)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a product into a dictionary """
        return {
            "id": self.id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "product_price": self.product_price,
            "product_quantity": self.product_quantity,
        }

    def deserialize(self, data):
        """
        Deserializes an order_header from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.order_id = data["order_id"]
            self.product_id = data["product_id"]
            self.product_price = data["product_price"]
            self.product_quantity = data["product_quantity"]

        except KeyError as error:
            raise DataValidationError(
                "Invalid product: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid product: body of request contained bad or no data"
            )
        return self