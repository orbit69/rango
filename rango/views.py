from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    category_views = Category.objects.order_by('-views')[:5]
    categories_all = Category.objects.all()
    context_dict  = {'categories_likes' : category_list, 'categories_views' : category_views,
                     'categories_all' : categories_all}
    return render(request, 'rango/index.html', context = context_dict)


def about(request):
    # context_dict = {'aboutMessage': "Tablica, z, about, w, views"}
    # return render(request, 'rango/about.html', context = context_dict)
    print(request.method)   #to printuje do konsoli
    print(request.user)
    return render(request, 'rango/about.html', {})


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


def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print (form.errors)

    return render(request, 'rango/add_category.html', {'form' : form})


#dokonczyc zadanie do ksiazki
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form' : form, "category" : category}
    return render(request, 'rango/add_page.html', context_dict)
