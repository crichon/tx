from django.shortcuts import render
from django.http import HttpResponse
from main.models import Item, Supplier

def index(request):
	return HttpResponse("Commande courrante ?")

def toolbox(request):
	return HttpResponse("Bienvenu dans la toolbox")
# Create your views here.

def importItem(xlsFile):



