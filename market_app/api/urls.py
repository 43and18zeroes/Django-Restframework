from django.urls import path, include
from .views import ProductViewSet, MarketsView, MarketsSingleView, SellerOfMarketList, SellerView, sellers_single_view
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('market/', MarketsView.as_view()),
    path('market/<int:pk>/', MarketsSingleView.as_view(), name='market-detail'),
    path('market/<int:pk>/sellers/', SellerOfMarketList.as_view()),
    path('seller/', SellerView.as_view()),
    path('seller/<int:pk>/', sellers_single_view, name='seller_single'),
]