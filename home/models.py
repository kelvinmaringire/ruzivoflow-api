from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.api import APIField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


from .streams import ServicesBlock, FeaturesBlock, PortfolioItemBlock, SocialMediaBlock
from .serializers import ImageSerializedField, PortfolioItemBlockField, SocialMediaItemBlockField


class HomePage(Page):
    heroTitle = models.CharField(max_length=100, blank=False, null=True)
    heroSubtitle = RichTextField(null=True, blank=False)
    heroImage = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    heroOutlineButtonTitle = models.CharField(max_length=100, blank=False, null=True)
    heroOutlineButtonHref = models.CharField(null=True, blank=False)
    heroFlatButtonTitle = models.CharField(max_length=100, blank=False, null=True)
    heroFlatButtonHref = models.CharField(null=True, blank=False)

    services_title = models.CharField(max_length=100, blank=False, null=True)
    services_subtitle = models.CharField(max_length=150, blank=False, null=True)
    services = StreamField([
        ('service', ServicesBlock()),
    ], use_json_field=True, blank=False, null=True, collapsed=True,)

    editor_title = models.CharField(max_length=100, blank=False, null=True)
    editor_subtitle = models.CharField(max_length=150, blank=False, null=True)
    editor_description = models.CharField(max_length=350, blank=False, null=True)
    editor_top_image_description = models.CharField(max_length=100, blank=False, null=True)
    editor_top_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    editor_bottom_image_description = models.CharField(max_length=100, blank=False, null=True)
    editor_bottom_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    features = StreamField([
        ('feature', FeaturesBlock()),
    ], use_json_field=True, blank=False, null=True, collapsed=True,)

    try_editor_title = models.CharField(max_length=100, blank=False, null=True)
    try_editor_subtitle = models.CharField(max_length=150, blank=False, null=True)
    try_editor_subtitle_box = models.CharField(max_length=150, blank=False, null=True)
    try_editor_subtitle_signup = models.CharField(max_length=150, blank=False, null=True)
    try_editor_description = models.CharField(max_length=350, blank=False, null=True)
    try_editor_username = models.CharField(max_length=50, blank=False, null=True)
    try_editor_password = models.CharField(max_length=50, blank=False, null=True)

    portfolio_title = models.CharField(max_length=100, blank=False, null=True)
    portfolio_subtitle = models.CharField(max_length=150, blank=False, null=True)
    portfolio_items = StreamField([
        ('portfolio_item', PortfolioItemBlock())
    ], use_json_field=True, blank=False, null=True, collapsed=True,)

    contact_title = models.CharField(max_length=100, blank=False, null=True)
    contact_subtitle = models.CharField(max_length=150, blank=False, null=True)
    contact_box_title = models.CharField(max_length=100, blank=False, null=True)
    contact_location = models.CharField(max_length=100, blank=False, null=True)
    contact_email = models.CharField(max_length=50, blank=False, null=True)
    contact_phone_number = models.CharField(max_length=50, blank=False, null=True)
    social_media_items = StreamField([
        ('social_media', SocialMediaBlock()),
    ], use_json_field=True, blank=False, null=True, collapsed=True,)



    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel("heroTitle"),
            FieldPanel("heroSubtitle"),
            FieldPanel("heroImage"),
            FieldPanel("heroOutlineButtonTitle"),
            FieldPanel("heroOutlineButtonHref"),
            FieldPanel("heroFlatButtonTitle"),
            FieldPanel("heroFlatButtonHref"),
        ], heading="Hero Options", classname="collapsed", icon="desktop"),
        MultiFieldPanel([
            FieldPanel("services_title"),
            FieldPanel("services_subtitle"),
            FieldPanel("services"),
        ], heading="Services", classname="collapsed", icon="cogs"),
        MultiFieldPanel([
            FieldPanel("editor_title"),
            FieldPanel("editor_subtitle"),
            FieldPanel("editor_description"),
            FieldPanel("editor_top_image"),
            FieldPanel("editor_top_image_description"),
            FieldPanel("editor_bottom_image"),
            FieldPanel("editor_bottom_image_description"),
            FieldPanel("features"),
        ], heading="Ruzivo Editor", classname="collapsed", icon="image"),
        MultiFieldPanel([
            FieldPanel("try_editor_title"),
            FieldPanel("try_editor_subtitle"),
            FieldPanel("try_editor_subtitle_box"),
            FieldPanel("try_editor_subtitle_signup"),
            FieldPanel("try_editor_description"),
            FieldPanel("try_editor_username"),
            FieldPanel("try_editor_password"),
        ], heading="Try Ruzivo Editor", classname="collapsed", icon="crosshairs"),
        MultiFieldPanel([
            FieldPanel("portfolio_title"),
            FieldPanel("portfolio_subtitle"),
            FieldPanel("portfolio_items"),
        ], heading="Portfolio", classname="collapsed", icon="doc-full-inverse"),
        MultiFieldPanel([
            FieldPanel("contact_title"),
            FieldPanel("contact_subtitle"),
            FieldPanel("contact_box_title"),
            FieldPanel("contact_location"),
            FieldPanel("contact_email"),
            FieldPanel("contact_phone_number"),
            FieldPanel("social_media_items"),
        ], heading="Contact", classname="collapsed", icon="mail"),
    ]

    api_fields = [
        APIField('heroTitle'),
        APIField('heroSubtitle'),
        APIField('heroImage', serializer=ImageSerializedField()),
        APIField('heroOutlineButtonTitle'),
        APIField('heroOutlineButtonHref'),
        APIField('heroFlatButtonTitle'),
        APIField('heroFlatButtonHref'),
        APIField('services_title'),
        APIField('services_subtitle'),
        APIField('services'),
        APIField("editor_title"),
        APIField("editor_subtitle"),
        APIField("editor_description"),
        APIField("editor_top_image", serializer=ImageSerializedField()),
        APIField("editor_top_image_description"),
        APIField("editor_bottom_image", serializer=ImageSerializedField()),
        APIField("editor_bottom_image_description"),
        APIField("features"),
        APIField("try_editor_title"),
        APIField("try_editor_subtitle"),
        APIField("try_editor_subtitle_box"),
        APIField("try_editor_subtitle_signup"),
        APIField("try_editor_description"),
        APIField("try_editor_username"),
        APIField("try_editor_password"),
        APIField("portfolio_title"),
        APIField("portfolio_subtitle"),
        APIField("portfolio_items", serializer=PortfolioItemBlockField()),
        APIField("contact_title"),
        APIField("contact_subtitle"),
        APIField("contact_box_title"),
        APIField("contact_location"),
        APIField("contact_email"),
        APIField("contact_phone_number"),
        APIField("social_media_items", serializer=SocialMediaItemBlockField()),

    ]


