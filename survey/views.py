from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from survey.models import Question, Answer, Valoration
from django.urls import reverse



class QuestionListView(ListView):
    model = Question

    def get_queryset(self):
        questions = Question.objects.all().order_by('-ranking')[:20]
        for question in questions:
            question.user_value = 0
            question.like_value = 0
            if self.request.user.is_authenticated:
                answer= Answer.objects.filter(author=self.request.user, question=question)
                if len(answer) != 0:
                    answer = answer.get()
                    question.user_value = answer.value
                valoration= Valoration.objects.filter(author=self.request.user, question=question)
                if len(valoration) != 0:
                    valoration = valoration.get()
                    question.like_value = valoration.value
            question.calculate_ranking() 
        return questions

class QuestionCreateView(CreateView):
    model = Question
    fields = ['title', 'description']
    redirect_url=''

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['title', 'description']
    template_name = 'survey/question_form.html'
    redirect_url='/'


def answer_question(request,question_id):
    if request.user.is_authenticated:
        question = Question.objects.get(pk=question_id)
        answer = Answer.objects.filter(question=question, author=request.user)
        if len(answer) == 0:
            answer = Answer.objects.create(author=request.user,question=question)
            question.total_answers+=1
            question.calculate_ranking() 
            question.save()
        else:
            answer=answer.get()
        answer.value=int(request.POST["response_value"])    
        answer.save()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/registration/login')

def like_dislike_question(request,question_id):
    if request.user.is_authenticated:
        value = int(request.POST["response_like_value"])
        question = Question.objects.get(pk=question_id)

        valoration=Valoration.objects.filter(question=question,author=request.user)
        if len(valoration) == 0:
            valoration = Valoration(author=request.user,question=question)
            question.likes+= 1 if value==1 else 0
            question.dislikes+= 1 if value==2 else 0
        else:
            valoration=valoration.get()
            if valoration.value != value:
                question.likes += 1 if value == 1 else (-1 if valoration.value == 1 else 0)
                question.dislikes += 1 if value == 2 else (-1 if valoration.value == 2 else 0)
        valoration.value = value
        valoration.save()
        question.calculate_ranking() 
        question.save()
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/registration/login')

