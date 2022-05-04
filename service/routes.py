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

import secrets
from asyncio.log import logger
import logging
from attr import validate
from flask import jsonify, request, url_for, make_response, abort
from flask_restx import Api, Resource, fields, reqparse, inputs
from werkzeug.exceptions import NotFound


from service.models import Order
from . import status  # HTTP Status Codes

# Import Flask application
from . import app


# Document the type of autorization required
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Api-Key'
    }
}

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
          description='This is a sample server for Order service.',
          default='orders',
          default_label='Order operations',
          doc='/apidocs', # default also could use doc='/apidocs/'
          authorizations=authorizations,
        #   prefix='/api'
         )


create_item_model = api.model('Item', {
    # 'id': fields.Integer,
    'product_id': fields.Integer,
    'product_price': fields.Float,
    'product_quantity': fields.Integer
})

item_model = api.inherit(
    'ItemModel',
    create_item_model,
    {
        'id': fields.String(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)


# Define the model so that the docs reflect what can be sent
create_model = api.model('Order', {
    'date_order': fields.Date(required=True,
                          description='The date when the order was placed'),
    'customer_id': fields.String(required=True,
                              description='The id of the customer for this order'),
    'item_list': fields.List(fields.Nested(create_item_model))
})

order_model = api.inherit(
    'OrderModel', 
    create_model,
    {
        'id': fields.String(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)



# query string arguments
order_args = reqparse.RequestParser()
order_args.add_argument('customer_id', type=str, required=False, help='List Order by customer id')
order_args.add_argument('date_order', type=str, required=False, help='The date when the order was placed')

######################################################################
# Authorization Decorator
######################################################################
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if 'X-Api-Key' in request.headers:
#             token = request.headers['X-Api-Key']

#         if app.config.get('API_KEY') and app.config['API_KEY'] == token:
#             return f(*args, **kwargs)
#         else:
#             return {'message': 'Invalid or missing token'}, 401
#     return decorated

######################################################################
# Function to generate a random API key (good for testing)
######################################################################
def generate_apikey():
    """ Helper function used when testing API keys """
    return secrets.token_hex(16)



######################################################################
# GET HEALTH CHECK
######################################################################
@app.route("/healthcheck")
def healthcheck():
    """Let them know our heart is still beating"""
    return make_response(jsonify(status=200, message="Healthy"), status.HTTP_200_OK)



######################################################################
#  PATH: /orders/{id}
######################################################################
@api.route('/orders/<id>')
@api.param('id', 'The Order identifier')
class OrderResource(Resource):
    """
    OrderResource class

    Allows the manipulation of a single Order
    GET /order{id} - Returns a Order with the id
    PUT ordert{id} - Update a Order with the id
    DELETE /order{id} -  Deletes a Order with the id
    """


    ######################################################################
    # GET AN ORDER INFO
    ######################################################################
    # @app.route("/orders/<int:id>", methods=["GET"])
    @api.doc('get_order')
    @api.response(404, 'Order not found')
    @api.marshal_with(order_model)
    def get(self, id):
        """
        Get info of an Order
        This endpoint will return an Order information based the id specified in the path
        """
        app.logger.info("Request to get order info with id: %s", id)
        order = Order.find_or_404(id)

        app.logger.info("Returning order: %s", order.id)
        return order.serialize(), status.HTTP_200_OK


    ###################################################################### 
    #  UPDATE AN Order
    ######################################################################
    @api.doc('update_orders')
    @api.response(404, 'Order not found')
    @api.response(400, 'The posted Order data was not valid')
    @api.expect(order_model)    
    @api.marshal_with(order_model)
    # @app.route("/orders/<int:id>", methods=["PUT"])
    def put(self, id):
        """     
        Update an order  
        """
        app.logger.info("Request to update order with id: %s", id)
        order = check_valid_order(id)
        order.deserialize(api.payload)
        order.id = id
        order.update()
        app.logger.info("Order with ID [%s] updated.", order.id)
        return order.serialize(), status.HTTP_200_OK


    ######################################################################
    # DELETE AN ORDER
    ######################################################################
    @api.doc('delete_orders')
    @api.response(204, 'Order deleted')
    # @token_required
    # @app.route("/orders/<int:id>", methods=["DELETE"])
    def delete(self, id):
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
                
        return "", status.HTTP_204_NO_CONTENT


######################################################################
#  PATH: /orders
######################################################################
@api.route('/orders', strict_slashes=False)
class OrderCollection(Resource):

    ######################################################################
    # LIST ALL ORDERS
    ######################################################################
    # @app.route("/orders", methods=["GET"])
    @api.doc('list_orders')
    @api.expect(order_args, validate=True)
    @api.marshal_list_with(order_model)
    def get(self):
        """Returns all of the Orders"""
        app.logger.info("Request for order list")
        args = order_args.parse_args()
        orders = []
        
        if args['customer_id'] is not None:
            app.logger.info('Filtering by customer: %s', args['customer_id'])
            orders = Order.find_by_customer(args['customer_id'])
        elif args['date_order'] is not None:
            app.logger.info('Filtering by order date: %s', args['date_order'])
            orders = Order.find_by_date_order(args['date_order'])
        else:
            app.logger.info('Returning unfiltered list.')            
            orders = Order.all()

        results = [order.serialize() for order in orders]
        app.logger.info("Returning %d orders", len(results))
        return results, status.HTTP_200_OK


    ######################################################################
    # ADD A NEW Order
    ######################################################################
    @api.doc('create_orders')
    @api.response(400, 'The posted data was not valid')
    @api.expect(create_model)
    @api.marshal_with(order_model, code=201)
    def post(self):
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
        # check_content_type("application/json")
        order = Order()
        
        app.logger.debug('Payload = %s', api.payload)
        order.deserialize(api.payload)
        order.create()
        message = order.serialize()
        location_url = api.url_for(OrderResource, id=order.id, _external=True)

        app.logger.info("Order with ID [%s] created.", order.id)
        
        return message, status.HTTP_201_CREATED, {"Location": location_url}


######################################################################
#  PATH: /orders/{id}/items
######################################################################

@api.route('/orders/<id>/items')
@api.param('id', 'The Order identifier')
class OrderItemResource(Resource):
    # @app.route("/orders/<int:id>/items", methods=["PUT"])
    @api.doc('get_order_items')
    @api.marshal_with(item_model)
    @api.response(404, 'Order not found')
    def get(self, id):
        app.logger.info("Request to see order items with id: %s", id)
        order = Order.find(id)
        if not order:
            abort(status.HTTP_404_NOT_FOUND, 'Order with id [{}] was not found.'.format(id))
        
        # order.id = id
        # for item in order.items:
        #     item.update()
        
        # app.logger.info("Order items for order with ID [%s] updated.", order.id)
        return [item.serialize() for item in order.items], status.HTTP_200_OK
        # return order.serialize(), status.HTTP_200_OK


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


# def check_content_type(media_type):
#     """Checks that the media type is correct"""
#     content_type = request.headers.get("Content-Type")
#     if content_type and content_type == media_type:
#         return
#     app.logger.error("Invalid Content-Type: %s", content_type)
#     abort(
#         status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
#         f"Content-Type must be {media_type}",
#     )
