import logging

from django.shortcuts import render, redirect


logger = logging.getLogger(__name__)

# Create your views here.
def home(request):

    return render(request, 'home.html')