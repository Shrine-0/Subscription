from rest_framework import serializers
from order.models import Order

class OrderSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Order
        fields = "__all__"