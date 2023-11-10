from django.db import models
from django.db.models import F, ExpressionWrapper, fields


class QuestionManager(models.Manager):
    def get_newest_questions(self):
        return self.order_by('-created_at')

    def get_best_questions(self):
        return self.annotate(score=ExpressionWrapper(
            F('like_set__count', output_field=fields.IntegerField()) -
            F('dislike_set__count', output_field=fields.IntegerField()),
            output_field=fields.IntegerField()
        )).order_by('-score')
