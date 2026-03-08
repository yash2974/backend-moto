from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from crews.models import Crew
from .models import Profile

# Inline for user profile
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name = "Profile"
    verbose_name_plural = "Profile"
    fields = ['image_url']

# Inline for crews owned by user
class CrewOwnerInline(admin.TabularInline):
    model = Crew
    fk_name = 'owner'
    extra = 0
    fields = ['name', 'type', 'is_private']
    readonly_fields = ['name', 'type', 'is_private']
    can_delete = False
    show_change_link = True
    verbose_name = "Crew (Owner)"
    verbose_name_plural = "Crews Owned"

# Inline for crews where user is a member
class CrewMemberInline(admin.TabularInline):
    model = Crew.members.through
    fk_name = 'user'
    extra = 0
    readonly_fields = ['crew']
    can_delete = False
    verbose_name = "Crew Membership"
    verbose_name_plural = "Crew Memberships"
    
    def crew(self, obj):
        return obj.crew
    crew.short_description = 'Crew Name'

# Extend the default UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline, CrewOwnerInline, CrewMemberInline]
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
