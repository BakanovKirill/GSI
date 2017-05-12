from rest_framework import serializers
from django.contrib.auth.models import User

from customers.models import CustomerPolygons, DataPolygons, DataSet


class DataPolygonsSerializer(serializers.ModelSerializer):
    attribute = serializers.CharField(max_length=250)
    value = serializers.CharField(max_length=250)
    units = serializers.CharField(max_length=250)
    total = serializers.CharField(max_length=250)
    total_area = serializers.CharField(max_length=250)

    class Meta:
		model = DataPolygons
		fields = (
            'attribute',
            'value',
            'units',
            'total',
            'total_area'
		)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CustomerPolygonsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    kml_name = serializers.CharField(max_length=250)
    
    class Meta:
		model = CustomerPolygons
		fields = (
            'id',
            'kml_name',
		)
        
        
class DataSetsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=250)
    shapefiles = CustomerPolygonsSerializer(many=True, read_only=True)

    class Meta:
		model = DataSet
		fields = (
            'id',
            'name',
            'shapefiles',
		)
        
        
class DataSetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=250)

    class Meta:
		model = DataSet
		fields = (
            'id',
            'name',
		)
        
        
        
class CustomerPolygonSerializer(CustomerPolygonsSerializer):
    id = serializers.IntegerField()
    kml_name = serializers.CharField(max_length=250)
    data_set = DataSetSerializer()
    kml_url = serializers.CharField(max_length=250)
    attributes_shapefile = DataPolygonsSerializer(many=True, read_only=True)
    
    class Meta:
		model = CustomerPolygons
		fields = (
            'id',
            'kml_name',
            'data_set',
            'kml_url',
            'attributes_shapefile',
		)
        
        
