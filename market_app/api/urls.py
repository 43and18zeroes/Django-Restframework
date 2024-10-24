from django.urls import path, include
from .views import ProductViewSet, MarketsView, MarketsSingleView, SellerOfMarketList, SellerListView, SellerDetailView, sellers_single_view
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('market/', MarketsView.as_view()),
    path('market/<int:pk>/', MarketsSingleView.as_view(), name='market-detail'),
    path('market/<int:pk>/sellers/', SellerOfMarketList.as_view()),
    path('seller/', SellerListView.as_view()),
    path('seller/<int:pk>/', SellerDetailView.as_view()),
]