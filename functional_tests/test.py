from django.test import LiveServerTestCase
from selenium import webdriver

from selenium import webdriver
import unittest

from quizzes.models import Question


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

        first_question = Question()
        first_question.text = 'What is Your Name?'
        first_question.save()

        second_question = Question()
        second_question.text = 'What is Your Favorite Color?'
        second_question.save()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_quiz_and_retrieve_it_later(self):
        # John had heard of a cool new online quiz app.  He goes to check out
        # its homepage
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention quizzes
        header_text = self.browser.find_element_by_tag_name('h1').text

        self.assertIn('Quiz Time!', self.browser.title)
        self.assertIn('Quiz Time!', header_text)

        # He is invited to answer a multiple-choice question with 4 possible
        # answers right away
        # the question contains question text, 4 possible answers, and a submit
        # button
        question = self.browser.find_element_by_id('id_question')
        question_number = question.find_element_by_class_name(
            'question_number'
        )
        question_text = question.find_element_by_class_name('question_text')
        question_answers = question.find_elements_by_class_name('answer')
        submit_button = question.find_element_by_class_name('submit')

        self.assertEqual(len(question_answers), 4)
        self.assertEqual(question_number.text, 'Question Number: 1')
        self.assertEqual(question_text.text, "What is Your Name?")

        # He clicks one of the four answers, it is now the selected answer
        question_answers[0].click()

        # John then submits his answer by clicking the submit button
        submit_button.click()

        # The page updates, and the original question and answers are replaced
        # by a second question.  Above these, there is text informing John of
        # the correctness of his answer
        result = self.browser.find_element_by_id('id_result')
        result_text = result.find_element_by_class_name('result_text')

        self.assertEqual(
            'Correct!',
            result_text.text,
            'Unexpected result text. Expected "Correct!" --- Found: "%s"'
            % (result_text.text)
        )

        question = self.browser.find_element_by_id('id_question')
        question_number = question.find_element_by_class_name(
            'question_number'
        )
        question_text = question.find_element_by_class_name('question_text')
        question_answers = question.find_elements_by_class_name('answer')
        submit_button = question.find_element_by_class_name('submit')

        self.assertEqual(len(question_answers), 4)
        self.assertEqual(question_number.text, 'Question Number: 2')
        self.assertEqual(question_text.text, "What is Your Favorite Color?")

        # John wonders whether the site will remember his progress if he
        # leaves and returns to the site.  Then he sees that the site has
        # generated a unique URL for him -- there is some explanatory text to
        # that effect.

        # He visits that URL - the second quiz question is still there.

        # Satisfied, he leaves the rest of the quiz for the morning
