from rest_framework import serializers
from .models import Product, Collection
import decimal


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField(read_only=True)

    def get_products_count(self, collection: Collection):
        return collection.products_count if hasattr(collection, 'products_count') else None

    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    # def validate(self, attrs):
    #     # more validation
    #     # raise serializers.ValidationError({'piong': 'young'})
    #     return super().validate(attrs)

    # def create(self, validated_data): # optional
    #     # manipulate fields
    #     return super().create(validated_data)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    slug = serializers.SlugField()
    price = serializers.DecimalField(
        max_digits=6,
        decimal_places=2,
        source='unit_price'
    )
    final_price = serializers.SerializerMethodField()
    collection = CollectionSerializer()

    def get_final_price(self, product: Product):
        return round(product.unit_price * decimal.Decimal(1.1), 2)
