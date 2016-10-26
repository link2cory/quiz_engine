from django.core.urlresolvers import resolve
from django.test import TestCase
from quizzes.views import home_page


class HomePageTest(TestCase):

    def test_root_url_resolbes_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
