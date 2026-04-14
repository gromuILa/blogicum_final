from django.contrib import admin

from .models import Post, Category, Location, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'pub_date', 'author',
        'category', 'location', 'is_published'
    )
    list_filter = ('is_published', 'category', 'location', 'pub_date')
    search_fields = ('title', 'text')
    list_editable = ('is_published',)
    empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('title', 'description')
    list_editable = ('is_published',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published')
    list_filter = ('is_published',)
    search_fields = ('name',)
    list_editable = ('is_published',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'author__username')


admin.site.site_header = 'Блогикум админ'
admin.site.index_title = 'Панель администратора'

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Comment, CommentAdmin)
