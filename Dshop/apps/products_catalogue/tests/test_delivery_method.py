import pytest
from django.urls import reverse
from apps.products_catalogue.models import DeliveryMethod, Order
from rest_framework.test import APIClient

@pytest.fixture
def standard_delivery_method():
    return DeliveryMethod.objects.create(name='Standard', price=10.00)


@pytest.mark.django_db
def test_delivery_method_creation():
    assert 0 == DeliveryMethod.objects.count()
    method = DeliveryMethod.objects.create(name='Standard', price=10.00) 
    tested_method = DeliveryMethod.objects.get(id=method.id)
    assert tested_method.name == 'Standard'  
    assert tested_method.price == 10.00    

@pytest.mark.django_db
def test_add_to_cart_then_order(ten_tv_products, standard_delivery_method):
    tv_product_1 = ten_tv_products[0] # expected price 599.00 * 2 = 1198
    tv_product_2 = ten_tv_products[1] # expected price 899.00 * 10 = 8990
    data = {
        'items': [ {'product_pk': tv_product_1.pk, 'quantity': 2}, {'product_pk': tv_product_2.pk, 'quantity': 10},  ]
    }
    api_client = APIClient()
    response = api_client.post(reverse("api_cart"), data)
    request = response.request
    print(response.data)
    order = Order.create_cart(request=request, delivery=standard_delivery_method)
    
    # tutaj wychodzenie z koszyka
    assert response.status_code == 201
    assert order.delivery_name == "Standard"
    assert order.delivery_price == 10
    assert order.cart_total == 1190 + 8990
    assert order.total_sum == 10 + 1198 + 8990
   