from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest

from quizzes.views import home_page

import re


class MyTestCase(TestCase):

    @staticmethod
    def remove_csrf(html_code):
        csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
        return re.sub(csrf_regex, '', html_code)

    def assertEqualExceptCSRF(self, html_code1, html_code2):
        return self.assertEqual(
            self.remove_csrf(html_code1),
            self.remove_csrf(html_code2)
        )


class HomePageTest(MyTestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', request=request)
        self.assertEqualExceptCSRF(expected_html, response.content.decode())

    def test_home_page_handles_POST_request_correct_answer(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['answer'] = 'John'

        response = home_page(request)

        self.assertIn('Correct!', response.content.decode())

    def test_home_page_handles_POST_request_incorrect_answer(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['answer'] = 'Jacob'

        response = home_page(request)

        self.assertIn('Wrong!', response.content.decode())
