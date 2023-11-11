from django.db import models
from .managers import QuestionManager, AnswerManager
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/')


class Tag(models.Model):
    name = models.CharField(max_length=50)


class Question(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def get_num_answers(self):
        return self.answer_set.count()

    def likes_count(self):
        return self.likes.count()

    def dislikes_count(self):
        return self.dislikes.count()

    objects = QuestionManager()


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    objects = AnswerManager()

    def likes_count(self):
        return self.likes.count()

    def dislikes_count(self):
        return self.dislikes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE, related_name='likes')
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE, related_name='dislikes')
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE, related_name='dislikes')
    created_at = models.DateTimeField(auto_now_add=True)
