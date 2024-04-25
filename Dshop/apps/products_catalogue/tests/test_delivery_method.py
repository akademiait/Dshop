import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
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
def test_add_to_cart_then_order(api_client_authenticated, ten_tv_products, standard_delivery_method):
    tv_product_1 = ten_tv_products[0] # expected price 599.00 * 2 = 1198
    tv_product_2 = ten_tv_products[1] # expected price 899.00 * 10 = 8990
    data = {
        "cart": {
            'items': [ {'product_pk': tv_product_1.pk, 'quantity': 2}, {'product_pk': tv_product_2.pk, 'quantity': 10},  ]
        },
        "delivery": standard_delivery_method.pk
    }
    order_response = api_client_authenticated.post(reverse("api_order"), data)
    order = Order.objects.get(delivery=standard_delivery_method)
    cart_empty_response = api_client_authenticated.post(reverse("api_cart_empty"))
    assert cart_empty_response.status_code == 200
    assert order_response.status_code == 201
    assert order.delivery_name == "Standard"
    assert order.delivery_price == 10
    assert order.cart_total == 1198 + 8990
    assert order.total_sum == 10 + 1198 + 8990
    assert order.user == get_user_model().objects.get(username="testuser")
    assert order.decoded_cart["items"][0]["product_name"] == 'TV AMOLED 32"'
    assert order.decoded_cart["items"][1]["product_name"] == 'Smart TV 40"'
    assert order.decoded_cart["items"][0]["quantity"] == 2
    assert order.decoded_cart["items"][0]["price"] == "599.00"
    assert order.decoded_cart["items"][0]["subtotal"] == "1198.00"
    assert order.decoded_cart["items"][0]["product_pk"] == 1
    assert order.decoded_cart["items"][0]["quantity"] == 2
    assert order.decoded_cart["items"][1]["product_pk"] == 2
    assert order.decoded_cart["items"][1]["quantity"] == 10
    assert order.decoded_cart["items"][1]["price"] == "899.00"
    assert order.decoded_cart["items"][1]["subtotal"] == "8990.00"
    assert order.decoded_cart["count"] == 12
    assert order.decoded_cart["total"] == '10188.00'


@pytest.mark.django_db
def test_list_order(api_client_authenticated, ten_tv_products, standard_delivery_method):
    for i in range(5):
        data = {
            "cart": {
            'items': [
                {'product_pk': ten_tv_products[i * 2].pk, 'quantity': 5},
                {'product_pk': ten_tv_products[i * 2 + 1].pk, 'quantity': 10}]
            },
            "delivery": standard_delivery_method.pk
        }
        post_response = api_client_authenticated.post(reverse("api_order"), data)
        assert isinstance(post_response.data, dict)
        assert post_response.status_code == 201
    get_response = api_client_authenticated.get(reverse("api_order"))
    assert get_response.status_code == 200
    assert isinstance(get_response.data, dict)
    assert isinstance(get_response.data["results"], list)
    assert len(get_response.data["results"]) == 5
    

@pytest.mark.django_db()
@pytest.mark.parametrize("method", ["post", "get"])
def test_list_anonymous_order(method, ten_tv_products, standard_delivery_method):
    tv_product_1 = ten_tv_products[0]
    tv_product_2 = ten_tv_products[1]
    data = {
        "cart": {
            'items': [ {'product_pk': tv_product_1.pk, 'quantity': 2}, {'product_pk': tv_product_2.pk, 'quantity': 10},  ]
        },
        "delivery": standard_delivery_method.pk
    }
    api_client = APIClient()
    method = getattr(api_client, method)
    order_response = method(reverse("api_order"), data)
    assert order_response.status_code == 401


@pytest.mark.django_db()
@pytest.mark.parametrize("items", ["", None, []])
def test_empty_order(items, standard_delivery_method, api_client_authenticated):

    data = {
        "cart": {
            'items': items
        },
        "delivery": standard_delivery_method.pk
    }
    response = api_client_authenticated.post(reverse("api_order"), data)
    assert response.status_code == 400