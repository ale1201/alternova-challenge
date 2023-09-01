from django.contrib import admin

from movies.models import Movie, UserInteraction

admin.site.register(Movie)
admin.site.register(UserInteraction)