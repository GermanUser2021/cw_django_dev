from django.urls import path

from survey.views import (QuestionListView,
                          QuestionCreateView,
                          QuestionUpdateView,
                          answer_question,
                          like_dislike_question)

urlpatterns = [
    path('', QuestionListView.as_view(), name='question-list'),
    path('question/add/', QuestionCreateView.as_view(), name='question-create'),
    path('question/edit/<int:pk>', QuestionUpdateView.as_view(), name='question-edit'),
    path('question/<int:question_id>/answer', answer_question, name='question-answer'),
    path('question/<int:question_id>/like', like_dislike_question, name='question-like'),


]