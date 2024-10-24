from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import MarketSerializer, SellerSerializer, ProductSerializer, SellerListSerializer
from market_app.models import Market, Seller, Product
from rest_framework import mixins
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework import viewsets

class ListRetrieveViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    pass

class ProductViewSet(ListRetrieveViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductViewSetOld(viewsets.ViewSet):
    queryset = Product.objects.all()
    
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    def destroy(self, request, pk=None):
        product = get_object_or_404(self.queryset, pk=pk)
        serializer = ProductSerializer(product)
        product.delete()
        return Response(serializer.data)

class MarketsView(generics.ListAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer


class MarketsSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Market.objects.all()
    serializer_class = MarketSerializer
    
    
class SellerOfMarketList(generics.ListCreateAPIView):
    serializer_class = SellerListSerializer
    
    def get_queryset(self):
        pk = self.kwargs.get('pk')
        market = Market.objects.get(pk = pk)
        return market.sellers.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        market = Market.objects.get(pk = pk)
        serializer.save(markets=[market])


class SellerView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


@api_view(['GET', 'DELETE', 'PUT'])
def sellers_single_view(request, pk):

    try:
        seller = Seller.objects.get(pk=pk)
    except Seller.DoesNotExist:
        return Response({"error": "Seller not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SellerSerializer(seller)
        return Response(serializer.data)

    if request.method == 'PUT':
        data = request.data

        if "markets" in data:
            try:
                markets = Market.objects.filter(id__in=data['markets'])
                seller.markets.set(markets)
            except Market.DoesNotExist:
                return Response({"error": "One or more markets not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SellerSerializer(seller, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        seller.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)