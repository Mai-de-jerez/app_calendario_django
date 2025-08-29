from django.test import TestCase
from .models import Profile
from .models import CustomUser

# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create_user('test', 'test@test.com', 'test1234')

    def test_profile_exists(self):
        exists = Profile.objects.filter(user__username='test').exists()
        self.assertEqual(exists, True)

# Create your tests here.
