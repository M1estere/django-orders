# orders/serializers.py

from rest_framework import serializers
from .models import Order, Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            item, created = Item.objects.get_or_create(**item_data)
            order.items.add(item)

        order.update_total_price()
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        instance.table_number = validated_data.get('table_number', instance.table_number)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        instance.items.clear()
        for item_data in items_data:
            item, created = Item.objects.get_or_create(**item_data)
            instance.items.add(item)
            
        instance.update_total_price()
        return instance
