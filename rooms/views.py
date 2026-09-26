import logging

from django.shortcuts import render, redirect
from django.views.decorators.http import require_safe


logger = logging.getLogger(__name__)

@require_safe
def home(request):
#simple home page
    return render(request, 'home.html')


def book_room(request):
#check room avaliability in db
    return render(request,'book_room.html')