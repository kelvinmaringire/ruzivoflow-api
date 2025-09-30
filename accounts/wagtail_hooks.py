from wagtail_modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from .models import ExtendedUser


class ExtendedUserAdmin(ModelAdmin):
    model = ExtendedUser
    menu_label = "User Profiles"   # Sidebar label
    menu_icon = "user"             # Choose an icon from Wagtail icons
    list_display = ("user", "cell_no", "company_name", "sex", "dob")
    search_fields = ("user__username", "user__first_name", "user__last_name", "company_name")


# Register it with Wagtail
modeladmin_register(ExtendedUserAdmin)
