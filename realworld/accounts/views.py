from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.html import format_html
from django.views.decorators.http import require_http_methods
from django_htmx.http import HttpResponseClientRedirect
from realworld.articles.models import Article
from django.contrib.auth.views import LoginView as BaseLoginView
import json
import requests
import uuid

from .forms import SettingsForm, UserCreationForm

User = get_user_model()


class CustomLoginView(BaseLoginView):
    def form_valid(self, form):
        event_id = str(uuid.uuid4())
        event_data = {
            "event_id": event_id,  
            "username": form.cleaned_data["username"],
        }

        event_json = json.dumps(event_data)
        lambda_url = "https://p2u53l7r11.execute-api.us-east-1.amazonaws.com/default/conduid-loginevent"

        try:
            response = requests.post(lambda_url, data=event_json)

            if response.status_code == 200:
                response_data = response.json()
                message = response_data.get("message", "Success")
                print(message)
            else:
                error_message = response.json().get("error", "Unknown error")
                print(error_message)

        except Exception as e:
            error_message = str(e)
            print(error_message)
        return super().form_valid(form)

@require_http_methods(["GET"])
def profile(request: HttpRequest, user_id: int) -> HttpResponse:

    profile = get_object_or_404(User, pk=user_id)

    articles = (
        Article.objects.select_related("author")
        .filter(author=profile)
        .with_favorites(request.user)
        .prefetch_related("tags")
        .order_by("-created")
    )

    if favorites := "favorites" in request.GET:
        articles = articles.filter(num_favorites__gt=0)

    return TemplateResponse(
        request,
        "accounts/profile.html",
        {
            "profile": profile,
            "articles": articles,
            "favorites": favorites,
            "is_following": profile.followers.filter(pk=request.user.id).exists(),
        },
    )


@require_http_methods(["GET", "POST"])
@login_required
def settings(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        return TemplateResponse(
            request,
            "accounts/settings.html",
            {"form": SettingsForm(instance=request.user)},
        )

    if (form := SettingsForm(request.POST, instance=request.user)).is_valid():
        form.save()
        return HttpResponseClientRedirect(request.user.get_absolute_url())

    return TemplateResponse(request, "accounts/_settings.html", {"form": form})


@require_http_methods(["GET", "POST"])
def register(request: HttpRequest) -> HttpResponse:

    if request.method == "GET":
        return TemplateResponse(
            request, "registration/register.html", {"form": UserCreationForm()}
        )

    if (form := UserCreationForm(request.POST)).is_valid():
        user = form.save()
        auth_login(request, user)

        return HttpResponseClientRedirect(reverse("home"))

    return TemplateResponse(request, "registration/_register.html", {"form": form})


@require_http_methods(["POST", "DELETE"])
@login_required
def follow(request: HttpRequest, user_id: int) -> HttpResponse:

    user = get_object_or_404(User.objects.exclude(pk=request.user.id), pk=user_id)

    is_following: bool

    if request.method == "DELETE":
        user.followers.remove(request.user)
        is_following = False
    else:
        user.followers.add(request.user)
        is_following = True

    return TemplateResponse(
        request,
        "accounts/_follow_action.html",
        {
            "followed": user,
            "is_following": is_following,
            "is_action": True,
        },
    )


@require_http_methods(["GET"])
def check_email(request: HttpRequest) -> HttpResponse:
    if (email := request.GET.get("email")) and User.objects.filter(
        email__iexact=email
    ).exists():
        return HttpResponse(
            format_html(
                """<ul class="error-messages"><li>This email is in use.</li></ul>"""
            )
        )
    return HttpResponse()
