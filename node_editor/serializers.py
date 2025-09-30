import json

from rest_framework import serializers
from .models import NodeCategory, Node, Workflow, NodeItem, Connection


class NodeCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = NodeCategory
        fields = '__all__'


class NodeSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField('get_icon_url')

    class Meta:
        model = Node
        fields = '__all__'

    def get_icon_url(self, obj):
        if obj.icon:
            request = self.context.get('request')
            icon_url = obj.icon.file.url
            return request.build_absolute_uri(icon_url)
        return None


class WorkflowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Workflow
        fields = '__all__'


class NodeItemSerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField('get_icon_url')

    class Meta:
        model = NodeItem
        fields = '__all__'
        # extra_kwargs = {'node_value': {'write_only': True}}

    def get_icon_url(self, obj):
        if obj.icon:
            request = self.context.get('request')
            icon_url = obj.icon.file.url
            return request.build_absolute_uri(icon_url)
        return None


class ConnectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Connection
        fields = '__all__'
