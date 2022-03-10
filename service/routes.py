"""
My Service

Describe what your service does here
"""

"""
Order Store Service
Paths:
------
GET /orders - Returns a list all of the Orders
GET /orders/{id} - Returns the Order with a given id number
POST /orders - creates a new Order record in the database
PUT /orders/{id} - updates a Order record in the database
DELETE /orders/{id} - deletes a Order record in the database
"""

from flask import jsonify, make_response
from werkzeug.exceptions import NotFound

from service.models import Order
from . import status  # HTTP Status Codes


# Import Flask application

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
            # paths=url_for("list_order", _external=True),
        ),
        status.HTTP_200_OK,
    )


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Order.init_db(app)


######################################################################
# GET AN ORDER INFO
######################################################################

@app.route("/orders/<int:id_order>", methods=["GET"])
def get_order(id_order):
    """
    Get info of an Order
    This endpoint will return an Order information based the id specified in the path
    """
    app.logger.info("Request to get order info with id: %s", id_order)
    order = Order.find(id_order)

    if not order:
        raise NotFound("Order with id '{}' was not found.".format(id_order))

    app.logger.info("Returning order: %s", order.id)
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE AN ORDER
######################################################################

@app.route("/orders/<int:id_order>", methods=["DELETE"])
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
