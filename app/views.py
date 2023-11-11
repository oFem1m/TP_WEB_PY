from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, InvalidPage
from .models import Question, Answer, Tag
from .managers import QuestionManager

STATS = {
    'tags': ['tag_0', 'tag_72', 'tag_12', 'tag_87', 'tag_40', 'tag_45', 'tag_21', 'tag_94', 'tag_11', 'tag_3'],
    'best_members': ['Member 1', 'Member 2', 'Member 3', 'Member 4', 'Member 5'],
}


def paginate(objects, per_page=15, request=None):
    page = request.GET.get('page', 1) if request else 1
    paginator = Paginator(objects, per_page)
    try:
        page_obj = paginator.page(page)
        page_range = paginator.get_elided_page_range(page, on_each_side=1)
    except InvalidPage as e:
        page = 1
        page_obj = paginator.page(page)
        page_range = paginator.get_elided_page_range(page, on_each_side=1)
    return page_obj, page_range


def index(request):
    questions = Question.objects.get_best_questions()
    page_obj, pagination_buttons = paginate(questions, request=request)
    return render(request, 'index.html',
                  {'page_obj': page_obj, 'page_title': 'Questions', 'stats': STATS,
                   'pagination': pagination_buttons})


def question(request, question_id):
    question_item = Question.objects.get(pk=question_id)
    answers = Answer.objects.get_hot_answers().filter(question=question_item)
    page_obj, pagination_buttons = paginate(answers, request=request)
    return render(request, 'question.html',
                  {'question': question_item, 'page_obj': page_obj, 'stats': STATS, 'pagination': pagination_buttons})


def ask(request):
    return render(request, 'ask.html', {'stats': STATS})


def login(request):
    return render(request, 'login.html', {'stats': STATS})


def signup(request):
    return render(request, 'register.html', {'stats': STATS})


def tag(request, tag_id):
    tag = get_object_or_404(Tag, name__iexact=tag_id)
    questions = Question.objects.filter(tags=tag)
    page_obj, pagination_buttons = paginate(questions, request=request)
    return render(request, 'index.html',
                  {'page_obj': page_obj, 'page_title': f'Tag: {tag.name}', 'stats': STATS,
                   'pagination': pagination_buttons})


def hot(request):
    questions = Question.objects.get_hot_questions()
    page_obj, pagination_buttons = paginate(questions, request=request)
    return render(request, 'index.html',
                  {'page_obj': page_obj, 'page_title': 'Hot Questions', 'stats': STATS,
                   'pagination': pagination_buttons})
