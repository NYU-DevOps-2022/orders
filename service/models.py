"""
Models for orders

All of the models are stored in this module
"""
from asyncio.windows_events import NULL
import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass

class customers(db.Model):
    """
    Class that represents a <customers>
    """

    app = None

    # Table Schema
    id_customer = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.varchar(45), nullable=False)

    def __repr__(self):
        return "<customers %r id=[%s]>" % (self.name, self.id_customer)
    
    def serialize(self):
        """ Serializes a customers into a dictionary """
        return {"id_customer": self.id_customer, "name": self.name}

    def deserialize(self, data: dict):
        """
        Deserializes a customers from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.id_customer = data["id_customer"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid customers: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid customers: body of request contained bad or no data"
            )
        return self
    


    

class products(db.Model):
    """
    Class that represents a <products>
    """

    app = None

    # Table Schema
    id_product = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.varchar(45), nullable=False)
    Price = db.Column(db.varchar(45), nullable=False)
    name = db.Column(db.varchar(45), nullable=False)


    def __repr__(self):
        return "<products %r id=[%s]>" % (self.name, self.id_product)
    
    def serialize(self):
        """ Serializes a products into a dictionary """
        return {
            "id_product" : self.id_product,
            "quantity" : self.quantity,
            "price" : self.Price,
            "name" : self.name,
        }

    def deserialize(self, data: dict):
        """
        Deserializes a products from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.name = data["name"]
            self.id_product = data["id_product"]
            self.Price = data["price"]
            self.quantity = data["quantity"]
        except KeyError as error:
            raise DataValidationError(
                "Invalid products: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid products: body of request contained bad or no data"
            )
        return self
    



class order_header(db.Model):
    """
    Class that represents a <your resource model name>
    """

    app = None

    # Table Schema
    id_order = db.Column(db.Integer, primary_key=True)
    date_order = db.Column(db.DateTime(),default=datetime.now)
    id_customer_order = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<order id=[%s]>" % (self.id)

    def create(self):
        """
        Creates a order_header to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a order_header to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a order_header from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a order_header into a dictionary """
        return {
            "id_order" : self.id_order,
            "date_order" : self.date_order,
            "id_customer_order" : self.id_customer_order
        }

    def deserialize(self, data):
        """
        Deserializes a order_header from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.id_order = data["id_order"]
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
        """ Returns all of the order_header in the database """
        logger.info("Processing all order_header")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a order_header by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a order_header by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all order_header with the given name

        Args:
            name (string): the name of the order_header you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)


class order_detail(db.Model):
    """
    Class that represents a <order_detail>
    """

    app = None

    # Table Schema
    order_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity_order = db.Column(db.Integer, default=NULL)
    price_order = db.Column(db.DECIMAL(10, 2), default=NULL)

    def __repr__(self):
        return "<order id=[%s]>" % (self.order_id)

    def create(self):
        """
        Creates a order_detail to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    def save(self):
        """
        Updates a order_detail to the database
        """
        logger.info("Saving %s", self.name)
        db.session.commit()

    def delete(self):
        """ Removes a order_detail from the data store """
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """ Serializes a order_detail into a dictionary """
        return {
            "order_id" : self.order_id,
            "product_id" : self.product_id,
            "quantity_order" : self.quantity_order,
            "price_order" : self.price_order,
        }

    def deserialize(self, data):
        """
        Deserializes a order_detail from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.order_id = data["order_id"]
            self.product_id = data["product_id"]
            self.quantity_order = data["quantity_order"]
            self.price_order = data["price_order"]

        except KeyError as error:
            raise DataValidationError(
                "Invalid order_detail: missing " + error.args[0]
            )
        except TypeError as error:
            raise DataValidationError(
                "Invalid order_detail: body of request contained bad or no data"
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
        """ Returns all of the order_detail in the database """
        logger.info("Processing all order_detail")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """ Finds a order_detail by it's ID """
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.get(by_id)

    @classmethod
    def find_or_404(cls, by_id):
        """ Find a order_detail by it's id """
        logger.info("Processing lookup or 404 for id %s ...", by_id)
        return cls.query.get_or_404(by_id)

    @classmethod
    def find_by_name(cls, name):
        """Returns all order_detail with the given name

        Args:
            name (string): the name of the order_detail you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name)

