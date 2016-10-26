from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_quiz_and_retrieve_it_later(self):
        # John had heard of a cool new online quiz app.  He goes to check out its
        # homepage
        self.browser.get('http://localhost:8000')

        # He notices the page title and header mention quizes
        self.assertIn('Quiz', self.browser.title)
        self.fail('Finish the test!')

        # He is invited to answer a multiple-choice question right away

        # He clicks one of the four answers, then submits his answer by clicking a
        # submit button underneath

        # The page updates, and the original question and answers are replaced by a
        # second question.  Above these, there is text informing John of the
        # correctness of his answer

        # John wonders whether the site will remember his progress if he leaves and
        # returns to the site.  Then he sees that the site has generated a unique URL
        # for him -- there is some explanatory text to that effect.

        # He visits that URL - the second quiz question is still there.

        # Satisfied, he leaves the rest of the quiz for the morning

if __name__ == '__main__':
    unittest.main(warnings='ignore')
