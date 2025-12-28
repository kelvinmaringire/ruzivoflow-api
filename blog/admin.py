from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_author_full_name', 'category', 'status', 'views', 'created_at', 'published_at']
    list_filter = ['status', 'category', 'tags', 'created_at']
    search_fields = ['title', 'content', 'excerpt', 'author__username', 'author__first_name', 'author__last_name']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['views', 'created_at', 'updated_at', 'published_at']
    
    def get_author_full_name(self, obj):
        return obj.author.get_full_name() or obj.author.username
    get_author_full_name.short_description = 'Author'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('Content', {
            'fields': ('featured_image', 'excerpt', 'content')
        }),
        ('Status & Metadata', {
            'fields': ('status', 'views', 'created_at', 'updated_at', 'published_at')
        }),
    )
