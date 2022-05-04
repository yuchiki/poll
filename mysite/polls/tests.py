"""test module"""

import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


class QuestionModelTests(TestCase):
    """tests for Question Model"""

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is in the future.
        """

        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=-1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() return sTrue for questions whose pub_ddate is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a quesiton with the given `question_test` and published the given number of `days`
    offset to now
    (negative for question publiushed in the pass,
    positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_future_question():
    """
    未来のpub_dateを持つquestionを作成します。
    """
    return create_question("Future Question", 5)


def create_past_question():
    """
    過去のpub_dateを持つquesionを作成します。
    """
    return create_question("Past Question", -5)


class QuestionIndexViewTests(TestCase):
    """tests for Question Index View"""

    def view_index(self):
        """index URLを叩くヘルパー関数"""
        return self.client.get(reverse('polls:index'))

    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.view_index()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the index page.
        """
        question = create_past_question()
        response = self.view_index()
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question]
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future are not displayed on the index page.
        """
        create_future_question()
        response = self.view_index()
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions are displayed.

        """
        question = create_past_question()
        create_future_question()
        response = self.view_index()
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_past_question()
        question2 = create_past_question()
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    """ tests for Question Detail view"""

    def view_detail(self, question):
        """ detailページを質問をもとに叩くヘルパー関数"""
        return self.view_detail_with_id(question.id)

    def view_detail_with_id(self, question_id):
        """ detailページを質問IDをもとに叩くヘルパー関数"""
        url = reverse('polls:detail', args=[question_id])
        return self.client.get(url)

    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future returns a 404 not found.
        """
        future_question = create_future_question()
        response = self.view_detail(future_question)

        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past displays the question's text
        """

        past_question = create_past_question()
        response = self.view_detail(past_question)
        self.assertContains(response, past_question.question_text)

    def test_dummy(self):
        self.assertTrue(False)
