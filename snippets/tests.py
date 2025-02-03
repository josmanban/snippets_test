from django.test import TestCase
from snippets.models import Snippet, Language
from django.urls import reverse
from django.contrib.auth.models import User


# Create your tests here.
class SnippetUpdateViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password2025")
        self.user.is_active=True
        self.user.is_superuser=True
        self.aux_language = Language(
            name="python",
            slug="python"
        )

        self.aux_language.save()
        self.aux_snippet = Snippet(
            name="foo",
            description="foo",
            snippet="print('hello world')",
            language=self.aux_language,
            user=self.user
        )
        self.aux_snippet.save()

    def test_edit(self):
        self.client.login(username="testuser", password="password2025")
        response = self.client.post(
            reverse("snippet_edit", kwargs={"pk":self.aux_snippet.id}),
            {
                "id":1,
                "name":"bar",
                "description": "bar",
                "snippet": "print('hello world')",
                "language": self.aux_language.id
            }
        )

        self.aux_snippet.refresh_from_db()
        self.assertEqual(self.aux_snippet.description, "bar")

    def test_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username":"testuser",
                "password":"password2025",                
            }
        )
        self.assertEqual(response.status_code,302)
