# this is a docstring for this AutoSlugField
from autoslug import AutoSlugField
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from django.contrib.auth.admin import UserAdmin
from django.core.validators import MaxLengthValidator, MinValueValidator
from datetime import timedelta as timezone



class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='name')
    details = models.TextField(blank=True)
    image = models.FileField(blank=True,upload_to='categories')
    views = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"




class Option(models.Model):
    name = models.CharField(max_length=250)      
    slug = AutoSlugField(populate_from='name')
    image = models.ImageField(blank=True,upload_to='options')
    details = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=CASCADE)
    votes = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name



class Vote(models.Model):
    option = models.ForeignKey(Option, on_delete=CASCADE)
    voter = models.ForeignKey(User, on_delete=CASCADE)
    slug = AutoSlugField(populate_from='option')

# This was commented before i was able to delete the dummy votes and users i created for testing
# the error was__str__ returned a non string 
    def __str__(self):
        return self.voter
    


class Comment(models.Model):
    category = models.ForeignKey(Category, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.comment




class Contact(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()
    
    def __str__(self):
        return self.name





# # This is supposed to restrict a user from voting 2ice
# class CategoryRequest_Voter(models.Model):
#     voter =models.ForeignKey(User, on_delete=models.CASCADE)
#     published_date = models.DateField(auto_now_add=True, null=True)

#     class Meta:
#         unique_together = ('voter','voted')

#     def publish(self):
#          self.published_date = timezone.now()
#          self.save()



# class User(models.Model):
#     option = models.ForeignKey(Option, on_delete=CASCADE)
#     User = models.ForeignKey(User, unique=True, on_delete=CASCADE)
#     slug = AutoSlugField(populate_from='options')
#     # user = models.ForeignKey(User, on_delete=CASCADE)
#     class Meta:
#         unique_together =('User', 'option')

#     def __str__(self):
#         return self.User