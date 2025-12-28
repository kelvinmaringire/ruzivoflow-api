from wagtail_modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register
)
from .models import Category, Tag, Post


class CategoryAdmin(ModelAdmin):
    model = Category
    menu_label = "Categories"  # Sub-menu label
    menu_icon = "folder"  # Choose an icon from Wagtail icons
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "slug", "created_at", "updated_at")
    search_fields = ("name", "description")
    list_filter = ("created_at", "updated_at")


class TagAdmin(ModelAdmin):
    model = Tag
    menu_label = "Tags"  # Sub-menu label
    menu_icon = "tag"  # Choose an icon from Wagtail icons
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    list_filter = ("created_at",)


class PostAdmin(ModelAdmin):
    model = Post
    menu_label = "Posts"  # Sub-menu label
    menu_icon = "doc-full"  # Choose an icon from Wagtail icons
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("title", "get_author_full_name", "category", "status", "views", "created_at", "published_at")
    list_filter = ("status", "category", "tags", "created_at", "published_at")
    search_fields = ("title", "content", "excerpt", "author__username", "author__first_name", "author__last_name")
    ordering = ("-created_at",)
    
    def get_author_full_name(self, obj):
        return obj.author.get_full_name() or obj.author.username
    get_author_full_name.short_description = "Author"


# Group all blog models under a single "Blog" menu section
class BlogAdminGroup(ModelAdminGroup):
    menu_label = "Blog"  # Main menu label - isolates blog app
    menu_icon = "edit"  # Main menu icon
    menu_order = 200  # Menu order in sidebar
    items = (PostAdmin, CategoryAdmin, TagAdmin)  # Order: Posts first, then Categories, then Tags


# Register the Blog group (this registers all models under one menu section)
modeladmin_register(BlogAdminGroup)

