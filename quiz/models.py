from django.db import models
from django.contrib.auth.models import AbstractUser

def MakeOTP():
    import random,string
    return ''.join(random.choices(string.ascii_uppercase +
                                            string.ascii_lowercase +
                                            string.digits, k=6))

# Create your models here.
class Team(models.Model):
	lolos = models.BooleanField(default=False)
	jenis_lomba = [
            ('SB', 'SPELLING BEE'),
            ('EQ', 'ENGLISH QUIZ'),
        ]
	lomba = models.CharField(max_length=2, choices=jenis_lomba)
	name = models.CharField(max_length=120)
	def __str__(self):
		return f"{self.name}"

class User(AbstractUser):
	role = models.IntegerField(default=1)
	team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
	# def save(self,*args,**kwargs):
	# 	created = not self.pk
	# 	super().save(*args,**kwargs)
	# 	if created:
	# 		AnswerAnggota.objects.create(user=self)


class Quiz(models.Model):
	start_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
	end_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
	time = models.IntegerField(blank=True, null=True)
	name = models.CharField(max_length=120)
	topic = models.CharField(max_length=120)
	number_of_questions = models.IntegerField()

	def __str__(self):
		return f"{self.name}"

	def get_questions(self):
		return self.question_set.all()[:self.number_of_questions]

class Sesi(models.Model):
	start_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
	end_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	team = models.ForeignKey(
	    Team, on_delete=models.CASCADE, blank=True, null=True)
	time = models.IntegerField(blank=True, null=True)

	def __str__(self):
		return f"{self.team} | {self.quiz}: {self.start_date} - {self.end_date}"

class Question(models.Model):
	otp = models.CharField(max_length=7, default=MakeOTP)
	text = models.TextField()
	level_soal = [
            ('EASY', 'EASY'),
            ('MEDI', 'MEDIUM'),
            ('HARD', 'HARD'),
            ('SEMI', 'SEMIFINAL'),
        ]
	level = models.CharField(max_length=4, choices=level_soal)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	song = models.TextField(blank=True, null=True)
	tipe_soal = [
    ('PG', 'Multiple Choice/ Sejenis'),
    ('ES', 'Esai'),
    ('AKM', 'AKM'),
	('SB', 'Spelling Bee')
	]
	tipe = models.CharField(
        max_length=3,
        choices=tipe_soal,
    )

	def __str__(self):
		return str(self.text)

	def get_answer(self):
		return self.answer_set.all()

class Answer(models.Model):
	otp = models.CharField(max_length=7, default=MakeOTP)
	text = models.TextField()
	correct = models.BooleanField(default=False)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)

	def __str__(self):
		return f"question: {self.question.text}, answer: {self.text}, correct: {self.correct}"

class AnswerAnggota(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='re_answer', blank=True, null=True)
	user = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
	answer_akm = models.ManyToManyField(Answer, related_name='re_answer_akm', blank=True, null=True)
	answer_text = models.TextField(blank=True, null=True)
	score = models.IntegerField(default=0)

	def __str__(self):
		return f"{self.question.text}, {self.user}"

class Result(models.Model):
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	score = models.FloatField()
	team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, null=True)
	selesai = models.BooleanField(default=False)
	finish_date = models.DateTimeField(auto_now_add=False, blank=True, null=True)

	def __str__(self):
		return f"{self.team} | {self.score} | {self.quiz}"