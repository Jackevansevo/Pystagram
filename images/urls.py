from django.urls import include, path
from rest_framework import routers

from . import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"photos", views.UploadViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("follow/<str:username>", views.follow_user, name="follow_user"),
    path("user/unfollow/<str:username>", views.unfollow_user, name="unfollow_user"),
    path("upload", views.UploadForm.as_view(), name="upload"),
    path("upload/<int:pk>", views.UploadDetail.as_view(), name="upload_detail"),
    path("like/<int:pk>", views.like_upload, name="like"),
    path("unlike/<int:pk>", views.unlike_upload, name="unlike"),
    path("search", views.search, name="search"),
    path("api", include(router.urls)),
    path("<str:username>", views.user_profile, name="user_profile"),
    path("<str:username>/followers", views.followers_list, name="user_followers"),
    path("<str:username>/following", views.following_list, name="user_following"),
]
