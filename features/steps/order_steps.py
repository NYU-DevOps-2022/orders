######################################################################
# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
######################################################################

"""
Order Steps

Steps file for Order.feature

For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import json
import requests
from behave import given
from compare import expect

@given('the following orders')
def step_impl(context):
    """ Delete all Order and load new ones """
    headers = {'Content-Type': 'application/json'}
    # list all of the orders and delete them one by one
    context.resp = requests.get(context.base_url + '/orders', headers=headers)
    expect(context.resp.status_code).to_equal(200)
    for order in context.resp.json():
        context.resp = requests.delete(context.base_url + '/orders/' + str(order["id"]), headers=headers)
        expect(context.resp.status_code).to_equal(204)
    
    # load the database with new orders
    create_url = context.base_url + '/orders'
    for row in context.table:
        data = {
            "customer_id": row['customer'],
            "date_order": row['date']
        }
        payload = json.dumps(data)
        context.resp = requests.post(create_url, data=payload, headers=headers)
        expect(context.resp.status_code).to_equal(201)
