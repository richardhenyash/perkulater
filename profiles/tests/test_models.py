"""
Profiles application model tests
"""
from django.shortcuts import get_object_or_404
from django.test import TestCase

from django.contrib.auth.models import User

from profiles.models import UserProfile, Reward

from products.tests.test_data import build_test_data


class TestUserProfileModel(TestCase):
    """A class to test the UserProfile model"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_profile_str(self):
        """Test UserProfile string method"""
        user = get_object_or_404(User, username="unittestuser")
        user_profile = get_object_or_404(UserProfile, user=user)
        self.assertEqual(str(user_profile), "unittestuser")

    def test_profile_full_name(self):
        """Test UserProfile full_name method"""
        user = get_object_or_404(User, username="unittestuser")
        user_profile = get_object_or_404(UserProfile, user=user)
        self.assertEqual(user_profile.full_name(), "Test User")

    def test_profile_user_name(self):
        """Test UserProfile user_name method"""
        user = get_object_or_404(User, username="unittestuser")
        user_profile = get_object_or_404(UserProfile, user=user)
        self.assertEqual(user_profile.user_name(), "unittestuser")

    def test_create_user_profile_receiver(self):
        """Test UserProfile create receiver"""
        # Create new standard user
        newuser = User.objects.create_user(
            'unittestuser2', 'unittestuser2@test.com', 'unittestuser2password')
        user_profile = get_object_or_404(UserProfile, user=newuser)
        # Test new user user_name
        self.assertTrue(user_profile)
        self.assertEqual(user_profile.user_name(), "unittestuser2")

    def test_update_user_profile_receiver(self):
        """Test UserProfile update receiver"""
        # Get standard user
        user = get_object_or_404(User, username="unittestuser")
        # Update username
        user.username = "unittestuserupdated"
        user.save()
        user_profile = get_object_or_404(UserProfile, user=user)
        # Test updated user user_name
        self.assertTrue(user_profile)
        self.assertEqual(user_profile.user_name(), "unittestuserupdated")


class TestRewardModel(TestCase):
    """A class to test the Reward model"""
    @classmethod
    def setUpTestData(cls):
        build_test_data()

    def test_reward_str(self):
        """Test Reward string method"""
        user = get_object_or_404(User, username="unittestuser")
        reward = get_object_or_404(Reward, user=user)
        self.assertEqual(str(reward), "unittestuser")
