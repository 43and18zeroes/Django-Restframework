from django.urls import path
from .views import first_view, market_single_view

urlpatterns = [
    path('', first_view),
    path('<int:pk>/', market_single_view),
]