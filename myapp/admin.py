from django.contrib import admin
from .models import Post, Tag

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('site_url', 'memo', 'author', )
    list_display_links = ('site_url', )
    ordering = ('-created_at', )


admin.site.register(Tag)

