from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Exists, OuterRef
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from rest_framework import viewsets

from .models import Upload, User
from .serializers import UploadSerializer, UserSerializer

# [TODO]
#  user sign up flow
# rework /api endpoints to better reflect application structure (i.e. /feed | /user | /user/followers)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UploadViewSet(viewsets.ModelViewSet):
    queryset = Upload.objects.all()
    serializer_class = UploadSerializer


@login_required
def index(request):
    #  A flat list of all the usernames our currently logged in user is following
    uploads = (
        Upload.objects.select_related("uploader")
        .prefetch_related("likes")
        .filter(uploader__followers__in=[request.user.pk])
        .annotate(
            total_likes=Count("likes"),
            liked=Exists(request.user.liked.filter(pk=OuterRef("pk"))),
        )
    )
    context = {"uploads": uploads}
    return render(request, "images/index.html", context)


@login_required
def followers_list(request, username):
    user = User.objects.prefetch_related("followers").get(username=username)
    if user.private:
        raise Http404
    context = {"users": user.followers.all()}
    return render(request, "images/user_list.html", context)


@login_required
def following_list(request, username):
    user = User.objects.prefetch_related("following").get(username=username)
    if user.private:
        raise Http404
    context = {"users": user.following.all()}
    return render(request, "images/user_list.html", context)


def user_profile(request, username):
    # Attempt to lookup the user
    user = get_object_or_404(
        User.objects.prefetch_related("followers", "following").annotate(
            num_followers=Count("followers", distinct=True),
            num_following=Count("following", distinct=True),
            num_uploads=Count("uploads", distinct=True),
        ),
        username=username,
    )

    follows_you = False
    following = False

    if request.user.is_authenticated:
        following = user.followers.filter(username=request.user).exists()
        follows_you = user.following.filter(username=request.user).exists()

    context = {
        "user": user,
        "following": following,
        "follows_you": follows_you,
    }
    return render(request, "images/user_profile.html", context)


@login_required
def follow_user(request, username):
    user = get_object_or_404(User, username=username)
    request.user.following.add(user)
    return HttpResponseRedirect(reverse("user_profile", args=(username,)))


@login_required
def unfollow_user(request, username):
    user = get_object_or_404(User, username=username)
    request.user.following.remove(user)
    return HttpResponseRedirect(reverse("user_profile", args=(username,)))


def search(request):
    query = request.GET.get("q")
    context = {}
    if query is not None:
        accounts = User.objects.filter(username__contains=query)
        context["accounts"] = accounts
    return render(request, "images/search_results.html", context)


@login_required
def like_upload(request, pk):
    user = request.user.liked.add(pk)
    return HttpResponseRedirect(reverse("index"))


@login_required
def unlike_upload(request, pk):
    user = request.user.liked.remove(pk)
    return HttpResponseRedirect(reverse("index"))


def save_upload(request):
    ...


def unsave_upload(request):
    ...


class UploadForm(LoginRequiredMixin, CreateView):
    model = Upload
    fields = ["description", "image"]

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)


class UploadDetail(DetailView):
    model = Upload
