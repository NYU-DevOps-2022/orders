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

import sys
import secrets
import logging
from functools import wraps
from flask import jsonify, request, url_for, make_response, render_template
from flask_restx import Api, Resource, fields, reqparse, inputs
from service.models import Pet, Gender, DataValidationError, DatabaseConnectionError
from . import app, status    # HTTP Status Codes


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

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Order Demo REST API Service',
          description='This is a sample server Order store server.',
          default='orders',
          default_label='Order shop operations',
          doc='/apidocs', # default also could use doc='/apidocs/'
          #authorizations=authorizations,
          prefix='/api'
         )

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

# Define the model so that the docs reflect what can be sent
create_model = api.model('Order_Items', {
    'Order_Items_id': fields.String(readOnly=True,
                          description='The id of the order_items'),
    'Product_Id': fields.String(required=True,
                              description='Name of the product'),
    'Product_Price': fields.String(required=True,
                                description='Product Price'),
    'Product_Quantity': fields.String(required=True,
                                description='Product Quantity')
})

order_model = api.inherit(
    'OrderModel', 
    create_model,
    {
    'id': fields.String(readOnly=True,
                            description='The unique id assigned internally by service')
    'Date_Order': fields.String(required=True,
                                description='Date Order')
    'Customer_id': fields.String(required=True,
                                description='Customer id')                    
    }
)

# query string arguments
Order_Items_args = reqparse.RequestParser()
Order_Items_args.add_argument('Order_Items_id', type=str, required=False, help='List Order Items by ID')
Order_Items_args.add_argument('Product_Id', type=str, required=False, help='List Order Items by Product_Id')
Order_Items_args.add_argument('Product_Price', type=inputs.boolean, required=False, help='List Order Items price')

######################################################################
# Special Error Handlers
######################################################################
@api.errorhandler(DataValidationError)
def request_validation_error(error):
    """ Handles Value Errors from bad data """
    message = str(error)
    app.logger.error(message)
    return {
        'status_code': status.HTTP_400_BAD_REQUEST,
        'error': 'Bad Request',
        'message': message
    }, status.HTTP_400_BAD_REQUEST

@api.errorhandler(DatabaseConnectionError)
def database_connection_error(error):
    """ Handles Database Errors from connection attempts """
    message = str(error)
    app.logger.critical(message)
    return {
        'status_code': status.HTTP_503_SERVICE_UNAVAILABLE,
        'error': 'Service Unavailable',
        'message': message
    }, status.HTTP_503_SERVICE_UNAVAILABLE


######################################################################
# Function to generate a random API key (good for testing)
######################################################################
def generate_apikey():
    """ Helper function used when testing API keys """
    return secrets.token_hex(16)


######################################################################
#  PATH: /orders/{id}
######################################################################
@api.route('/orders/<order_id>')
@api.param('order_id', 'The Order identifier')
class OrderResource(Resource):
    """
    OrderResource class

    Allows the manipulation of a single Order
    GET /orders/{id} - Returns a Order with the id
    PUT /orders/{id} - Update an Order with the id
    DELETE /orders/{id} -  Deletes an Order with the id
    """
######################################################################
#  PATH: /orders
######################################################################
@api.route('/orders/<order_id>')
@api.param('order_id', 'The Order identifier')
class OrderResource(Resource):
    """ Handles all interactions with collections of Pets """
######################################################################
# LIST ALL ORDERS
######################################################################
 @api.doc('list_orders')
    @api.expect(order_args, validate=True)
    @api.marshal_list_with(order_model)
    def get(self):
    """Returns all of the Orders"""
    app.logger.info("Request for order list")
    orders = []
    customer = request.args.get("customer")
    date_order = request.args.get("date_order")

    if customer:
        orders = Order.find_by_customer(customer)
        # logger.info("Search order by customer id: %d", customer)
        if orders.count() == 0:
            abort(status.HTTP_400_BAD_REQUEST)
    if date_order:
        orders = Order.find_by_date_order(date_order)
    else:
        orders = Order.all()

    results = [order.serialize() for order in orders]
    app.logger.info("Returning %d orders", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)

 #------------------------------------------------------------------
    # RETRIEVE AN ORDER
    #------------------------------------------------------------------
 @api.doc('get_orders')
 @api.response(404, 'Order not found')
 @api.marshal_with(order_model)
 def get(self, order_id):
        """
    Get info of an Order
    This endpoint will return an Order information based the id specified in the path
    """
    app.logger.info("Request to get order info with id: %s", id)
    order = Order.find_or_404(id)

    # if not order:
    #     raise NotFound(f"Order with id '{id}' was not found.")

    app.logger.info("Returning order: %s", order.id)
    return order.serialize(), (status.HTTP_200_OK)



######################################################################
# ADD A NEW Order
######################################################################
@app.route("/orders", methods=["POST"])
def create_orders():
    """
    Creates an Order
    This endpoint will create an Order based the data in the body that is posted
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
    app.logger.info("Request to create an order")
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

    @api.doc('update_orders') #security='apikey'
    @api.response(404, 'Order not found')
    @api.response(400, 'The posted Order data was not valid')
    @api.expect(create_model)
    @api.marshal_with(create_model)
    #@token_required
    def put(self, order_id):
            """     
    Update an order  
    """
    app.logger.info("Request to update pet with id: %s", id)
    check_content_type("application/json")
    order = check_valid_order(id)
    order.deserialize(request.get_json())
    order.id = id
    order.update()
    app.logger.info("Order with ID [%s] updated.", order.id)
    return order.serialize(), status.HTTP_200_OK)


######################################################################
# DELETE AN ORDER
######################################################################

@api.doc('delete_orders')
@api.response(204, 'Order deleted')
   # @token_required
def delete(self, order_id):
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
    return '', status.HTTP_204_NO_CONTENT


######################################################################
#  UPDATE Order items
######################################################################

 @api.doc('update_orders')
 @api.response(404, 'Order not found')
    @api.response(400, 'The posted Order data was not valid')
    @api.expect(order_model)
    @api.marshal_with(order_model)
    #@token_required
    def put(self, id):
        """
       
    app.logger.info("Request to update order items with id: %s", id)
    check_content_type("application/json")
    order = check_valid_order(id)
    order.deserialize(request.get_json())
    order.id = id
    for item in order.items:
        item.update()
    app.logger.info("Order items for order with ID [%s] updated.", order.id)
    return make_response("", status.HTTP_204_NO_CONTENT)


######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################

def check_valid_order(id):
    order = Order.find(id)
    if not order:
        raise NotFound(f"order with id '{id}' was not found.")
    return order


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
