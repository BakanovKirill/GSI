from rest_framework import serializers
from django.contrib.auth.models import User

from customers.models import DataTerraserver, DataSet, CustomerAccess


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class DataSetSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=250)
    description = serializers.CharField(max_length=250)
    results_directory = serializers.CharField(max_length=250)
    
    class Meta:
		model = DataSet
		fields = (
			'name',
			'description',
			'results_directory'
		)
