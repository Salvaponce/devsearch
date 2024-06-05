from .models import Skill, Profile
from django.db.models import Q


def searchDev(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

        skills = Skill.objects.filter(name__icontains = search_query)

    #Search profile by dev name or short_bio
    profiles = Profile.objects.distinct().filter(Q(name__icontains = search_query) | 
                                      Q(short_bio__icontains = search_query) |
                                      Q(skill__in = skills))
    
    return profiles, search_query