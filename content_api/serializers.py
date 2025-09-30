import os
from wagtail.documents.models import Document
from wagtail.images.models import Image
from wagtail.models import Collection
from rest_framework import serializers

class DocumentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = '__all__'
        read_only_fields = ('title', 'uploaded_by_user', 'file_size', 'file_hash')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('tags', None)

    def get_file_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url)

    def create(self, validated_data):
        # Get file from validated data
        file = validated_data['file']
        
        # Set title from filename
        validated_data['title'] = os.path.splitext(file.name)[0]
        
        # Set authenticated user
        validated_data['uploaded_by_user'] = self.context['request'].user
        
        # Create document instance
        document = Document(**validated_data)
        
        # Save to trigger file storage
        document.save()
        
        # Calculate and set file metadata
        document._set_document_file_metadata()
        
        # Save metadata fields
        document.save(update_fields=['file_size', 'file_hash'])
        
        return document

    


class ImageSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = '__all__'

    def get_file_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.file.url)    
    

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'  