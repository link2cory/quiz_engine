from django.core.urlresolvers import resolve
from django.template.loader import render_to_string
from django.test import TestCase
from django.http import HttpRequest

from quizzes.views import home_page
from quizzes.models import Question

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

    def setUp(self):
        first_question = Question()
        first_question.text = 'What is Your Name?'
        first_question.save()

        first_question.answer.create(text="John")
        first_question.answer.create(text="Jacob")
        first_question.answer.create(text="Jingleheimer")
        first_question.answer.create(text="Schmidt")

        second_question = Question()
        second_question.text = 'What is Your Favorite Color?'
        second_question.save()

        second_question.answer.create(text="Red")
        second_question.answer.create(text="Blue")
        second_question.answer.create(text="Yellow")
        second_question.answer.create(text="I Don't Know")

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')

        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()

        response = home_page(request)
        expected_html = render_to_string('home.html', request=request)

        self.assertIn('What is Your Name?', response.content.decode())
        self.assertIn('Question Number: 1', response.content.decode())

    def test_home_page_handles_POST_request_correct_answer(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['answer'] = 'John'

        response = home_page(request)

        self.assertIn('Correct!', response.content.decode())
        self.assertIn('Question Number: 2', response.content.decode())
        self.assertIn(
            'What is Your Favorite Color?',
            response.content.decode()
        )

    def test_home_page_handles_POST_request_incorrect_answer(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['answer'] = 'Jacob'

        response = home_page(request)

        self.assertIn('Wrong!', response.content.decode())
        self.assertIn('Question Number: 2', response.content.decode())
        self.assertIn(
            'What is Your Favorite Color?',
            response.content.decode()
        )


class QuestionModelTest(TestCase):

    def test_saving_and_retrieving_questions(self):
        first_question = Question()
        first_question.text = 'What is Your Name?'
        first_question.save()

        second_question = Question()
        second_question.text = 'What is Your Favorite Color?'
        second_question.save()

        saved_questions = Question.objects.all()
        first_saved_question = saved_questions[0]
        second_saved_question = saved_questions[1]

        self.assertEqual(saved_questions.count(), 2)
        self.assertEqual(first_saved_question.text, first_question.text)
        self.assertEqual(second_saved_question.text, second_question.text)
