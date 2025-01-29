from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Hier definierst du die Felder, die in der Liste angezeigt werden
    list_display = ('username', 'email', 'first_name', 'last_name', 'id', 'employee', 'member_since', 'profile_photo', 'files')
    # Hier definierst du die Felder, nach denen gefiltert werden kann
    list_filter = ('is_staff', 'is_superuser', 'employee', 'active_projects', 'files')
    # Hier definierst du die Felder, die im Bearbeitungsformular angezeigt werden
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('employee', 'active_projects', 'description', 'member_since', 'profile_photo', 'files'),
        }),
    )
    # Optional: Hier kannst du die Reihenfolge der Felder im Bearbeitungsformular anpassen
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('employee', 'active_projects', 'description'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
