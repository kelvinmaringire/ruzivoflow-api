from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class ServicesBlock(blocks.StructBlock):
    icon = blocks.CharBlock()
    title = blocks.CharBlock()
    subtitle = blocks.RichTextBlock()


class FeaturesBlock(blocks.StructBlock):
    icon = blocks.CharBlock()
    title = blocks.CharBlock()
    subtitle = blocks.RichTextBlock()


class TechnologyBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=True)


class PortfolioItemBlock(blocks.StructBlock):
    name = blocks.CharBlock(required=True, max_length=100)
    client = blocks.CharBlock(required=True, max_length=100)
    client_logo = ImageChooserBlock(required=True)
    image = ImageChooserBlock(required=True)
    platform = blocks.CharBlock(required=True, max_length=100)
    description = blocks.RichTextBlock(required=True, features=['bold', 'italic', 'link'])
    technologies = blocks.ListBlock(
        blocks.StructBlock([
            ('name', blocks.CharBlock(required=True))
        ]),
        required=True
    )
    website_url = blocks.URLBlock(required=False)
    play_store_url = blocks.URLBlock(required=False, label="Google Play Store URL")
    app_store_url = blocks.URLBlock(required=False, label="Apple App Store URL")
    year = blocks.IntegerBlock(required=True, min_value=2000, max_value=2100)


class SocialMediaBlock(blocks.StructBlock):
    name = blocks.CharBlock()
    image = ImageChooserBlock()
    link = blocks.URLBlock()