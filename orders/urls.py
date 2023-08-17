from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('historybasket/<int:id>/', views.order_history_down, name='order_create_down'),
    path('historybasket/', views.order_history, name='order_create'),
    path('refill/', views.refill, name='refill'),
]
