from unittest.mock import patch

import factory

from users.factories import UserFactory

from .models import Question


class QuestionFactory(factory.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'Question %d' % n)
    question = 'What is a question?'
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = Question

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        with patch('qanda.service.elasticsearch.Elasticsearch'):
            return super()._create(model_class, *args, **kwargs)
