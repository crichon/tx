from django.contrib.auth.models import User, Group
from django.shortcuts import render
from django.http import HttpResponse

from main.models import Item, Supplier, Category
from  xlrd import open_workbook


def index(request):
	return HttpResponse("Soon available")

def toolbox(request):
	#TODO: get downloaded in toolbox
	importItem('./listeProduits.xlsx')
	return HttpResponse("Initialisation terminee")

def importItem(file_path):

	#Ouverture du fichier
	rb = open_workbook(file_path)
	r_sheet = rb.sheet_by_index(0)

	for row_index in range (1, r_sheet.nrows):
		#Hydratation or get Supplier Model
		item_supplier= r_sheet.cell(row_index, 4).value
		item_supplier, created = Supplier.objects.get_or_create(name=item_supplier)

		#Hydratation or get Category Model
		current_category =  r_sheet.cell(row_index, 0).value
		item_category, created = Category.objects.get_or_create(name=current_category)

		#Hydratation Item
		item_name = r_sheet.cell(row_index, 1).value
		item_ref = current_supplier= r_sheet.cell(row_index, 3).value
		item, created = Item.objects.get_or_create(ref=item_ref, name=item_name, category=item_category, supplier=item_supplier)


