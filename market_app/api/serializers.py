from rest_framework import serializers
from market_app.models import Market, Seller, Product

class MarketSerializer(serializers.ModelSerializer):
     
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
    class Meta:
        model = Market
        fields = ['id', 'sellers', 'url', 'name', 'location', 'description', 'net_worth']
        
    def validate_name(self, value):
        errors = []
    
        if 'X' in value:
            errors.append('no X in location')
        if 'Y' in value:
            errors.append('no Y in location')
            
        if errors:
            raise serializers.ValidationError(errors)
        
        return value
    
class MarketHyperlinkedSerializer(MarketSerializer, serializers.HyperlinkedModelSerializer):
    # sellers = None
    class Meta:
        model = Market
        exclude = ['location']
        
class SellerSerializer(serializers.ModelSerializer):
    markets = MarketSerializer(many=True, read_only=True)
    market_ids = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects.all(),
        many=True,
        write_only=True,
        source='markets'
    )
    
    market_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Seller
        exclude = []
        
    def get_market_count(self, obj):
        return obj.markets.count()

    
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
    
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
   
   
class SellerListSerializer(SellerSerializer, serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seller
        fields  = ["url", "name", "market_ids", "market_count", "contact_info"]       
    
"""
Seller:
{
    "name": "Sellernew",
    "contact_info": "sellernew@gmail.com",
    "market_ids": [2, 3]
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