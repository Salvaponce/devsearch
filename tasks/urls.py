from django.urls import path
from . import views

urlpatterns = [
    path('to_do/', views.to_do, name='to_do'),
]