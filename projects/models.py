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

    class Meta:
        ordering = ['-created']

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVote = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVote / totalVotes) * 100

        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):

    VOTE_TYPE = (
        ('up', 'up'),
        ('down', 'down')
    )

    owner = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True) #One to many relationship
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=50, choices=VOTE_TYPE)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self) -> str:
        return self.project.title + " || " + self.value
    

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self) -> str:
        return self.name
