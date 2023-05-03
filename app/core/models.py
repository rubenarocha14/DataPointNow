# DB Models

# Allows us to define new models
from django.db import models  # noqa
from django.conf import settings

# Base user defines all of the fields and methods
# needed for the predef user model
# BaseUserManager handles the persisting
# Acting as an abstract layer
# Permission Mixin allows us to give users certain
# permissions such as admin, user etc
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManger(BaseUserManager):
    # Manager for Users

    def create_user(self, email, password=None, **extra_fields):
        # Create, save and return user
        # self.model defines a new user object
        # self.normalize_email(email) is the function that will normalize all
        # emails
        if not email:
            raise ValueError("User must enter a valid email")
        user = self.model(email=self.normalize_email(email), **extra_fields)

        # set_passowrd when using BaseUserManager hashes the set password
        # this is an autohash and connot be reversed
        user.set_password(password)
        # saves the user and self._db supports multiple db if necessary
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    # User in the system
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Same as entity manager, allows us to access entities (models)
    # from different files in our project
    objects = UserManger()

    USERNAME_FIELD = "email"


class Product(models.Model):
    # Product in the system
    name = models.CharField(max_length=255)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    UPC = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    available_online = models.BooleanField(default=True)
    available_for_pickup = models.BooleanField(default=True)
    available_electronically = models.BooleanField(default=True)
    is_service = models.BooleanField(default=False)
    track_inventory = models.BooleanField(default=True)
    inventory_alert_type = models.CharField(max_length=255, blank=True)
    inventory_alert_threshold = models.PositiveIntegerField(null=True, blank=True)
    # variation = models.ForeignKey(Variation, on_delete=models.CASCADE, null=True, blank=True)
    product_data = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    sub_categories = models.JSONField()
    items = models.JSONField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.name


class Variation(models.Model):
    variation_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product, related_name="variations", on_delete=models.CASCADE
    )
    sku = models.CharField(max_length=255)
    upc = models.CharField(max_length=255)
    cost_money = models.DecimalField(max_digits=10, decimal_places=2)
    price_money = models.DecimalField(max_digits=10, decimal_places=2)
    pricing_type = models.CharField(max_length=255)
    track_inventory = models.BooleanField()
    inventory_alert_type = models.CharField(max_length=255)
    inventory_alert_threshold = models.IntegerField()
    item_option_values = models.JSONField()

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    UPC = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    available_online = models.BooleanField()
    available_for_pickup = models.BooleanField()
    available_electronically = models.BooleanField()
    is_service = models.BooleanField()
    track_inventory = models.BooleanField()
    inventory_alert_type = models.CharField(max_length=255)
    inventory_alert_threshold = models.IntegerField()
    variation = models.ForeignKey(
        Variation,
        null=True,
        blank=True,
        related_name="products",
        on_delete=models.SET_NULL,
    )
    product_data = models.JSONField()

    def __str__(self):
        return self.name


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=255)
    time_zone = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    website = models.URLField()
    business_hours = models.JSONField()

    def __str__(self):
        return self.name


class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    nick_name = models.CharField(max_length=255)
    email_address = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    role_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    given_name = models.CharField(max_length=255)
    family_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255)
    email_address = models.EmailField()
    address = models.TextField()
    phone_number = models.CharField(max_length=255)
    reference_id = models.CharField(max_length=255)
    group_id = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return f"{self.given_name} {self.family_name}"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    buyer_email = models.EmailField()
    recipient_name = models.CharField(max_length=255)
    recipient_phone_number = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    shipping_address = models.JSONField()
    billing_address = models.JSONField()
    note = models.TextField(blank=True)
    line_items = models.JSONField()
    taxes = models.JSONField()
    discounts = models.JSONField()
    service_charges = models.JSONField()
    fulfillments = models.JSONField()
    refunds = models.JSONField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.order_id


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        Order, related_name="transactions", on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        Location, related_name="transactions", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField()
    tender = models.JSONField()
    amount_money = models.DecimalField(max_digits=10, decimal_places=2)
    tip_money = models.DecimalField(max_digits=10, decimal_places=2)
    processing_fee_money = models.DecimalField(max_digits=10, decimal_places=2)
    client_id = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer, related_name="transactions", on_delete=models.CASCADE
    )
    employee = models.ForeignKey(
        Employee, related_name="transactions", on_delete=models.CASCADE
    )
    refunds = models.JSONField()
    reference_id = models.CharField(max_length=255)
    product = models.JSONField()

    def __str__(self):
        return self.transaction_id


class ItemSold(models.Model):
    item_sold_id = models.AutoField(primary_key=True)
    item = models.ForeignKey(
        Product, related_name="items_sold", on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order, related_name="items_sold", on_delete=models.CASCADE
    )
    variation = models.ForeignKey(
        Variation, related_name="items_sold", on_delete=models.CASCADE
    )
    quantity = models.IntegerField()
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.item.name} ({self.variation.name}) - {self.quantity}"


class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    discount_type = models.CharField(max_length=255)
    amount_money = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    scope = models.CharField(max_length=255)
    customer_group_ids = models.JSONField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
