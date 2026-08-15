from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .forms import LoginForm, RegisterForm
from .serializers import RegisterSerializer


def register_view(request):
    if request.user.is_authenticated:
        return redirect("search:browse")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.profile.phone = form.cleaned_data.get("phone", "")
            user.profile.save(update_fields=["phone", "updated_at"])
            login(request, user)
            messages.success(request, "Welcome! Your account is ready.")
            return redirect("profiles:my-profile")
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", {"form": form})


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = LoginForm

    def get_success_url(self):
        return "/search/"

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
