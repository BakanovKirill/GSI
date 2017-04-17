from rest_framework import serializers

from customers.models import DataTerraserver


class DataTerraserverSerializer(serializers.Serializer):
    shapefile = serializers.CharField(max_length=250)
    parameter = serializers.CharField(max_length=250)
    transaction_id = serializers.CharField(max_length=250)
    
    class Meta:
		model = DataTerraserver
		fields = (
			'shapefile',
			'parameter',
			'transaction_id'
		)
