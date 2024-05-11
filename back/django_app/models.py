from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django_app.utils import Model
from django.utils import timezone


class Logs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True, null=True)
    ip_address = models.CharField(max_length=40, db_index=True)
    date = models.DateTimeField(default=timezone.now, db_index=True)

    def __str__(self):
        return f"{self.ip_address} {self.date} {self.user}"


class Profile(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=250, blank=True)
    avatar = models.ImageField(
        validators=[FileExtensionValidator(["jpg", "png", "jpeg"])],
        blank=True,
        null=True,
        upload_to="avatars",
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
