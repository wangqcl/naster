from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from common.models import Users,Compinfo
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import check_password


def index(request):
    return render(request, "web/monweb/message.html")