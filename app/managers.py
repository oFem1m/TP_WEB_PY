from django.db import models
from django.db.models import F, Count, Subquery, OuterRef


class QuestionManager(models.Manager):
    def get_newest_questions(self):
        return self.order_by('-created_at')

    def get_best_questions(self):
        from .models import Like, Dislike
        # Используем Subquery для подсчета лайков и дислайков
        likes_count_subquery = Subquery(
            Like.objects.filter(question=OuterRef('pk')).values('question')
            .annotate(likes_count=Count('id')).values('likes_count')[:1]
        )
        dislikes_count_subquery = Subquery(
            Dislike.objects.filter(question=OuterRef('pk')).values('question')
            .annotate(dislikes_count=Count('id')).values('dislikes_count')[:1]
        )

        # Создаем вычисляемое поле для разницы между лайками и дислайками
        questions = self.annotate(
            likes_count=likes_count_subquery,
            dislikes_count=dislikes_count_subquery,
            score=F('likes_count') - F('dislikes_count')
        )

        # Сортируем вопросы по убыванию значения (лайки - дислайки)
        questions = questions.order_by('-score')

        return questions

    def get_hot_questions(self):
        from .models import Like

        likes_count_subquery = Subquery(
            Like.objects.filter(question=OuterRef('pk')).values('question')
            .annotate(likes_count=Count('id')).values('likes_count')[:1]
        )

        questions = self.annotate(likes_count=likes_count_subquery)

        questions = questions.order_by('-likes_count')

        return questions


class AnswerManager(models.Manager):
    def get_hot_answers(self):
        from .models import Like

        likes_count_subquery = Subquery(
            Like.objects.filter(answer=OuterRef('pk')).values('answer')
            .annotate(likes_count=Count('id')).values('likes_count')[:1]
        )

        answers = self.annotate(likes_count=likes_count_subquery)

        answers = answers.order_by('-likes_count')

        return answers


