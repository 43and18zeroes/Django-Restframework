from rest_framework import serializers
from market_app.models import Market, Seller, Product

def validate_no_x(value):
    errors = []
    
    if 'X' in value:
        errors.append('no X in location')
    if 'Y' in value:
        errors.append('no Y in location')
        
    if errors:
        raise serializers.ValidationError(errors)
    
    return value

class MarketSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    location = serializers.CharField(max_length=255, validators=[validate_no_x])
    description = serializers.CharField()
    net_worth = serializers.DecimalField(max_digits=100, decimal_places=2)
    
    def create(self, validated_data):
        return Market.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get('description', instance.description)
        instance.net_worth = validated_data.get('net_worth', instance.net_worth)
        instance.save()
        return instance
    
class SellerDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    # markets = MarketSerializer(many=True, read_only=True)
    markets = serializers.StringRelatedField(many=True)
    
class SellerCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    contact_info = serializers.CharField()
    markets = serializers.ListField(child=serializers.IntegerField(), write_only=True)
    
    def validate_markets(self, value):
        markets = Market.objects.filter(id__in=value)
        if len(markets) != len(value):
            raise serializers.ValidationError("Passt nicht mit den IDs")
        return value
    
    def create(self, validated_data):
        market_ids = validated_data.pop('markets')
        seller = Seller.objects.create(**validated_data)
        markets = Market.objects.filter(id__in=market_ids)
        seller.markets.set(markets)
        return seller
    
class ProductDetailSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = serializers.IntegerField(write_only=True)  # Change to writable field
    seller = serializers.IntegerField(write_only=True)  # Change to writable field
    market_display = serializers.StringRelatedField(source='market', read_only=True)  # Keep the read-only display
    seller_display = serializers.StringRelatedField(source='seller', read_only=True)  # Keep the read-only display
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        
        # Fetch and assign new market and seller
        if 'market' in validated_data:
            try:
                market = Market.objects.get(id=validated_data['market'])
                instance.market = market
            except Market.DoesNotExist:
                raise serializers.ValidationError("Market ID does not exist")
        
        if 'seller' in validated_data:
            try:
                seller = Seller.objects.get(id=validated_data['seller'])
                instance.seller = seller
            except Seller.DoesNotExist:
                raise serializers.ValidationError("Seller ID does not exist")
        
        instance.save()
        return instance
    
class ProductCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=50, decimal_places=2)
    market = serializers.IntegerField(write_only=True)
    seller = serializers.IntegerField(write_only=True)
    
    def validate_market(self, value):
        try:
            Market.objects.get(id=value)
        except Market.DoesNotExist:
            raise serializers.ValidationError("Market ID does not exist")
        return value

    def validate_seller(self, value):
        try:
            Seller.objects.get(id=value)
        except Seller.DoesNotExist:
            raise serializers.ValidationError("Seller ID does not exist")
        return value

    def create(self, validated_data):
        market_id = validated_data.pop('market')
        seller_id = validated_data.pop('seller')
        market = Market.objects.get(id=market_id)
        seller = Seller.objects.get(id=seller_id)
        product = Product.objects.create(market=market, seller=seller, **validated_data)
        return product
    
    
"""
Seller:
{
    "name": "Seller1",
    "contact_info": "seller1@gmail.com",
    "markets": "[2]"
}


Product:
{
    "name": "Product1",
    "description": "This is a nice product",
    "price": 10.00,
    "market": 2,
    "seller": 1
}

{
    "name": "Product4",
    "description": "This is an updated nice product",
    "price": 10.00,
    "market": 4,
    "seller": 2
}
"""