from django.shortcuts import render
from .models import Quiz, Question, AnswerAnggota, User, Answer
from django.views.generic import ListView
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone


# Create your views here.
@login_required
def QuizListView(request):
	u = User.objects.get(username=f"{request.user.username}")
	quiz = Quiz.objects.all()
	return render(request, 'quizes/main.html', {'object_list': quiz, 'u': u})

def check_time(pk):
	nw = timezone.now()
	q = Quiz.objects.get(pk=pk)

	if q.start_date <= nw <= q.end_date:
		return True
	else:
		return False

@login_required
def quiz_view(request, pk, soal):
	if check_time(pk) == True:
		u = User.objects.get(username=f"{request.user.username}")
		quiz = Quiz.objects.get(pk=pk)
		q = quiz.get_questions()
		questions = q[int(soal)]
		if request.method == "POST":
			if questions.tipe == 'PG':
				try:
					a = AnswerAnggota.objects.get(question=questions, user=u.team)
					a.question = Question.objects.get(otp=request.POST["qotp"])
					a.answer = Answer.objects.get(otp=request.POST["jawaban"])
					a.save()

				except:
					Post = AnswerAnggota()
					Post.user = u.team
					Post.question = Question.objects.get(otp=request.POST["qotp"])
					Post.answer = Answer.objects.get(otp=request.POST["jawaban"])
					Post.save()
			elif questions.tipe == 'ES':
				try:
					a = AnswerAnggota.objects.get(question=questions, user=u.team)
					a.question = Question.objects.get(otp=request.POST["qotp"])
					a.answer_text = request.POST["jawaban"]
					a.save()
				except:
					Post = AnswerAnggota()
					Post.user = u.team
					Post.question = Question.objects.get(otp=request.POST["qotp"])
					Post.answer_text = request.POST["jawaban"]
					Post.save()
			if questions.tipe == 'AKM':
				if request.POST.get('jawaban', 'clear') == 'clear':
					try:
						a = AnswerAnggota.objects.get(question=questions, user=u.team)
						a.delete()
					except:
						return HttpResponseRedirect(request.path_info)
				else:
					try:
						a = AnswerAnggota.objects.get(question=questions, user=u.team)
						a.question = Question.objects.get(otp=request.POST["qotp"])
						a.answer_akm.add(Answer.objects.get(otp=request.POST["jawaban"]))
						a.save()

					except:
						Post = AnswerAnggota()
						Post.user = u.team
						Post.question = Question.objects.get(otp=request.POST["qotp"])
						Post.save()
						Post.answer_akm.add(Answer.objects.get(otp=request.POST["jawaban"]))
						Post.save()
		#         Post.pilihan = 5
		#         Post.checklist = True
	#         return redirect("/sesudah")



			return HttpResponseRedirect(request.path_info)
		else:
			try:
				a = AnswerAnggota.objects.get(question=questions, user=u.team)
			except:
				a = None
			# try:
			bis = {}
			for qis in range(1, len(q)+1):
				# bis[f"{qis}"].append(AnswerAnggota.objects.get(question=Question.objects.get(pk=qis),user=u))
				bis[f"{qis}"] = check_jawab(qis, u.team)
			# except:
			# 	b = None
			ans = questions.get_answer()
			ans = list(ans)
			return render(request, 'quizes/quiz.html', {'obj': quiz, 'bis': bis, 'pk': int(soal) + 1,'soal':questions, 'a':a, 'ans':ans, 'jumsol': len(q)})
	else:
		return HttpResponseRedirect(reverse("index"))

from django.template.defaulttags import register

# def selesai(request):
# 	u = User.objects.get(username=f"{request.user.username}")
# 	quiz = Quiz.objects.get(pk=pk)
# 	q = quiz.get_questions()
# 	r = Result.objects.








def logout_view(request):
    logout(request)
    return render(request, "login.html", {
        "message": "Keluar"
    })

def check_jawab(qis, u):
	try:
		AnswerAnggota.objects.get(question=Question.objects.get(pk=qis),user=u)
		return True
	except:
		return False

@register.filter
def get_range(value):
    return range(1, value+1)

@register.filter
def get_range_pas(value):
    return range(value)

@register.filter
def get_modulo(value):
    return int(value) % 5 == 0

@register.filter
def min_dua(value):
    return value - 2

@register.filter
def min_satu(value):
    return int(value) - 1

@register.filter
def plus_satu(value):
    return value + 1


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {
                    "message": "Tidak Ditemukan"
                })
        return render(request, "login.html")
    else:
        return redirect("/")