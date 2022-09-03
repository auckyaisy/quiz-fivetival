
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
    Post = User()
    Post.password = make_password(row[2])
    Post.is_superuser = "0"
    Post.username = row[4]
    Post.first_name = row[1]
    Post.is_staff = "0"
    Post.is_active = "1"
    Post.role = row[3]
    Post.team = Team.objects.get(name=row[0])
    Post.save()
