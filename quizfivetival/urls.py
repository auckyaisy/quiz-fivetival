"""quizfivetival URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

# default: "Django Administration"
admin.site.site_header = 'Fivetival Admin'
# default: "Site administration"
admin.site.index_title = 'bisa lihat sm ubah data link juknis'
# default: "Django site admin"
admin.site.site_title = 'Fivetival Admin'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("quiz.urls"))
]