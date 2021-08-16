from django.contrib import admin
from .models import Question, Answer, Valoration

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title','pk','created','author', 'description','likes','dislikes','ranking','total_answers')

admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Valoration)
