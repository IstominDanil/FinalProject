from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name


class Advertisement(models.Model):
    headline = models.CharField(max_length=128)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('final_detail', args=[self.pk])

    def __str__(self):
        return self.headline


class Reply(models.Model):
    text = models.CharField(max_length=170)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    adv = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # class Meta:
    #     ordering = ('-created_at',)