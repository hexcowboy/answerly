from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase

from elasticsearch import Elasticsearch

from .models import Question


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
