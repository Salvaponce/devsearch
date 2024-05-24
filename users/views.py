from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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

    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, "User doesn not exist.") #Something to fix

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user) #Create a session for the user, add that to our browser cookies
            return redirect('profiles')
        else:
            messages.error(request,'Username or password is incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.success(request, "User was logged out")
    return redirect('login')