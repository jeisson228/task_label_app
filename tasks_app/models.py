from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class Label(models.Model):
    name = models.CharField(max_length=50, validators=[MinLengthValidator(1)], unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='labels')

    class Meta:
        unique_together = ['name', 'owner']
        ordering = ['name']

    def __str__(self):
        return self.name

class Task(models.Model):
    title = models.CharField(max_length=200, validators=[MinLengthValidator(1)])
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    labels = models.ManyToManyField(Label, related_name='tasks', blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
