from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import searchProject, paginateProject
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here. Logic of our app
#Can respond with an html or json or whatever you want


def projects(request):

    projects, search_query = searchProject(request)
    projects, custom_range = paginateProject(request, projects, 3)    

    context = {"projects": projects, 'search_query' : search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id = pk)
    tags = projectObj.tags.all()
    reviews = projectObj.review_set.all() #Go to this project and give all the children, give the entire set
    context = {"project": projectObj, "tags": tags, "reviews": reviews}
    return render(request, 'projects/single-project.html', context)


@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    if request.method == 'POST':  # Check if it's a POST request
        form = ProjectForm(request.POST, request.FILES)  # Pass POST data to the form instance
        if form.is_valid():
            # Process valid form data
            project = form.save(commit=False)  # Or perform other actions with the cleaned data
            project.owner = profile
            project.save()
            # Redirect to success page or show confirmation message
            return redirect('account')  # Replace with your success URL pattern name
    else:
        form = ProjectForm() #Like this we build an instance of ProjectForm
    context = {'form': form}
    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    projectObj = Project.project_set.get(id = pk)
    form = ProjectForm(instance=projectObj)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=projectObj)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form': form}
    return render(request, 'projects/project-form.html', context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = Project.project_set.get(id = pk)

    if request.method == 'POST':
        project.delete()

        return redirect('/')

    return render(request, 'delete.html', {'object':project})
