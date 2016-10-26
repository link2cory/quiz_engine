from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest

from quizzes.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolbes_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Quiz Time!</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
