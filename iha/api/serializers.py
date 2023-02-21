from rest_framework import serializers
from iha.models import IHA, IHACategory

class IHASerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    creator_name = serializers.ReadOnlyField(source='creator.username')
    class Meta:
        model = IHA
        fields = ('id',
                  'slug',
                  'date_of_record',
                  'date_of_update',
                  'mark',
                  'model',
                  'weight',
                  'status',
                  'category_name',
                  'creator_name',
                  'creator',
                  'category')
        read_only_fields = ['id','slug','date_of_record','date_of_update']

class IHACategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = IHACategory
        fields = ['id','name']
        read_only_fields = ['id']