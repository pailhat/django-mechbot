from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, JsonResponse
import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Alert
from .forms import AlertForm, AlertFormUpdate
from django.db import connection
from django.conf import settings
from django_hosts.resolvers import reverse

# Create your views here.
DISCORD_SERVER_INVITE = "https://discord.gg/bjUB2FnCE5"

@login_required(login_url="mechbot_docs",)
def index(request: HttpRequest):
    if request.get_host == settings.HOST_URL:
        return redirect("https://" + settings.HOST_URL_MECHBOT + "/")
    print(request.user)
    user = request.user
    title = user.username + "'s " + "Alerts"
    alerts = Alert.objects.filter(user_id=user.id)
    alert_count = alerts.count()
    context = {
        "user": user,
        "authenticated": True,
        "title": title,
        "alerts": alerts,
        "alert_count": alert_count,
        "alert_limit": settings.ALERT_LIMIT
    }
    return render(request, 'mechbot/index.html', context)


@login_required(login_url="mechbot_docs",)
def new_alert(request: HttpRequest):
    if request.get_host == settings.HOST_URL:
        return redirect("https://" + settings.HOST_URL_MECHBOT + "/")
    
    user = request.user
    print(user)

    # Don't allow people to make new alerts if they reach the limit
    alert_count = Alert.objects.filter(user_id=user.id).count()
    if alert_count >= settings.ALERT_LIMIT:
        return redirect("mechbot_main")

    form = AlertForm(label_suffix='')
    title = "New Alert"
    if request.method == "POST":
        form = AlertForm(request.POST)
        form.instance.user_id = user
        if form.is_valid():
            form.save()
            return redirect("mechbot_main")
    context = {"form": form, "title": title, "authenticated": True,}
    return render(request, 'mechbot/alert_form.html', context)


@login_required(login_url="mechbot_docs",)
def update_alert(request, pk):
    if request.get_host == settings.HOST_URL:
        return redirect("https://" + settings.HOST_URL_MECHBOT + "/")

    alert = Alert.objects.get(id=pk)
    print("Compared:")
    print(alert.user_id)
    print(request.user)
    if str(alert.user_id) != str(request.user):
        return redirect("mechbot_main")

    form = AlertFormUpdate(instance=alert,label_suffix='')
    title = "Edit Alert"
    if request.method == 'POST':
        form = AlertFormUpdate(request.POST, instance=alert)
        if form.is_valid():
            form.save()
            return redirect("mechbot_main")
    context = {"form": form,"title": title, "authenticated": True,}
    return render(request, 'mechbot/alert_form.html', context)

@login_required(login_url="mechbot_docs",)
def delete_alert(request, pk):
    if request.get_host == settings.HOST_URL:
        return redirect("https://" + settings.HOST_URL_MECHBOT + "/")

    alert = Alert.objects.get(id=pk)
    print("Compared:")
    print(alert.user_id)
    print(request.user)
    
    if str(alert.user_id) != str(request.user):
        return redirect("mechbot_main")

    title = "Delete Alert"
    if request.method == 'POST':
        alert.delete()
        return redirect("mechbot_main")

    context = {"alert": alert, "title" : title, "authenticated": True,}
    return render(request, 'mechbot/delete_alert.html', context)

def mechbot_docs(request: HttpRequest):
    title = "MechBot Docs"
    user = request.user
    try:
        authenticated = request.user.is_authenticated(request)
    except:
        authenticated = False

    context = {"title" : title, "authenticated": authenticated}
    return render(request, 'mechbot/docs.html', context)

def discord_login(request: HttpRequest):
    return redirect(settings.AUTH_URL_DISCORD)

def discord_login_redirect(request: HttpRequest):
    error = request.GET.get('error')
    if error == "access_denied":
        return redirect("mechbot_docs")
        
    code = request.GET.get('code')
    print(code)
    user = exchange_code(code)
    discord_user = authenticate(request, user=user)
    print(discord_user)
    login(request, discord_user)
    return redirect("mechbot_main")

def exchange_code(code: str):
    data =  {
        "client_id": settings.DISCORD_CLIENT_ID,
        "client_secret": settings.DISCORD_CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.AUTH_REDIRECT_URL,
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
