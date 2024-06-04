from django.shortcuts import render
from .models import Task

# Create your views here.
def to_do(request):
    lst = request.user.task_set.all()
    context = {'lista': lst}
    return render(request, 'tasks/to-do_list.html', context)