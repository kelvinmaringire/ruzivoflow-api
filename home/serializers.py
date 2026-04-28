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
            # StreamField block schema changed in migration 0005:
            # - removed `client`
            # - renamed `client_logo` -> `logo`
            # Use safe access + fallbacks to support existing content.
            item_data = {
                'name': item.value.get('name'),
                'client': item.value.get('client') or item.value.get('name'),
                'platform': item.value.get('platform'),
                'description': str(item.value.get('description') or ''),
                'features': [
                    tech.get('name')
                    for tech in (item.value.get('features') or item.value.get('technologies') or [])
                    if tech.get('name')
                ],
                'website_url': item.value.get('website_url'),
                'play_store_url': item.value.get('play_store_url'),
                'download_path': item.value.get('download_path'),
                'year': item.value.get('year'),
            }

            logo = item.value.get('logo') or item.value.get('client_logo')
            if logo:
                filename, extension = splitext(logo.file.name)
                item_data['client_logo'] = {
                    "image": request.build_absolute_uri(logo.file.url) if request else logo.file.url,
                    "name": basename(filename)
                }

            # Handle image
            image = item.value.get('image')
            if image:
                filename, extension = splitext(image.file.name)
                item_data['image'] = {
                    "image": request.build_absolute_uri(image.file.url) if request else image.file.url,
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


   