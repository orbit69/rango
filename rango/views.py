from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from rango.forms import UserForm, UserProfileForm


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


def register(request):
    #ustawiam flage na false, zmienei na true gdy rejestracja cie powiedzie
    registered = False

    if request.method == 'POST':
        #dodaje do moich form
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        #jesli obydwie formy sa poprawne (tzn. user dobrze wpisze dane)
        if user_form.is_valid() and profile_form.is_valid():
            #dodaje do bazy
            user = user_form.save()
            #haszuje haslo i dodaje do bazy
            user.set_password(user.password)
            user.save()

            #commit true bo sam zdecyduje kiedy dodac do bazy
            profile = profile_form.save(commit=False)
            profile.user = user

            #dodaje zdjecie?
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  {'user_form' : user_form,
                   'profile_form' : profile_form,
                   'registered' : registered})

