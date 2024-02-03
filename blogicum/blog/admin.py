from django.contrib import admin

from .models import Category, Location, Post


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)


class LocationAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    search_fields = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
