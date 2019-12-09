# django
from django.contrib.admin import ModelAdmin, site

# models
from .models import Vote, VoteCount

site.register(Vote)
site.register(VoteCount)