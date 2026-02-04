from django.shortcuts import render
from .models import CardCoctail

""" 
 CardCoctail( name=, category=, type=, ingredients=, description=, glass=, strength=, image=, badge= )
"""
def main(request):
    return render(request, "main.html")

def IBA(request):
    return render(request, "IBA.html")

def coctail(request):
    return render(request, "coctail.html")

def contacts(request):
    return render(request, "contacts.html")

def list_coctails(request):
    return render(request, "list_coctail.html")

def admin(request):
    return render(request, "admin.html")