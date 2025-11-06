from rest_framework import serializers
from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'node', 'name', 'model', 'release_date']


class NetworkNodeSerializer(serializers.ModelSerializer):
    # вложённые продукты — при желании можно включать/исключать
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name',
            'email', 'country', 'city', 'street', 'house_number',
            'supplier', 'debt', 'created_at', 'level', 'products'
        ]
        read_only_fields = ('created_at', 'level')  # readonly auto-поля

    def validate(self, data):
        # Простейшая валидация: если указан supplier, он не должен быть самим собой (в create pk нет)
        supplier = data.get('supplier') or getattr(self.instance, 'supplier', None)
        if self.instance and supplier and supplier.pk == self.instance.pk:
            raise serializers.ValidationError("Поставщик не может быть самим собой.")
        return data
