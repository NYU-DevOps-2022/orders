"""
My Service

Describe what your service does here
"""

import os
import sys
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from werkzeug.exceptions import NotFound
from . import status  # HTTP Status Codes

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import  DataValidationError, order_detail, order_header

# Import Flask application
from . import app

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    app.logger.info("Request for Root URL")
    return (
        jsonify(
            name="Order Demo REST API Service",
            version="1.0",
            paths=url_for("list_order", _external=True),
        ),
        status.HTTP_200_OK,
    )

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    order_header.init_db(app)
    order_detail.init_db(app)



######################################################################
# UPDATE AN EXISTING ORDER
######################################################################
@app.route("/order/<int:id_order>", methods=["PUT"])
def update_orders(id_order):
    """
    Update an Order
    This endpoint will update an Order based the body that is posted
    """
    app.logger.info("Request to update order with id: %s", id_order)
    check_content_type("application/json")
    order_detail = order_detail.find(id_order)
    if not order_detail:
        raise NotFound("Order with id '{}' was not found.".format(id_order))
    order_detail.deserialize(request.get_json())
    order_detail.order_id = id_order
    order_detail.update()

    app.logger.info("Order with ID [%s] updated.", order_detail.id_order)
    return make_response(jsonify(order_detail.serialize()), status.HTTP_200_OK)



######################################################################
# DELETE AN ORDER
######################################################################

@app.route("/order/<int:id_order>", methods=["DELETE"])
def delete_pets(id_order):
    """
    Delete an Order
    This endpoint will delete an Order based the id specified in the path
    """
    app.logger.info("Request to delete order with id: %s", id_order)
    order = order_detail.find(id_order)
    if order:
        order_detail.delete()
        order_header.delete()

    app.logger.info("Order with ID [%s] delete complete.", id_order)
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        "Content-Type must be {}".format(media_type),
    )