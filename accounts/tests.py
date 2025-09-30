from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from wagtail.images.models import Image
from wagtail.images.tests.utils import get_test_image_file  # Wagtail helper for test images
from .models import ExtendedUser


class ExtendedUserModelTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username="john", password="pass123")

    def test_profile_created_automatically(self):
        """Check that ExtendedUser profile is automatically created when a User is created."""
        profile_exists = ExtendedUser.objects.filter(user=self.user).exists()
        self.assertTrue(profile_exists)

    def test_extended_user_str(self):
        """Check that the __str__ method returns the user's full name."""
        profile = ExtendedUser.objects.get(user=self.user)
        # User has no first/last name, get_full_name() returns empty string
        self.assertEqual(profile.__str__(), self.user.get_full_name())

    def test_edit_profile_fields(self):
        """Check that you can edit basic profile fields."""
        profile = ExtendedUser.objects.get(user=self.user)
        profile.cell_no = "1234567890"
        profile.address = "123 Main St"
        profile.sex = "M"
        profile.company_name = "MyCompany"
        profile.save()

        profile.refresh_from_db()
        self.assertEqual(profile.cell_no, "1234567890")
        self.assertEqual(profile.address, "123 Main St")
        self.assertEqual(profile.sex, "M")
        self.assertEqual(profile.company_name, "MyCompany")

    def test_dob_field(self):
        """Check that the dob field can be set and retrieved correctly."""
        profile = ExtendedUser.objects.get(user=self.user)
        today = timezone.now().date()
        profile.dob = today
        profile.save()

        profile.refresh_from_db()
        self.assertEqual(profile.dob, today)

    def test_pic_field(self):
        """Check that a Wagtail image can be attached to the profile."""
        profile = ExtendedUser.objects.get(user=self.user)

        # Create a test image
        image_file = get_test_image_file(filename="test.jpg")
        image = Image.objects.create(title="Test Image", file=image_file)

        profile.pic = image
        profile.save()
        profile.refresh_from_db()

        self.assertEqual(profile.pic, image)
        self.assertEqual(profile.pic.title, "Test Image")
