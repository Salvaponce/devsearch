from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import CustomCreationForm

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


def profiles(request):
    profiles = Profile.objects.all()
    return render(request, 'users/profiles.html', {'profiles': profiles})


def userProfile(request, pk):
    profile = Profile.objects.get(id = pk)

    topSkills = profile.skill_set.exclude(description__exact = "")
    otherSkills = profile.skill_set.filter(description = "")

    context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}

    return render(request, 'users/user-profile.html', context)


def loginUser(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "User doesn not exist.") #Something to fix
            return redirect('login')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user) #Create a session for the user, add that to our browser cookies
            return redirect('profiles')
        else:
            messages.error(request,'Username or password is incorrect')
            
    context = {'page': page}
    return render(request, 'users/login_register.html', context)


def registerUser(request):
    form = CustomCreationForm()
    page = 'register'

    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) #We are saving out user bur holding a temperary instance of this user
            user.username = user.username.lower() #Now we know that every user is not the same but capitalize
            user.save()

            messages.success(request, "User account was crated")
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'An error has occured during registration')
        

    context = {'page': page, 'form': form}
    return render(request, 'users/login_register.html', context)


def logoutUser(request):
    logout(request)
    messages.success(request, "User was logged out")
    return redirect('login')

@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.projects_set.all()

    context = {'profile': profile, 'skills': skills, 'projects': projects}
    return render(request, 'users/account.html', context)