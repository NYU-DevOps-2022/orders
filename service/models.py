"""
Models for orders

All of the models are stored in this module
"""
import logging
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


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

    def __repr__(self):
        return f"<order id=[{self.id_order}]>"

    def create(self):
        """
        Creates a order_header to the database
        """
        logger.info("Creating %s", self.id_order)
        self.id_order = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates an order_header to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def update(self):
        """
        Updates an Order to the database
        """
        logger.info("Saving %s", self.id_order)
        if not self.id:
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
            "id_customer_order": self.id_customer_order
        }

    def deserialize(self, data):
        """
        Deserializes an order_header from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            # self.id_order = data["id_order"]
            self.date_order = data["date_order"]
            self.id_customer_order = data["id_customer_order"]
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
    def find(cls, by_id):
        """ Finds an order_header by its ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find an order_header by its id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_customer(cls, id_customer_order):
        """ Returns all order_header with the given customer id """
        logger.info("Processing name query for %s ...", id_customer_order)
        return cls.query.filter(cls.id_customer_order == id_customer_order)


# class order_detail(db.Model):
#     """
#     Class that represents a <order_detail>
#     """

#     app = None

#     # Table Schema
#     order_id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, nullable=False)
#     quantity_order = db.Column(db.Integer, default=0)
#     price_order = db.Column(db.DECIMAL(10, 2), default=0)

#     def __repr__(self):
#         return f"<order id=[{self.order_id}]>"

#     def create(self):
#         """
#         Creates an order_detail to the database
#         """
#         logger.info("Creating %s", self.name)
#         self.id = None  # id must be none to generate next primary key
#         db.session.add(self)
#         db.session.commit()

#     def save(self):
#         """
#         Updates an order_detail to the database
#         """
#         logger.info("Saving %s", self.name)
#         db.session.commit()

#     def delete(self):
#         """ Removes an order_detail from the data store """
#         logger.info("Deleting %s", self.name)
#         db.session.delete(self)
#         db.session.commit()

#     def serialize(self):
#         """ Serializes an order_detail into a dictionary """
#         return {
#             "order_id": self.order_id,
#             "product_id": self.product_id,
#             "quantity_order": self.quantity_order,
#             "price_order": self.price_order,
#         }

#     def deserialize(self, data):
#         """
#         Deserializes an order_detail from a dictionary

#         Args:
#             data (dict): A dictionary containing the resource data
#         """
#         try:
#             self.order_id = data["order_id"]
#             self.product_id = data["product_id"]
#             self.quantity_order = data["quantity_order"]
#             self.price_order = data["price_order"]

#         except KeyError as error:
#             raise DataValidationError(
#                 "Invalid order_detail: missing " + error.args[0]
#             )
#         except TypeError as error:
#             raise DataValidationError(
#                 "Invalid order_detail: body of request contained bad or no data"
#             )
#         return self

#     @classmethod
#     def init_db(cls, app):
#         """ Initializes the database session """
#         logger.info("Initializing database")
#         cls.app = app
#         # This is where we initialize SQLAlchemy from the Flask app
#         db.init_app(app)
#         app.app_context().push()
#         db.create_all()  # make our sqlalchemy tables

#     @classmethod
#     def all(cls):
#         """ Returns all of the order_detail in the database """
#         logger.info("Processing all order_detail")
#         return cls.query.all()

#     def find(cls, by_id):
#         """ Finds an order_detail by its ID """
#         logger.info("Processing lookup for id %s ...", by_id)
#         return cls.query.get(by_id)

#     @classmethod
#     def find_or_404(cls, by_id):
#         """ Find an order_detail by its id """
#         logger.info("Processing lookup or 404 for id %s ...", by_id)
#         return cls.query.get_or_404(by_id)

#     @classmethod
#     def find_by_name(cls, name):
#         """Returns all order_details with the given name

#         Args:
#             name (string): the name of the order_detail you want to match
#         """
#         logger.info("Processing name query for %s ...", name)
#         return cls.query.filter(cls.name == name)
