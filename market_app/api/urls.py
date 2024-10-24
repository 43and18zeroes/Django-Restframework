from django.urls import path, include
from .views import ProductViewSet, MarketsView, MarketsSingleView, SellerOfMarketList, SellerViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'sellers', SellerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('market/', MarketsView.as_view()),
    path('market/<int:pk>/', MarketsSingleView.as_view(), name='market-detail'),
    path('market/<int:pk>/sellers/', SellerOfMarketList.as_view()),
]