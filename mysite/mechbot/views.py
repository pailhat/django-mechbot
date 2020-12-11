from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Alert
from .forms import AlertForm, AlertFormUpdate
from django.db import connection
from django.conf import settings

# Create your views here.
DISCORD_SERVER_INVITE = "https://discord.gg/bjUB2FnCE5"
BASE_URL = "https://" + settings.MECHBOT_URL + "/"
auth_url_discord = settings.AUTH_URL_DISCORD


@login_required(login_url="/mechbot/oauth2/login",)
def index(request: HttpRequest):
    print(request.user)
    user = request.user
    alerts = Alert.objects.filter(user_id=user.id)

    context = {
        "user": user,
        "alerts": alerts
    }
    return render(request, 'mechbot/index.html', context)


@login_required(login_url="/mechbot/oauth2/login",)
def new_alert(request: HttpRequest):
    user = request.user
    print(user)
    form = AlertForm()
    title = "Add New MechMarket Alert"
    if request.method == "POST":
        form = AlertForm(request.POST)
        form.instance.user_id = user
        if form.is_valid():
            form.save()
            return redirect("/mechbot")
    context = {"form": form, "title": title}
    return render(request, 'mechbot/alert_form.html', context)


@login_required(login_url="/mechbot/oauth2/login",)
def update_alert(request, pk):
    alert = Alert.objects.get(id=pk)
    print("Compared:")
    print(alert.user_id)
    print(request.user)
    if str(alert.user_id) != str(request.user):
        return redirect("/mechbot")

    form = AlertFormUpdate(instance=alert)
    title = "Edit MechMarket Alert"
    if request.method == 'POST':
        form = AlertFormUpdate(request.POST, instance=alert)
        if form.is_valid():
            form.save()
            return redirect("/mechbot")
    context = {"form": form,"title": title}
    return render(request, 'mechbot/alert_form.html', context)

@login_required(login_url="/mechbot/oauth2/login",)
def delete_alert(request, pk):
    alert = Alert.objects.get(id=pk)
    print("Compared:")
    print(alert.user_id)
    print(request.user)
    
    if str(alert.user_id) != str(request.user):
        return redirect("/mechbot")

    title = "Delete MechMarket Alert"
    if request.method == 'POST':
        alert.delete()
        return redirect("/mechbot")

    context = {"alert": alert, "title" : title}
    return render(request, 'mechbot/delete_alert.html', context)

def discord_login(request: HttpRequest):
    return redirect(auth_url_discord)

def discord_login_redirect(request: HttpRequest):
    code = request.GET.get('code')
    print(code)
    user = exchange_code(code)
    discord_user = authenticate(request, user=user)
    print(discord_user)
    login(request, discord_user)
    return redirect("/mechbot")

def exchange_code(code: str):
    data =  {
        "client_id": settings.DISCORD_CLIENT_ID,
        "client_secret": settings.DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": BASE_URL + "mechbot/oauth2/login/redirect",
        "scope": "identify"
    }
    headers = {
        "content_type": "application/x-www-form-urlencoded"
    }
    response = requests.post("https://discord.com/api/oauth2/token", data=data, headers=headers)
    print(response)
    credentials = response.json()
    access_token = credentials['access_token']
    response = requests.get("https://discord.com/api/v6/users/@me", headers={
        "Authorization": "Bearer %s" % access_token
    })
    print(response)
    user = response.json()
    print(user)
    return user

def discord_server_redirect(request: HttpRequest):
    return redirect(DISCORD_SERVER_INVITE)
