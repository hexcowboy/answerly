from datetime import date

from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
# from django.utils.dateparse import parse_datetime
from django.template.defaultfilters import date as _date
from django.template.defaultfilters import time as _time

from .factories import QuestionFactory
from .models import Question
from .views import DailyQuestionListView


class QuestionSaveTestCase(TestCase):
    """
    Tests Question.save()
    """

    @patch('qanda.service.elasticsearch.Elasticsearch')
    def test_elasticsearch_upsert_on_save(self, ElasticsearchMock):
        user = get_user_model().objects.create_user(
            username='unittest',
            password='unittest123',
        )
        question_title = 'Unit test'
        question_body = 'long text here'
        question = Question(
            title=question_title,
            question=question_body,
            user=user,
        )
        question.save()
        self.assertIsNotNone(question.id)
        self.assertTrue(ElasticsearchMock.called)
        mock_client = ElasticsearchMock.return_value
        mock_client.update.assert_called_once_with(
            settings.ES_INDEX,
            'doc',
            id=question.id,
            body={
                'doc': {
                    'text': '{}\n{}'.format(question_title, question_body),
                    'question_body': question_body,
                    'title': question_title,
                    'id': question.id,
                    'created': question.created,
                },
                'doc_as_upsert': True,
            }
        )


class DailyQuestionListTestCase(TestCase):
    """
    Tests the DailyQuestionListView
    """
    QUESTION_LIST_NEEDLE_TEMPLATE = '''
    <li>
        <a href="/q/{id}">{title}</a>
        by {username} on {date}
    </li>
    '''
    REQUEST = RequestFactory().get(path='/q/2030-12-31')
    TODAY = date.today()

    def test_GET_on_day_with_many_questions(self):
        todays_questions = [QuestionFactory() for _ in range(10)]
        response = DailyQuestionListView.as_view()(
            self.REQUEST,
            year=self.TODAY.year,
            month=self.TODAY.month,
            day=self.TODAY.day
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(10, response.context_data['object_list'].count())
        rendered_content = response.rendered_content

        for question in todays_questions:
            needle = self.QUESTION_LIST_NEEDLE_TEMPLATE.format(
                id=question.id,
                title=question.title,
                username=question.user.username,
                date=_date(question.created) + ', ' + _time(question.created)
                # date=question.created.strftime(settings.DATETIME_FORMAT)
            )
            self.assertInHTML(needle, rendered_content)
