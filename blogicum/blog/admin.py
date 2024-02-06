from django.contrib import admin

from .models import Category, Location, Post, Comment


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)


class LocationAdmin(admin.ModelAdmin):
    search_fields = ('name',)


class PostAdmin(admin.ModelAdmin):
    search_fields = ('title',)


class CommentAdmin(admin.ModelAdmin):
    search_fields = ('text',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, PostAdmin)
