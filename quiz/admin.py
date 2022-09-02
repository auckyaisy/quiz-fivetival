from django.contrib import admin
from .models import Result, Quiz, Question, Answer, Team, AnswerAnggota, User

# Register your models here.
admin.site.register(Result)
admin.site.register(Quiz)

class AnswerInline(admin.TabularInline):
	model = Answer

class QuestionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(User)
admin.site.register(AnswerAnggota)
admin.site.register(Team)