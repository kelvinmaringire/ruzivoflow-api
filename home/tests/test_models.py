"""
Model Tests for Home App

Crucial tests for HomePage Wagtail model:
- HomePage creation as Wagtail Page
- HomePage retrieval
- API fields exposure via Wagtail API
- StreamField functionality
"""
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType

from wagtail.models import Page
from wagtail.images.tests.utils import get_test_image_file
from wagtail.images.models import Image

from home.models import HomePage


class HomePageModelTestCase(TestCase):
    """Test HomePage model creation and basic functionality"""

    def setUp(self):
        """Set up root page and test images for Wagtail"""
        # Get or create root page (required by Wagtail)
        root_page_content_type = ContentType.objects.get_for_model(Page)
        self.root_page = Page.objects.filter(depth=1).first()
        
        if not self.root_page:
            # Create root page if it doesn't exist
            self.root_page = Page.objects.create(
                title="Root",
                slug="root",
                content_type=root_page_content_type,
                path="0001",
                depth=1,
                numchild=0,
                url_path="/",
            )
        
        # Create test images for required image fields
        self.hero_image = Image.objects.create(
            title="Test Hero Image",
            file=get_test_image_file()
        )
        self.editor_top_image = Image.objects.create(
            title="Test Editor Top Image",
            file=get_test_image_file()
        )
        self.editor_bottom_image = Image.objects.create(
            title="Test Editor Bottom Image",
            file=get_test_image_file()
        )

    def test_homepage_creation(self):
        """Test HomePage creation as a Wagtail Page"""
        homepage = HomePage(
            title="Test Home",
            slug="test-home",
            heroTitle="Welcome",
            heroSubtitle="<p>Test subtitle</p>",
            heroImage=self.hero_image,
            heroOutlineButtonTitle="Outline Button",
            heroOutlineButtonHref="/outline",
            heroFlatButtonTitle="Flat Button",
            heroFlatButtonHref="/flat",
            services_title="Our Services",
            services_subtitle="What we offer",
            editor_title="Editor",
            editor_subtitle="Try our editor",
            editor_description="Editor description",
            editor_top_image=self.editor_top_image,
            editor_top_image_description="Top image",
            editor_bottom_image=self.editor_bottom_image,
            editor_bottom_image_description="Bottom image",
            try_editor_title="Try Editor",
            try_editor_subtitle="Try it now",
            try_editor_subtitle_box="Sign up",
            try_editor_subtitle_signup="Create account",
            try_editor_description="Try editor description",
            try_editor_username="testuser",
            try_editor_password="testpass",
            portfolio_title="Portfolio",
            portfolio_subtitle="Our work",
            contact_title="Contact",
            contact_subtitle="Get in touch",
            contact_box_title="Contact Box",
            contact_location="Test Location",
            contact_email="test@example.com",
            contact_phone_number="+1234567890",
        )
        
        # Add as child of root page
        self.root_page.add_child(instance=homepage)
        
        # Verify homepage was created
        self.assertIsNotNone(homepage.id)
        self.assertEqual(homepage.title, "Test Home")
        self.assertEqual(homepage.heroTitle, "Welcome")
        self.assertEqual(homepage.depth, 2)  # Root is depth 1, homepage is depth 2
        self.assertTrue(homepage.path.startswith(self.root_page.path))

    def test_homepage_inherits_from_page(self):
        """Test that HomePage inherits from Wagtail Page model"""
        homepage = HomePage(
            title="Test Home",
            slug="test-home",
            heroTitle="Welcome",
            heroSubtitle="<p>Test</p>",
            heroImage=self.hero_image,
            heroOutlineButtonTitle="Outline",
            heroOutlineButtonHref="/outline",
            heroFlatButtonTitle="Flat",
            heroFlatButtonHref="/flat",
            services_title="Services",
            services_subtitle="Subtitle",
            editor_title="Editor",
            editor_subtitle="Subtitle",
            editor_description="Description",
            editor_top_image=self.editor_top_image,
            editor_top_image_description="Top",
            editor_bottom_image=self.editor_bottom_image,
            editor_bottom_image_description="Bottom",
            try_editor_title="Try",
            try_editor_subtitle="Subtitle",
            try_editor_subtitle_box="Box",
            try_editor_subtitle_signup="Signup",
            try_editor_description="Desc",
            try_editor_username="user",
            try_editor_password="pass",
            portfolio_title="Portfolio",
            portfolio_subtitle="Subtitle",
            contact_title="Contact",
            contact_subtitle="Subtitle",
            contact_box_title="Box",
            contact_location="Location",
            contact_email="email@example.com",
            contact_phone_number="123",
        )
        self.root_page.add_child(instance=homepage)
        
        # Verify it's a Page instance
        self.assertIsInstance(homepage, Page)
        # Verify it's also a HomePage instance
        self.assertIsInstance(homepage, HomePage)
        # Verify Page methods are available
        self.assertTrue(hasattr(homepage, 'get_url'))
        self.assertIsNotNone(homepage.url_path)
        # url_path should be set (get_url() requires Site configuration which may not exist in tests)
        self.assertTrue(homepage.url_path.startswith('/'))

    def test_homepage_api_fields_exist(self):
        """Test that api_fields are defined on HomePage model"""
        homepage = HomePage(
            title="Test Home",
            slug="test-home",
            heroTitle="Welcome",
            heroSubtitle="<p>Test</p>",
            heroImage=self.hero_image,
            heroOutlineButtonTitle="Outline",
            heroOutlineButtonHref="/outline",
            heroFlatButtonTitle="Flat",
            heroFlatButtonHref="/flat",
            services_title="Services",
            services_subtitle="Subtitle",
            editor_title="Editor",
            editor_subtitle="Subtitle",
            editor_description="Description",
            editor_top_image=self.editor_top_image,
            editor_top_image_description="Top",
            editor_bottom_image=self.editor_bottom_image,
            editor_bottom_image_description="Bottom",
            try_editor_title="Try",
            try_editor_subtitle="Subtitle",
            try_editor_subtitle_box="Box",
            try_editor_subtitle_signup="Signup",
            try_editor_description="Desc",
            try_editor_username="user",
            try_editor_password="pass",
            portfolio_title="Portfolio",
            portfolio_subtitle="Subtitle",
            contact_title="Contact",
            contact_subtitle="Subtitle",
            contact_box_title="Box",
            contact_location="Location",
            contact_email="email@example.com",
            contact_phone_number="123",
        )
        self.root_page.add_child(instance=homepage)
        
        # Verify api_fields attribute exists
        self.assertTrue(hasattr(homepage, 'api_fields'))
        self.assertIsNotNone(homepage.api_fields)
        self.assertGreater(len(homepage.api_fields), 0)

    def test_homepage_streamfields_exist(self):
        """Test that StreamFields exist and can be accessed"""
        homepage = HomePage(
            title="Test Home",
            slug="test-home",
            heroTitle="Welcome",
            heroSubtitle="<p>Test</p>",
            heroImage=self.hero_image,
            heroOutlineButtonTitle="Outline",
            heroOutlineButtonHref="/outline",
            heroFlatButtonTitle="Flat",
            heroFlatButtonHref="/flat",
            services_title="Services",
            services_subtitle="Subtitle",
            editor_title="Editor",
            editor_subtitle="Subtitle",
            editor_description="Description",
            editor_top_image=self.editor_top_image,
            editor_top_image_description="Top",
            editor_bottom_image=self.editor_bottom_image,
            editor_bottom_image_description="Bottom",
            try_editor_title="Try",
            try_editor_subtitle="Subtitle",
            try_editor_subtitle_box="Box",
            try_editor_subtitle_signup="Signup",
            try_editor_description="Desc",
            try_editor_username="user",
            try_editor_password="pass",
            portfolio_title="Portfolio",
            portfolio_subtitle="Subtitle",
            contact_title="Contact",
            contact_subtitle="Subtitle",
            contact_box_title="Box",
            contact_location="Location",
            contact_email="email@example.com",
            contact_phone_number="123",
        )
        self.root_page.add_child(instance=homepage)
        
        # Verify StreamFields exist and can be accessed
        self.assertTrue(hasattr(homepage, 'services'))
        self.assertTrue(hasattr(homepage, 'portfolio_items'))
        self.assertTrue(hasattr(homepage, 'features'))
        self.assertTrue(hasattr(homepage, 'social_media_items'))
        # StreamFields can be empty initially
        self.assertIsNotNone(homepage.services)
        self.assertIsNotNone(homepage.portfolio_items)
        self.assertIsNotNone(homepage.features)
        self.assertIsNotNone(homepage.social_media_items)
