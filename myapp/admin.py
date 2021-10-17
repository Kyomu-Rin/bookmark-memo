from django.contrib  import admin
from .models         import Post, Tag, Like, Contact, Opinion

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('site_url', 'memo', 'author', )
    list_display_links = ('site_url', )
    ordering = ('-created_at', )

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name', )
    ordering = ('-created_at', )


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'tag')
    list_display_links = ('tag', )



@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'mail', 'context', )
    list_display_links = ('name', )
    ordering = ('-created_at', )



@admin.register(Opinion)
class OpinionAdmin(admin.ModelAdmin):
    list_display = ('name', 'mail', 'user', 'context', )
    list_display_links = ('name', )
    ordering = ('-created_at', )