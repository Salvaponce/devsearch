from django.db import models
import uuid
from users.models import Profile

# Create your models here. Data base

class Project(models.Model): #We inherance from models. Meaning we create a officiallly a django model
    owner = models.ForeignKey(Profile, on_delete= models.SET_NULL, null=True, blank = True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True) #null is for the db. blanck is for django.
    featured_image = models.ImageField(null=True, blank=True, default = 'file-notfound.jpg')
    demo_link = models.CharField(max_length=1200, null=True, blank=True)
    source_link = models.CharField(max_length=1200, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True) #Is a string because the model Tag is below this model
    vote_total = models.IntegerField(default=0)
    vote_ratio = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title


class Review(models.Model):

    VOTE_TYPE = (
        ('up', 'up'),
        ('down', 'down')
    )

    #owner = 
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=50, choices=VOTE_TYPE)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.project.title + " || " + self.value
    

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.name
