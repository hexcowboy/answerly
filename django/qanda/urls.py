from django.urls.conf import path

from . import views

app_name = 'qanda'
urlpatterns = [
    path(
        'ask',
        views.QuestionCreateView.as_view(),
        name='ask',
    ),
    path(
        'q/<int:pk>',
         views.QuestionDetailView.as_view(),
         name='question_detail',
    ),
    path(
        'q/<int:pk>/answer',
         views.AnswerCreateView.as_view(),
         name='answer_question',
    ),
    path(
        'a/<int:pk>/accept',
        views.AnswerAcceptanceUpdateView.as_view(),
        name='update_answer_acceptance',
    ),
    path(
        'daily/<int:year>/<int:month>/<int:day>/',
        views.DailyQuestionListView.as_view(),
        name='daily_questions',
    ),
    path(
        '',
        views.TodaysQuestionListView.as_view(),
        name='index',
    ),
]
