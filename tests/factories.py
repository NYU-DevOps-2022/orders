# Copyright 2016, 2019 John J. Rofrano. All Rights Reserved.
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

"""
Test Factory to make fake objects for testing
Reference: https://simpleit.rocks/python/django/setting-up-a-factory-for-one-to-many-relationships-in-factoryboy/

"""
from pydoc import ModuleScanner
from datetime import datetime, timezone
from service.models import Order, OrderItem
import factory
from factory.fuzzy import FuzzyChoice
from factory.fuzzy import FuzzyDateTime
from factory.fuzzy import FuzzyInteger
from factory.fuzzy import FuzzyFloat

starting_seq_num = 1

class OrderFactory(factory.Factory):
    """Creates fake orders that you don't have to feed"""

    class Meta:
        model = Order
    factory
    id = factory.Sequence(lambda n: n)
    date_order = FuzzyDateTime(datetime(2020, 1, 1, tzinfo=timezone.utc))
    customer_id = FuzzyInteger(1, 999)

    @classmethod
    def _setup_next_sequence(cls):      
        # Instead of defaulting to starting with 0, start with starting_seq_num.
        return starting_seq_num

class OrderItemFactory(factory.Factory):
    """Creates fake orders that you don't have to feed"""

    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    id = factory.Sequence(lambda n: n)
    product_id = FuzzyInteger(1, 999)
    product_quantity = FuzzyInteger(1, 10)
    product_price = FuzzyFloat(0.5, 10.0)


class OrderWithItemsFactory(OrderFactory):

    @factory.post_generation
    def items(obj, create, extracted, **kwargs):
        """
        If called like: OrderFactory(items=4) it generates an Order with 4
        items.  If called without `items` argument, it generates a
        random amount of items for this order
        """
        if not create:
            # Build, not create related
            return

        if extracted:
            for n in range(extracted):
                OrderItemFactory(order=obj)
        else:
            import random
            number_of_units = random.randint(1, 10)
            for n in range(number_of_units):
                OrderItemFactory(order=obj)
