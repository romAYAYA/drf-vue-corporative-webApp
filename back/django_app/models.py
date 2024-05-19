from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


class Logs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, null=True)
    ip_address = models.CharField(max_length=40, db_index=True)
    date = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return f"{self.ip_address} {self.date} {self.user}"

    class Meta:
        verbose_name = "Log"
        verbose_name_plural = "Logs"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=250, blank=True, null=True)
    avatar = models.ImageField(
        validators=[FileExtensionValidator(["jpg", "png", "jpeg"])],
        blank=True,
        null=True,
        upload_to="avatars",
    )

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Project(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=255, default="No description provided")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    creation_date = models.DateTimeField(default=timezone.now)
    file = models.FileField(
        upload_to="projects",
        validators=[FileExtensionValidator(["pdf", "doc", "docx", "txt"])],
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class Comment(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="comments"
    )
    message = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.author} on {self.project}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"


class ProjectRating(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="project_ratings"
    )
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="ratings"
    )
    is_liked = models.BooleanField(default=True)

    class Meta:
        unique_together = ("author", "project")
        verbose_name = "Project Rating"
        verbose_name_plural = "Project Ratings"

    def __str__(self):
        return f"Rating by {self.author} on {self.project}"


class CommentRating(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_ratings"
    )
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name="ratings"
    )
    is_liked = models.BooleanField(default=True)

    class Meta:
        unique_together = ("author", "comment")
        verbose_name = "Comment Rating"
        verbose_name_plural = "Comment Ratings"

    def __str__(self):
        return f"Rating by {self.author} on {self.comment}"
