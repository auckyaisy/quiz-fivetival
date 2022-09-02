from django.shortcuts import render
from .models import Quiz, Question, AnswerAnggota, User, Answer, Result
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
	k = {}
	for q in quiz:
		try:
			a = Result.objects.get(quiz=q, team=u.team)
			k[q] = True
		except:
			k[q] = False
	return render(request, 'quizes/main.html', {'object_list': quiz, 'u': u, 'k': k})

def check_time(pk):
	nw = timezone.now()
	q = Quiz.objects.get(pk=pk)

	if q.start_date <= nw <= q.end_date:
		return True
	else:
		return False


def check_quiz(pk, user):
	try:
		a = Result.objects.get(quiz=Quiz.objects.get(pk=pk), team=user.team)
		return True
	except:
		return False

@login_required
def quiz_view(request, pk, soal):
	u = User.objects.get(username=f"{request.user.username}")
	if check_quiz(pk, u) == False:
		if check_time(pk) == True:
			quiz = Quiz.objects.get(pk=pk)
			q = quiz.get_questions()
			questions = q[int(soal)]
			if request.method == "POST":
				if questions.tipe == 'PG':
					try:
						a = AnswerAnggota.objects.get(question=questions, user=u.team)
						a.score = 0
						a.question = Question.objects.get(otp=request.POST["qotp"])
						a.answer = Answer.objects.get(otp=request.POST["jawaban"])
						if a.answer.correct == True:
							if a.question.level == "EASY":
								a.score += 3
							elif a.question.level == "MEDI":
								a.score += 4
							elif a.question.level == "HARD":
								a.score += 6
							else:
								a.score += 5
						else:
							if a.question.level == "EASY":
								a.score -= 1
							elif a.question.level == "MEDI":
								a.score -= 2
							elif a.question.level == "HARD":
								a.score -= 3
						a.save()

					except:
						Post = AnswerAnggota()
						Post.user = u.team
						Post.question = Question.objects.get(otp=request.POST["qotp"])
						Post.answer = Answer.objects.get(otp=request.POST["jawaban"])
						if Post.answer.correct == True:
							if Post.question.level == "EASY":
								Post.score += 3
							elif Post.question.level == "MEDI":
								Post.score += 4
							elif Post.question.level == "HARD":
								Post.score += 6
							else:
								Post.score += 5
						else:
							if Post.question.level == "EASY":
								Post.score -= 1
							elif Post.question.level == "MEDI":
								Post.score -= 2
							elif Post.question.level == "HARD":
								Post.score -= 3
						Post.save()
						Post.save()
				elif questions.tipe == 'ES':
					try:
						a = AnswerAnggota.objects.get(question=questions, user=u.team)
						a.score = 0
						a.question = Question.objects.get(otp=request.POST["qotp"])
						a.answer_text = request.POST["jawaban"]
						if a.answer_text.lower() == Answer.objects.get(question=a.question).text:
							if a.question.level == "EASY":
								a.score += 3
							elif a.question.level == "MEDI":
								a.score += 4
							elif a.question.level == "HARD":
								a.score += 6
							else:
								a.score += 5
						elif a.answer_text.lower() == "":
							if a.question.level == "EASY":
								a.score -= 1
							elif a.question.level == "SEMI":
								a.score -= 2
						else:
							if a.question.level == "EASY":
								a.score -= 1
							elif a.question.level == "MEDI":
								a.score -= 2
							elif a.question.level == "HARD":
								a.score -= 3
						a.save()
					except:
						Post = AnswerAnggota()
						Post.user = u.team
						Post.question = Question.objects.get(otp=request.POST["qotp"])
						Post.answer_text = request.POST["jawaban"]
						if Post.answer_text.lower() == Answer.objects.get(question=Post.question).text:
							if Post.question.level == "EASY":
								Post.score += 3
							elif Post.question.level == "MEDI":
								Post.score += 4
							elif Post.question.level == "HARD":
								Post.score += 6
							else:
								Post.score += 5
						elif Post.answer_text.lower() == "":
							if Post.question.level == "EASY":
								Post.score -= 1
							elif Post.question.level == "SEMI":
								Post.score -= 2
						else:
							if Post.question.level == "EASY":
								Post.score -= 1
							elif Post.question.level == "MEDI":
								Post.score -= 2
							elif Post.question.level == "HARD":
								Post.score -= 3
						Post.save()
				elif questions.tipe == 'AKM':
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
				elif questions.tipe == 'SB':
					try:
						a = AnswerAnggota.objects.get(question=questions, user=u.team)
						a.score = 0
						a.question = Question.objects.get(otp=request.POST["qotp"])
						a.answer_text = request.POST["jawaban"]
						if a.answer_text.lower() == Answer.objects.get(question=a.question).text:
							if a.question.level == "EASY":
								a.score += 3
							elif a.question.level == "MEDI":
								a.score += 5
						a.save()
					except:
						Post = AnswerAnggota()
						Post.user = u.team
						Post.question = Question.objects.get(otp=request.POST["qotp"])
						Post.answer_text = request.POST["jawaban"]
						if Post.answer_text.lower() == Answer.objects.get(question=Post.question).text:
							if Post.question.level == "EASY":
								Post.score += 3
							elif Post.question.level == "MEDI":
								Post.score += 5
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
				# except:(
				# 	b = None
				ans = questions.get_answer()
				ans = list(ans)
				return render(request, 'quizes/quiz.html', {'obj': quiz, 'bis': bis, 'pk': int(soal) + 1,'soal':questions, 'a':a, 'ans':ans, 'pksoal':pk, 'jumsol': len(q)})
		else:
			return HttpResponseRedirect(reverse("index"))
	else:
		return HttpResponseRedirect(reverse("index"))

from django.template.defaulttags import register

def selesai(request, pk):
	u = User.objects.get(username=f"{request.user.username}")
	quiz = Quiz.objects.get(pk=pk)
	try:
		a = Result.objects.get(quiz=quiz, user=u.team)
		return HttpResponseRedirect(reverse("index"))
	except:
		q = quiz.get_questions()
		r = Result()
		r.quiz = quiz
		score = 0
		for i in range(len(q)):
			try:
				ans = AnswerAnggota.objects.get(question=q[i], user=u.team)
				score += ans.score
			except:
				for k in q:
					if not k.tipe_soal == 'SB':
						if k.level == "EASY":
							score -= 1
						elif k.level == "SEMI":
							score -= 2
		r.score = score
		r.selesai = True
		r.finish_date = timezone.now()
		r.team = u.team
		r.save()

		return HttpResponseRedirect(reverse("index"))

	








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