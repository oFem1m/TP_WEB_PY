import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, Like, Dislike
import uuid
from faker import Faker


class Command(BaseCommand):
    help = 'Fill the database with test data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Coefficient for filling entities')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        fake = Faker()

        # Создаем пользователей
        users = []
        for i in range(ratio):
            user = User.objects.create(username=f'user_{i}_{ratio}_{uuid.uuid4()}', password='password')
            users.append(user)

        # Создаем тэги
        tags = []
        for i in range(ratio):
            tag = Tag.objects.create(name=f'Tag_{i}')
            tags.append(tag)

        # Создаем вопросы
        for i in range(ratio * 10):
            author = users[i % ratio]
            question = Question.objects.create(author=author, title=f'Title {i}', content=fake.text())
            question.tags.add(tags[i % ratio])

        # Создаем ответы
        for i in range(ratio * 100):
            author = users[i % ratio]
            question = Question.objects.get(pk=i % (ratio * 10) + 1)  # Получаем вопрос по id
            answer = Answer.objects.create(author=author, question=question, content=fake.text())

        # Создаем лайки и дислайки для вопросов
        for i in range(ratio * 10):
            question = Question.objects.get(pk=i + 1)  # Получаем вопрос по id
            total_ratings = ratio * 2  # В среднем 2 оценки на вопрос

            for j in range(total_ratings):
                user = random.choice(users)
                is_like = random.choice([True, False])  # Решаем, будет это лайк или дислайк

                if is_like:
                    like = Like.objects.create(user=user, question=question)
                else:
                    dislike = Dislike.objects.create(user=user, question=question)

        # Создаем лайки и дислайки для ответов
        for i in range(ratio * 100):
            answer = Answer.objects.get(pk=i + 1)  # Получаем ответ по id
            total_ratings = ratio * 2  # В среднем 2 оценки на ответ

            for j in range(total_ratings):
                user = random.choice(users)
                is_like = random.choice([True, False])  # Решаем, будет это лайк или дислайк

                if is_like:
                    like = Like.objects.create(user=user, answer=answer)
                else:
                    dislike = Dislike.objects.create(user=user, answer=answer)

        # Выводим сообщение об успешном заполнении базы данных
        self.stdout.write(self.style.SUCCESS(f'Successfully filled the database with test data (ratio={ratio}).'))
