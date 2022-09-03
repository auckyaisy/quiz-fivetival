from django.conf import settings
from django.urls import path

from . import views

urlpatterns = [
    path('', views.QuizListView, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('export', views.export, name='export'),
    path('quiz/<pk>/<soal>', views.quiz_view, name="quiz"),
    path('selesai/<pk>', views.selesai, name="selesai"),
]