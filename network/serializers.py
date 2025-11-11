from rest_framework import serializers
from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'node', 'name', 'model', 'release_date']


class NetworkNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = [
            'id', 'name',
            'email', 'country', 'city', 'street', 'house_number',
            'supplier', 'debt', 'created_at', 'level'
        ]
        read_only_fields = ('created_at', 'level')

    def validate(self, data):
        supplier = data.get("supplier") or getattr(self.instance, "supplier", None)

        if supplier:
            level = (supplier.level or 0) + 1
        else:
            level = 0

        if level > 2:
            raise serializers.ValidationError(
                {"supplier": "Узел не может быть выше уровня 2"}
            )

        return data
