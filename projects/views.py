from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm

# Create your views here. Logic of our app
#Can respond with an html or json or whatever you want


def projects(request):
    projects = Project.objects.all()
    return render(request, 'projects/projects.html', {"projects": projects})

def project(request, pk):
    projectObj = Project.objects.get(id = pk)
    tags = projectObj.tags.all()
    reviews = projectObj.review_set.all() #Go to this project and give all the children, give the entire set
    context = {"project": projectObj, "tags": tags, "reviews": reviews}
    return render(request, 'projects/single-project.html', context)

def createProject(request):
    if request.method == 'POST':  # Check if it's a POST request
        form = ProjectForm(request.POST, request.FILES)  # Pass POST data to the form instance
        if form.is_valid():
            # Process valid form data
            form.save()  # Or perform other actions with the cleaned data
            # Redirect to success page or show confirmation message
            return redirect('/')  # Replace with your success URL pattern name
    else:
        form = ProjectForm() #Like this we build an instance of ProjectForm
    context = {'form': form}
    return render(request, 'projects/project-form.html', context)

def updateProject(request, pk):
    projectObj = Project.objects.get(id = pk)
    form = ProjectForm(instance=projectObj)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=projectObj)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'projects/project-form.html', context)

def deleteProject(request, pk):
    project = Project.objects.get(id = pk)

    if request.method == 'POST':
        project.delete()

        return redirect('/')

    return render(request, 'projects/delete.html', {'object':project})
