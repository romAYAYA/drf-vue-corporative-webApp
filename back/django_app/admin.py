from django.contrib import admin
from django_app.models import Profile, Project, Comment, ProjectRating, CommentRating

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Comment)
admin.site.register(ProjectRating)
admin.site.register(CommentRating)