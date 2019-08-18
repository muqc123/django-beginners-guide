from django.shortcuts import render,HttpResponse

# Create your views here.

from .models import Board


def home(request):
	boards = Board.objects.all()
	return render(request, 'home.html', {'boards': boards})