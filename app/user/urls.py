# URL Mappings for User API

from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.createUserView.as_view(), name='create'),
]