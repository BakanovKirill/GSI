from rest_framework import serializers
from django.contrib.auth.models import User

from customers.models import CustomerPolygons, DataPolygons


class DataPolygonsSerializer(serializers.ModelSerializer):
    attribute = serializers.CharField(max_length=250)
    value = serializers.CharField(max_length=250)
    
    class Meta:
		model = DataPolygons
		fields = (
            'attribute',
            'value',
		)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CustomerPolygonsSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()
    # item_url = serializers.HyperlinkedIdentityField(view_name='customer_url')
    kml_name = serializers.CharField(max_length=250)
    kml_url = serializers.CharField(max_length=250)
    data_polygons = DataPolygonsSerializer(many=True, read_only=True)
    # data_polygons = serializers.StringRelatedField(many=True)
    
    
    # tracks = serializers.StringRelatedField(many=True)
    
    # shelf_data = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='category'
    #  )
    # shelf_data = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='track-detail'
    # )
    # shelf_data = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # shelf_data = serializers.RelatedField(
    #         queryset=DataSet.objects.all(),
    #         read_only=True,
    #     )
    
    class Meta:
		model = CustomerPolygons
		fields = (
            'id',
            # 'item_url',
            'kml_name',
            'kml_url',
            'data_polygons',
		)
        
        
