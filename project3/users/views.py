from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

#need to authenticate Users
from django.contrib.auth.models import User
from .models import UserForm

# Create your views here.

def index(request):
  if not request.user.is_authenticated:
      form = UserForm()
      return render(request, "users/login.html", {"message": None, "form":form})
  context = {
      "user": request.user
  }
  return render(request, "users/user.html", context)

def login_view(request):
  username = request.POST["username"]
  password = request.POST["password"]
  #new_username = request.POST["new_username"]
  #password = request.POST["password"]
  #print(request.POST)
  user = authenticate(request, username=username, password=password)
  if user is not None:
      login(request, user)
      return HttpResponseRedirect(reverse("index"))
  else:
      form = UserForm()
      return render(request, "users/login.html", {"message": "Invalid credentials.", "form":form})

def create_user(request):
    """
    Try to add a new user to the user model
    """
    try:
        form = UserForm(request.POST)
        new_user = form.save()
        new_form = UserForm()
        return render(request, "users/login.html", {"message": "You can log in now!", "form":new_form})
    except ValueError:
        form = UserForm()
        return render(request, "users/login.html", {"message": "Invalid Uservalues", "form":form})







def logout_view(request):
  logout(request)
  form = UserForm()
  return render(request, "users/login.html", {"message": "Logged out.", "form": form})
