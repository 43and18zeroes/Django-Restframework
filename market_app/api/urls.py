from django.urls import path
from .views import MarketsView, MarketsSingleView, SellerOfMarketList, SellerView, products_view, products_single_view, sellers_single_view

urlpatterns = [
    path('market/', MarketsView.as_view()),
    path('market/<int:pk>/', MarketsSingleView.as_view(), name='market-detail'),
    path('market/<int:pk>/sellers/', SellerOfMarketList.as_view()),
    path('seller/', SellerView.as_view()),
    path('seller/<int:pk>/', sellers_single_view, name='seller_single'),
    path('product/', products_view),
    path('product/<int:pk>/', products_single_view, name='seller-detail'),
]