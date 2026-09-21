import logging

from django.shortcuts import render, redirect


logger = logging.getLogger(__name__)


def home(request):
#simple home page
    return render(request, 'home.html')


def book_room(request):
#check room avaliability in db
    return render(request,'book_room.html')