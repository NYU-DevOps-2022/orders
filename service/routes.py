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

from asyncio.log import logger
import logging
from flask import jsonify, request, url_for, make_response, abort
from werkzeug.exceptions import NotFound

from service.models import Order
from . import status  # HTTP Status Codes

# Import Flask application
from . import app


######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/healthcheck")
def healthcheck():
    """Let them know our heart is still beating"""
    return make_response(jsonify(status=200, message="Healthy"), status.HTTP_200_OK)


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Base URL for our service"""
    return app.send_static_file("index.html")


# ######################################################################
# # GET INDEX
# ######################################################################
# @app.route("/")
# def index():
#     """ Root URL response """
#     app.logger.info("Request for Root URL")
#     return (
#         jsonify(
#             name="Order Demo REST API Service",
#             version="1.0",
#             paths=url_for("list_orders", _external=True),
#         ),
#         status.HTTP_200_OK,
#     )


######################################################################
# LIST ALL ORDERS
######################################################################
@app.route("/orders", methods=["GET"])
def list_orders():
    """Returns all of the Orders"""
    app.logger.info("Request for order list")

    orders = []
    customer = request.args.get("customer")
    
    if customer:
        orders = Order.find_by_customer(customer)
        logger.info("Search order by customer id: %d", customer)
        if orders.count() == 0:
            abort(status.HTTP_400_BAD_REQUEST)
    else:
        orders = Order.all()

    results = [order.serialize() for order in orders]
    app.logger.info("Returning %d orders", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)


######################################################################
# GET AN ORDER INFO
######################################################################

@app.route("/orders/<int:id>", methods=["GET"])
def get_order(id):
    """
    Get info of an Order
    This endpoint will return an Order information based the id specified in the path
    """
    app.logger.info("Request to get order info with id: %s", id)
    order = Order.find_or_404(id)

    # if not order:
    #     raise NotFound(f"Order with id '{id}' was not found.")

    app.logger.info("Returning order: %s", order.id)
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW Order
######################################################################
@app.route("/orders", methods=["POST"])
def create_orders():
    """
    Creates a Order
    This endpoint will create a Order based the data in the body that is posted
    e.g:
    curl --location --request POST 'http://localhost:8000/orders' \
        --header 'Content-Type: application/json' \
        --data-raw '{ 
            "date_order":"02/21/2022", 
            "customer_id":"3", 
            "item_list":[    
                {
                    "product_id": "1",
                    "product_quantity": "3",
                    "product_price": "5"
                },
                {
                    "product_id": "2",
                    "product_quantity": "10",
                    "product_price": "5"
                }
            ]
        }'
    """
    app.logger.info("Request to create a order")
    check_content_type("application/json")
    order = Order()
    order.deserialize(request.get_json())
    order.create()
    message = order.serialize()
    location_url = url_for("get_order", id=order.id, _external=True)

    app.logger.info("Order with ID [%s] created.", order.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


###################################################################### 
#  UPDATE AN Order
######################################################################

@app.route("/orders/<int:id>", methods=["PUT"]) 
def update_orders(id):     
    """     
    Update an order  
    """     
    app.logger.info("Request to update pet with id: %s", id)     
    check_content_type("application/json")     
    order = Order.find(id)
    if not order:         
        raise NotFound(f"order with id '{id}' was not found.")     
    order.deserialize(request.get_json())     
    order.id = id    
    order.update()      
    app.logger.info("Order with ID [%s] updated.", order.id)     
    return make_response(jsonify(order.serialize()), status.HTTP_200_OK) 


######################################################################
# DELETE AN ORDER
######################################################################

@app.route("/orders/<int:id>", methods=["DELETE"])
def delete_pets(id):
    """
    Delete an Order
    This endpoint will delete an Order based the id specified in the path
    e.g:
    curl -X DELETE 'http://localhost:8000/orders/1'

    """
    app.logger.info("Request to delete order with id: %s", id)
    order = Order.find(id)
    if order:
        # order_detail.delete()
        order.delete()

    app.logger.info("Order with ID [%s] delete complete.", id)
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
    """ Initializes the SQLAlchemy app """
    global app
    Order.init_db(app)


def check_content_type(media_type):
    """Checks that the media type is correct"""
    content_type = request.headers.get("Content-Type")
    if content_type and content_type == media_type:
        return
    app.logger.error("Invalid Content-Type: %s", content_type)
    abort(
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
        f"Content-Type must be {media_type}",
    )
