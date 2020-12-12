from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest

from django.conf import settings

# I have nothing else so for now just take people to mechbot
def site_index(request: HttpRequest):
    return redirect("https://" + settings.HOST_URL_MECHBOT)