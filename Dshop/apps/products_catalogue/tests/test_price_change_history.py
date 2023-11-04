"""
+ there is PriceChangeHistory model with relation to product, with fields: price, created_at, disabled_at.
- creating product creates first PriceChangeHistory object with disabled_at == null
- every price change on product creates new PriceChangeHistory object with current date and time, previous PriceChangeHistory has disabled_at set to current date and time. 
- current price of the product is equal to the most recent entry in PriceChangeHistory for this model

"""

import pytest
from apps.products_catalogue.models import PriceChangeHistory, Product, Category


# use https://pypi.org/project/freezegun/ for time management in tests
# add __init__ method to product and store current price in local variable
# in save check if price changed
# if price changed 
#   - update last existing PriceCHangeHistory object with disabled_at = current time
#   - create new PriceCHangeHistory with new price


@pytest.mark.django_db # to be deleted
def test_model_structure():
    # This kind of test is for fun mostly and will be deleted in going further. 
    # However, those simple tests have great unlocking power and allow to learn new stuff. 
    # There is nothing wrong in deleting obsolete test at some point:
    # Flow:
    # red
    # green
    # refactor

    # Given
    fields_to_check = ["product", "price", "created_at", "disabled_at"]
    # When
    model = PriceChangeHistory
    # Then
    for field in fields_to_check:
        assert model._meta.get_field(field)


@pytest.fixture
def create_product_with_cat():
    category = Category.objects.create(name='Test Category', is_active=True)
    return Product.objects.create(
        name="first one",
        category=category,
        price=11,
        short_description="short desc",
        full_description="full_description"
    )


@pytest.mark.django_db
def test_product_creation_creates_price_change_history(create_product_with_cat):   
    product = create_product_with_cat
    assert PriceChangeHistory.objects.count() == 1


@pytest.mark.django_db
def test_single_lowest_price_in_30_days(create_product_with_cat):
    product = create_product_with_cat
    assert product.lowest_price_in_30_days == product.price


@pytest.mark.django_db
def test_many_pricechangehistory_count(create_product_with_cat):
    product = create_product_with_cat
    #upper already saved once
    product.price = 2
    product.save()
    product.price = 3
    product.save()
    product.price = 4
    product.save()
    assert PriceChangeHistory.objects.count() == 4


@pytest.mark.django_db
def test_many_lowest_price_in_30_days_all_now(create_product_with_cat):
    product = create_product_with_cat
    product.price = 10
    product.save()
    product.price = 100
    product.save()
    product.price = 0.1
    product.save()
    assert product.lowest_price_in_30_days == 0.1

