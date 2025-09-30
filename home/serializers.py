from os.path import basename, splitext
from rest_framework.serializers import Field

from wagtail.images.blocks import ImageChooserBlock


class ImageSerializedField(Field):
    def to_representation(self, value):
        request = self.context.get('request')
        filename, extension = splitext(value.file.name)
        filename_without_extension = basename(filename)
        return {
            "image": request.build_absolute_uri(value.file.url),
            "name": filename_without_extension
        }

class PortfolioItemBlockField(Field):
    def to_representation(self, value):
        request = self.context.get('request')
        data = []

        for item in value:
            item_data = {
                'name': item.value['name'],
                'client': item.value['client'],
                'platform': item.value['platform'],
                'description': str(item.value['description']),
                'technologies': [tech['name'] for tech in item.value['technologies']],
                'website_url': item.value.get('website_url'),
                'play_store_url': item.value.get('play_store_url'),
                'app_store_url': item.value.get('app_store_url'),
                'year': item.value['year'],
            }

            # Handle client_logo
            if item.value['client_logo']:
                filename, extension = splitext(item.value['client_logo'].file.name)
                item_data['client_logo'] = {
                    "image": request.build_absolute_uri(item.value['client_logo'].file.url),
                    "name": basename(filename)
                }

            # Handle image
            if item.value['image']:
                filename, extension = splitext(item.value['image'].file.name)
                item_data['image'] = {
                    "image": request.build_absolute_uri(item.value['image'].file.url),
                    "name": basename(filename)
                }

            data.append(item_data)

        return data


class SocialMediaItemBlockField(Field):
    def to_representation(self, value):
        request = self.context.get('request')
        data = []

        for item in value:
            item_data = {
                'name': item.value['name'],
                'link': item.value.get('link'),
            }

            # Handle image
            if item.value['image']:
                filename, extension = splitext(item.value['image'].file.name)
                item_data['image'] = {
                    "image": request.build_absolute_uri(item.value['image'].file.url),
                    "name": basename(filename)
                }

            data.append(item_data)

        return data


   