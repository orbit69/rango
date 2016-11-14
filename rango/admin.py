from django.contrib import admin
from rango.models import Category, Page

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,           {'fields' : ['views', 'likes']}),
        ('Sam zmienilem',{'fields' : ['name']}),
    ]
    list_display = ('name', 'views', 'likes')

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'views')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
