from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage

QUESTIONS = [
    {
        'id': i,
        'title': f'Question №{i}',
        'content': 'I can\'t solve this problem',
        'num_answers': 50,
        'tags': ['test'],
    } for i in range(200)
]

STATS = {
    'tags': ['Cras', 'Dapibus', 'Morbi', 'Porta', 'Vestibulum', 'Cras', 'Dapibus', 'Morbi', 'Porta', 'Vestibulum'],
    'best_members': ['Member 1', 'Member 2', 'Member 3', 'Member 4', 'Member 5'],
}

REPLY = [
    {
        'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. '
                   'Cupiditate ea eos, est facere facilis itaque pariatur tenetur! '
                   'Consequatur cum cumque delectus dolor dolorum expedita explicabo '
                   'inventore labore nostrum placeat quia quidem ratione, repellendus '
                   'sapiente vitae? Et facilis rem repellendus suscipit.',

    } for i in range(30)
]


def paginate(request, objects, per_page=15):
    page = request.GET.get('page', 1)
    paginator = Paginator(objects, per_page)
    try:
        page_obj = paginator.page(page)
        page_range = paginator.get_elided_page_range(page, on_each_side=1)
    except InvalidPage as e:
        page = 1
        page_obj = paginator.page(page)
        page_range = paginator.get_elided_page_range(page, on_each_side=1)
    return page_obj, page_range


# Create your views here.
def index(request):
    page_obj, pagination_buttons = paginate(request, QUESTIONS)
    return render(request, 'index.html',
                  {'page_obj': page_obj, 'page_title': 'Questions', 'stats': STATS,
                   'pagination': pagination_buttons})


def question(request, question_id):
    item = QUESTIONS[question_id]
    page_obj, pagination_buttons = paginate(request, REPLY)
    return render(request, 'question.html',
                  {'question': item, 'page_obj': page_obj, 'stats': STATS, 'pagination': pagination_buttons})


def ask(request):
    return render(request, 'ask.html', {'stats': STATS})


def login(request):
    return render(request, 'login.html', {'stats': STATS})


def signup(request):
    return render(request, 'register.html', {'stats': STATS})


def tag(request, tag_id):
    page_obj, pagination_buttons = paginate(request, QUESTIONS)
    return render(request, 'index.html',
                  {'page_obj': page_obj, 'page_title': f'Tag: {tag_id}', 'stats': STATS,
                   'pagination': pagination_buttons})


def hot(request):
    page_obj, pagination_buttons = paginate(request, QUESTIONS)
    return render(request, 'index.html',
                  {'page_obj': page_obj, 'page_title': 'Hot Questions', 'stats': STATS,
                   'pagination': pagination_buttons})
