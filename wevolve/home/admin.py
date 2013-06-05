from django.contrib import admin

from wevolve.home.models import Category


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
