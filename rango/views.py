from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category
from rango.models import Page


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    category_views = Category.objects.order_by('-views')[:5]
    context_dict  = {'categories_likes' : category_list, 'categories_views' : category_views}
    return render(request, 'rango/index.html', context = context_dict)

def about(request):
    context_dict = {'aboutMessage': "Tablica, z, about, w, views"}
    return render(request, 'rango/about.html', context = context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug) #category_name_slug
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context_dict)
