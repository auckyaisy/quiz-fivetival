
from quiz.models import User, Team
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth import authenticate
import django
import csv
import sys
import os
import django


project_dir = "/"
sys.path.append(project_dir)
os.environ['DJANGO_SETTINGS_MODULE'] = 'quizfivetival.settings'
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", __file__)
django.setup()


# User = get_user_model()

file = 'eq.csv'

data = csv.reader(open(file), delimiter=",")
for row in data:
    Post = Team()
    Post.name = row[0]
    Post.lomba = row[5]
    Post.save()
