from django.test import TestCase
from django.urls import reverse
from .models import Paths

class URLShortenerTests(TestCase):
    def setUp(self):
        """Set up test data."""
        self.valid_url = "https://www.example.com/page"
        self.invalid_url = "not_a_valid_url"
        self.short_path = "abc1234"
        self.path_entry = Paths.objects.create(src_path=self.short_path, dest_url=self.valid_url)

    def test_create_short_url(self):
        """Test that a URL can be created and stored in the database."""
        self.assertEqual(Paths.objects.count(), 1)
        self.assertEqual(Paths.objects.first().dest_url, self.valid_url)

    def test_redirect_to_dest(self):
        """Test that accessing the shortened URL redirects correctly."""
        response = self.client.get(reverse("short_url_redirect", args=[self.short_path]))
        self.assertRedirects(response, self.valid_url, status_code=302, fetch_redirect_response=False)


    def test_redirect_invalid_path(self):
        """Test that an invalid shortened URL returns a 404 error."""
        response = self.client.get(reverse("short_url_redirect", args=["invalid123"]))
        self.assertEqual(response.status_code, 404)

    def test_form_submission_valid_url(self):
        """Test submitting a valid URL through the form."""
        response = self.client.post(reverse("main_home"), {"dest_url": "https://www.django.com"}, follow=True)
        self.assertEqual(Paths.objects.count(), 2)  # A new URL should be added
        self.assertContains(response, "Your shortened URL is")  # Message should be displayed

    def test_form_submission_invalid_url(self):
        """Test submitting an invalid URL through the form."""
        response = self.client.post(reverse("main_home"), {"dest_url": "invalid-url"}, follow=True)
        self.assertEqual(Paths.objects.count(), 1)  # No new URL should be added
        self.assertContains(response, "Enter a valid URL.")  # Error message should be displayed
