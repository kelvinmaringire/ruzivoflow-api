from django.test import TestCase
from wagtail.models import Page
from wagtail.images.models import Image
from wagtail.images.tests.utils import get_test_image_file
from wagtail.blocks.stream_block import StreamValue

from home.models import HomePage


class HomePageTestCase(TestCase):
    def setUp(self):
        # Get Wagtail root page
        self.root_page = Page.objects.get(depth=1)  # Always exists in test DB

        # Create test images
        image_file = get_test_image_file(filename="hero.jpg")
        self.hero_image = Image.objects.create(title="Hero Image", file=image_file)
        self.editor_top_image = Image.objects.create(title="Editor Top", file=image_file)
        self.editor_bottom_image = Image.objects.create(title="Editor Bottom", file=image_file)

        # Create HomePage instance
        self.homepage = HomePage(
            title="Home",
            heroTitle="Welcome Hero",
            heroSubtitle="<p>Hello World</p>",
            heroImage=self.hero_image,
            heroOutlineButtonTitle="Learn More",
            heroOutlineButtonHref="#",
            heroFlatButtonTitle="Get Started",
            heroFlatButtonHref="#",
            services_title="Our Services",
            services_subtitle="Subtitle for services",
            editor_title="Editor Section",
            editor_subtitle="Editor Subtitle",
            editor_description="Editor Description",
            editor_top_image=self.editor_top_image,
            editor_top_image_description="Top image description",
            editor_bottom_image=self.editor_bottom_image,
            editor_bottom_image_description="Bottom image description",
            try_editor_title="Try Editor",
            try_editor_subtitle="Try Subtitle",
            try_editor_subtitle_box="Box Subtitle",
            try_editor_subtitle_signup="Signup Subtitle",
            try_editor_description="Try description",
            try_editor_username="testuser",
            try_editor_password="testpass",
            portfolio_title="Our Portfolio",
            portfolio_subtitle="Portfolio Subtitle",
            contact_title="Contact Us",
            contact_subtitle="Get in touch",
            contact_box_title="Contact Box",
            contact_location="123 Street, City",
            contact_email="info@example.com",
            contact_phone_number="+123456789",
        )

        # Add HomePage to root
        self.root_page.add_child(instance=self.homepage)
        self.homepage.save()

    def test_homepage_creation(self):
        page = HomePage.objects.get(pk=self.homepage.pk)
        self.assertEqual(page.heroTitle, "Welcome Hero")
        self.assertEqual(page.editor_title, "Editor Section")
        self.assertEqual(page.services_title, "Our Services")

    def test_services_streamfield(self):
        self.homepage.services = StreamValue(
            self.homepage.services.stream_block,
            [{
                'type': 'service',
                'value': {'icon': 'fa-star', 'title': 'Service 1', 'subtitle': '<p>Desc</p>'}
            }],
            True
        )
        self.homepage.save()
        self.homepage.refresh_from_db()
        self.assertEqual(len(self.homepage.services), 1)
        self.assertEqual(self.homepage.services[0].value['title'], 'Service 1')

    def test_features_streamfield(self):
        self.homepage.features = StreamValue(
            self.homepage.features.stream_block,
            [{
                'type': 'feature',
                'value': {'icon': 'fa-check', 'title': 'Feature 1', 'subtitle': '<p>Desc</p>'}
            }],
            True
        )
        self.homepage.save()
        self.homepage.refresh_from_db()
        self.assertEqual(len(self.homepage.features), 1)
        self.assertEqual(self.homepage.features[0].value['title'], 'Feature 1')

    def test_portfolio_items_streamfield(self):
        self.homepage.portfolio_items = StreamValue(
            self.homepage.portfolio_items.stream_block,
            [{
                'type': 'portfolio_item',
                'value': {
                    'name': 'App 1',
                    'client': 'Client A',
                    'client_logo': self.hero_image.id,
                    'image': self.hero_image.id,
                    'platform': 'iOS',
                    'description': '<p>Description</p>',
                    'technologies': [{'name': 'Django'}],
                    'website_url': 'https://example.com',
                    'year': 2025
                }
            }],
            True
        )
        self.homepage.save()
        self.homepage.refresh_from_db()
        self.assertEqual(len(self.homepage.portfolio_items), 1)
        self.assertEqual(self.homepage.portfolio_items[0].value['name'], 'App 1')

    def test_social_media_streamfield(self):
        self.homepage.social_media_items = StreamValue(
            self.homepage.social_media_items.stream_block,
            [{
                'type': 'social_media',
                'value': {'name': 'Twitter', 'image': self.hero_image.id, 'link': 'https://twitter.com'}
            }],
            True
        )
        self.homepage.save()
        self.homepage.refresh_from_db()
        self.assertEqual(len(self.homepage.social_media_items), 1)
        self.assertEqual(self.homepage.social_media_items[0].value['name'], 'Twitter')
