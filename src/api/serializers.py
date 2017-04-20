from rest_framework import serializers
from django.contrib.auth.models import User

from customers.models import CustomerPolygons


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CustomerPolygonsSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField()
    kml_name = serializers.CharField(max_length=250)
    url = serializers.CharField(max_length=250)
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
            'kml_name',
            'url',
		)
