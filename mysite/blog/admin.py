"""register post .."""
from django.contrib import admin
from .models import Post, Comment

# admin.site.register(Post)
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Customizing  the way models are  displayed.."""

    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    prepopulated_fields = {'slug': ('title',)}  # AUTO MATICALLY FIELD SLUGE USEING TITILE
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Custmizig the admin view.."""

    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


