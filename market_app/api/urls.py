from django.urls import path
from .views import markets_view, markets_single_view, sellers_view, products_view, products_single_view, sellers_single_view

urlpatterns = [
    path('market/', markets_view),
    path('market/<int:pk>/', markets_single_view, name='market-detail'),
    path('seller/', sellers_view),
    path('seller/<int:pk>/', sellers_single_view, name='seller_single'),
    path('product/', products_view),
    path('product/<int:pk>/', products_single_view),
]