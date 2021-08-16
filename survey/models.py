from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.shortcuts import redirect
from django.utils import timezone

from datetime import date


class Question(models.Model):
    created = models.DateField('Creada', default=timezone.now)
    author = models.ForeignKey(get_user_model(), related_name="questions", verbose_name='Pregunta',
                               on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción')
    valorations = models.ManyToManyField(get_user_model(), through='Valoration')
    likes = models.PositiveIntegerField("Likes", default=0)
    dislikes = models.PositiveIntegerField("Dislikes", default=0)
    ranking = models.PositiveIntegerField("Ranking", default=0)
    total_answers = models.PositiveIntegerField("TotalAnswers", default=0)
    def get_absolute_url(self):
        return reverse('survey:question-edit', args=[self.pk])

    def calculate_ranking(self):
        self.ranking = self.total_answers*10+self.likes*5-3*self.dislikes
        if self.created >= date.today():
            self.ranking += 10
    def __str__(self):
        return self.title




class Valoration(models.Model):
    VALORATION_VALUES = ((0,'Sin valor'),
                      (1,'Like'),
                      (2,'Dislike'),)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value =  models.PositiveIntegerField("Valoracion", default=0, choices=VALORATION_VALUES)


class Answer(models.Model):
    ANSWERS_VALUES = ((0,'Sin Responder'),
                      (1,'Muy Bajo'),
                      (2,'Bajo'),
                      (3,'Regular'),
                      (4,'Alto'),
                      (5,'Muy Alto'),)
    created = models.DateField('Creada', auto_now_add=True)
    question = models.ForeignKey(Question, related_name="answers", verbose_name='Pregunta', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), related_name="answers", verbose_name='Autor', on_delete=models.CASCADE)
    value = models.PositiveIntegerField("Respuesta", default=0, choices=ANSWERS_VALUES)
    comment = models.TextField("Comentario", default="", blank=True)
    def __str__(self):
        return self.question.title+" "+str(self.author)
