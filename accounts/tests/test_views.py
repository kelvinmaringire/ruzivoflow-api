"""
API View Tests for Accounts App

Crucial tests for User and ExtendedUser API endpoints:
- User creation via POST /accounts/
- ExtendedUser auto-creation via signal
- User update via PUT/PATCH /accounts/<pk>/
"""
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from accounts.models import ExtendedUser


class UserListCreateTestCase(APITestCase):
    """Test User creation via POST /accounts/ endpoint"""

    def setUp(self):
        """Set up test client and test data"""
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_create_user_success(self):
        """Test successful user creation via API"""
        response = self.client.post('/accounts/', self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        
        user = User.objects.get(username='testuser')
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_create_user_auto_creates_extended_profile(self):
        """Test that ExtendedUser profile is auto-created when User is created"""
        response = self.client.post('/accounts/', self.user_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        user = User.objects.get(username='testuser')
        # Verify ExtendedUser was auto-created via signal
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, ExtendedUser)
        self.assertEqual(ExtendedUser.objects.count(), 1)


class UserUpdateTestCase(APITestCase):
    """Test User update via PUT/PATCH /accounts/<pk>/ endpoint"""

    def setUp(self):
        """Set up test client and test user"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123',
            first_name='Original',
            last_name='Name'
        )

    def test_update_user_patch(self):
        """Test user update using PATCH method (partial update)"""
        update_data = {'email': 'updated@example.com'}
        
        response = self.client.patch(f'/accounts/{self.user.id}/', update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'updated@example.com')
        # Other fields should remain unchanged
        self.assertEqual(self.user.first_name, 'Original')

    def test_get_user_detail(self):
        """Test retrieving user details via GET"""
        response = self.client.get(f'/accounts/{self.user.id}/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'testuser@example.com')


class ExtendedUserUpdateTestCase(APITestCase):
    """Test ExtendedUser update via PUT/PATCH /accounts/extended/<pk>/ endpoint"""

    def setUp(self):
        """Set up test client and test data"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass123'
        )
        # ExtendedUser is auto-created via signal
        self.extended_user = ExtendedUser.objects.get(user=self.user)
        self.extended_user.cell_no = '+1234567890'
        self.extended_user.save()

    def test_update_extended_user_patch(self):
        """Test ExtendedUser partial update using PATCH"""
        update_data = {'cell_no': '+9876543210', 'address': 'Updated Address'}
        
        response = self.client.patch(
            f'/accounts/extended/{self.extended_user.id}/',
            update_data,
            format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.extended_user.refresh_from_db()
        self.assertEqual(self.extended_user.cell_no, '+9876543210')
        self.assertEqual(self.extended_user.address, 'Updated Address')
