
import csv, sys, os, django


project_dir = "/"
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'quizfivetival.settings'
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", __file__)
import django
django.setup()


from django.contrib.auth import authenticate
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


from django.contrib.auth import get_user_model

from django.contrib.auth.hashers import make_password
from django.conf import settings
from quiz.models import User, Team

file = 'eq.csv'

data = csv.reader(open(file), delimiter=",")
for row in data:
    Post = Team()
    Post.name = row[0]
    Post.lomba = row[5]
    Post.save()
