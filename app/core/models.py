# DB Models

# Allows us to define new models
from django.db import models

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
