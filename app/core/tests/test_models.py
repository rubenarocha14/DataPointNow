# Test for Models

from decimal import Decimal

from django.test import TestCase

# Imports models
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    # Test models

    def test_create_user_with_email_successful(self):
        # Testing create a user w/ email successful

        email = "test@example.com"
        password = "testpass123"
        # objects is a reference to the obj manager we will create
        # create_user is a method we will later define
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        # Checks email is the same
        self.assertEqual(user.email, email)
        # Checks that a password works, cannot use assertEqual because
        # the password will be hased and not equal to the saved password
        self.assertTrue(user.check_password(password))

    def test_for_new_email_normalized(self):
        # est email is normalized
        sameple_emails = [
            ["test1@EXAMPLE.com", "test1@example.com"],
            ["Test2@Example.com", "Test2@example.com"],
            ["TEST3@EXAMPLE.COM", "TEST3@example.com"],
            ["test4@example.COM", "test4@example.com"],
        ]

        for email, expected in sameple_emails:
            user = get_user_model().objects.create_user(email, "sample123")
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        # Test new user w/o email raises error

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_superuser(self):
        # Test creating superuser
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "test123",
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


from django.test import TestCase
from .models import (
    Category,
    Product,
    Variation,
    Location,
    Employee,
    Customer,
    Order,
    Transaction,
    ItemSold,
    Discount,
)


class CategoryModelTest(TestCase):
    def test_create_and_retrieve_category(self):
        category = Category.objects.create(name="Electronics")
        self.assertEqual(category.name, "Electronics")


class ProductModelTest(TestCase):
    def test_create_and_retrieve_product(self):
        name = "Laptop"
        description = "Test product we are creating"
        UPC = 1
        price = Decimal("100.00")
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(
            name=name, description=description, UPC=UPC, price=price, category=category
        )
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.category, category)

        product = models.Product.objects.create(
            name=name, description=description, UPC=UPC, price=price
        )

        self.assertEqual(product.name, name)
        self.assertTrue(product != None)


class VariationModelTest(TestCase):
    def test_create_and_retrieve_variation(self):
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(name="Laptop", category=category)
        variation = Variation.objects.create(name="16GB RAM", product=product)
        self.assertEqual(variation.name, "16GB RAM")
        self.assertEqual(variation.product, product)


class LocationModelTest(TestCase):
    def test_create_and_retrieve_location(self):
        location = Location.objects.create(name="Store A")
        self.assertEqual(location.name, "Store A")


class EmployeeModelTest(TestCase):
    def test_create_and_retrieve_employee(self):
        employee = Employee.objects.create(first_name="John", last_name="Doe")
        self.assertEqual(employee.first_name, "John")
        self.assertEqual(employee.last_name, "Doe")


class CustomerModelTest(TestCase):
    def test_create_and_retrieve_customer(self):
        customer = Customer.objects.create(given_name="Jane", family_name="Smith")
        self.assertEqual(customer.given_name, "Jane")
        self.assertEqual(customer.family_name, "Smith")


class OrderModelTest(TestCase):
    def test_create_and_retrieve_order(self):
        order = Order.objects.create(order_id="12345")
        self.assertEqual(order.order_id, "12345")


class TransactionModelTest(TestCase):
    def test_create_and_retrieve_transaction(self):
        order = Order.objects.create(order_id="12345")
        location = Location.objects.create(name="Store A")
        transaction = Transaction.objects.create(
            transaction_id="T12345", order=order, location=location
        )
        self.assertEqual(transaction.transaction_id, "T12345")
        self.assertEqual(transaction.order, order)
        self.assertEqual(transaction.location, location)


class ItemSoldModelTest(TestCase):
    def test_create_and_retrieve_itemsold(self):
        category = Category.objects.create(name="Electronics")
        product = Product.objects.create(name="Laptop", category=category)
        order = Order.objects.create(order_id="12345")
        variation = Variation.objects.create(name="16GB RAM", product=product)
        item_sold = ItemSold.objects.create(
            item=product, order=order, variation=variation, quantity=1
        )
        self.assertEqual(item_sold.item, product)
        self.assertEqual(item_sold.order, order)
        self.assertEqual(item_sold.variation, variation)
        self.assertEqual(item_sold.quantity, 1)


class DiscountModelTest(TestCase):
    def test_create_and_retrieve_discount(self):
        discount = Discount.objects.create(
            name="10% Off", discount_type="Percentage", percentage=10
        )
        self.assertEqual(discount.name, "10% Off")
        self.assertEqual(discount.discount_type, "Percentage")
        self.assertEqual(discount.percentage, 10)
