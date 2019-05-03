from django.urls.conf import path

from . import views

app_name = 'qanda'
url_patterns = [
    path('ask', views.AskQuestionView.as_view(), name='ask'),
    path('q/<int:pk>' views.QuestionDetailView.as_view(), name='question_detail'),
]
