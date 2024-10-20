from rest_framework import serializers
from market_app.models import Market, Seller, Product

class MarketSerializer(serializers.ModelSerializer):
    
    sellers = serializers.StringRelatedField(many=True, read_only=True)
    
    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
    
    class Meta:
        model = Market
        fields = ['id', 'url', 'name', 'location', 'description', 'net_worth']
        
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
    sellers = None    
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
        
    # name = serializers.CharField(max_length=255)
    # description = serializers.CharField()
    # price = serializers.DecimalField(max_digits=50, decimal_places=2)
    
    # market_display = serializers.CharField(source='market.name', read_only=True) 
    # seller_display = serializers.CharField(source='seller.name', read_only=True) 

    # market = serializers.IntegerField(write_only=True)
    # seller = serializers.IntegerField(write_only=True)
    
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.price = validated_data.get('price', instance.price)
        
    #     if 'market' in validated_data:
    #         try:
    #             market = Market.objects.get(id=validated_data['market'])
    #             instance.market = market
    #         except Market.DoesNotExist:
    #             raise serializers.ValidationError("Market ID does not exist")
        
    #     if 'seller' in validated_data:
    #         try:
    #             seller = Seller.objects.get(id=validated_data['seller'])
    #             instance.seller = seller
    #         except Seller.DoesNotExist:
    #             raise serializers.ValidationError("Seller ID does not exist")
        
    #     instance.save()
    #     return instance
    
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
    # name = serializers.CharField(max_length=255)
    # description = serializers.CharField()
    # price = serializers.DecimalField(max_digits=50, decimal_places=2)
    # market = serializers.IntegerField(write_only=True)
    # seller = serializers.IntegerField(write_only=True)
    
    # def validate_market(self, value):
    #     try:
    #         Market.objects.get(id=value)
    #     except Market.DoesNotExist:
    #         raise serializers.ValidationError("Market ID does not exist")
    #     return value

    # def validate_seller(self, value):
    #     try:
    #         Seller.objects.get(id=value)
    #     except Seller.DoesNotExist:
    #         raise serializers.ValidationError("Seller ID does not exist")
    #     return value

    # def create(self, validated_data):
    #     market_id = validated_data.pop('market')
    #     seller_id = validated_data.pop('seller')
    #     market = Market.objects.get(id=market_id)
    #     seller = Seller.objects.get(id=seller_id)
    #     product = Product.objects.create(market=market, seller=seller, **validated_data)
    #     return product
    
    
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