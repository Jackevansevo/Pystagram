from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import reverse


class Upload(models.Model):
    """Represents an individual photo"""

    created_on = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=800, blank=True, null=True)
    image = models.ImageField()
    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uploads",
    )

    def get_absolute_url(self):
        return reverse("upload_detail", args=(self.pk,))

    def __str__(self):
        return self.image.url


class User(AbstractUser):
    """
    Subclass the AbstractUser django builtin, enables us to extent the user to
    enable followers
    """

    private = models.BooleanField(default=False)
    description = models.TextField(max_length=800, blank=True, null=True)
    avatar = models.ImageField()

    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", blank=True
    )
    liked = models.ManyToManyField("Upload", related_name="likes", blank=True)
    saved = models.ManyToManyField("Upload", related_name="saves", blank=True)

    def get_absolute_url(self):
        return reverse("user_profile", args=(self.username,))

    def __str__(self):
        return self.username
