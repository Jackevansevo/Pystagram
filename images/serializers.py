from rest_framework import serializers

from images.models import Upload, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "followers", "following", "uploads"]


class UploadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Upload
        fields = "__all__"
