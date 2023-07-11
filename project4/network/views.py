from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import User, Post, Follow

import json
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    return render(request, "network/index.html", {
        "posts": Post.objects.order_by("-timestamp").all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
@login_required
def new_post(request):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    # Getting user and post data
    user = request.user
    data = json.loads(request.body)
    body = data.get("body", "")

    # Making sure there is content received
    if not body:
        return JsonResponse({"error": "No text provided."}, status=400)

    # Making new post in DB
    try:
        make_post = Post(user=user, body=body)
        make_post.save()
    except:
        return JsonResponse({"error": "Could not save post."}, status=400)

    # redirecting to home page after succesfull post
    return JsonResponse({"message": "Post made succesfully."}, status=201)


def profile(request, user_id):

    try:
        user = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("User not found.")

    posts = Post.objects.order_by("-timestamp").filter(user=user)

    followers = Follow.objects.filter(follow=user).count()

    followage = Follow.objects.filter(user=user).count()

    return render(request, "network/profile.html", {
        "user": user,
        "posts": posts,
        "followers": followers,
        "followage": followage,
    })