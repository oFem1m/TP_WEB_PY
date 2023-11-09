from django.shortcuts import render
from django.core.paginator import Paginator, InvalidPage

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'content': f'Lorem Ipsum {i}',
        'num_answers': i,
        'tags': ['math'],
    } for i in range(2500)
]

STATS = {
    'tags': ['Cras', 'Dapibus', 'Morbi', 'Porta', 'Vestibulum'],
    'best_members': ['Member 1', 'Member 2', 'Member 3', 'Member 4', 'Member 5'],
}

REPLY = {
    'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit. '
               'Atque corporis delectus repudiandae? Accusamus, accusantium '
               'atque culpa debitis, deserunt, dignissimos dolor doloremque '
               'ducimus esse est et harum hic laudantium libero minima nesciunt '
               'nostrum obcaecati possimus quis quos repellendus voluptate voluptatem voluptates.'
}


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


def question(request):
    return render(request, 'question.html', {'stats': STATS})


def ask(request):
    return render(request, 'ask.html', {'stats': STATS})


def login(request):
    return render(request, 'login.html', {'stats': STATS})


def signup(request):
    return render(request, 'register.html', {'stats': STATS})
