from django.contrib import admin

from crews.models import Crew, Request

# Register your models here.
@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'get_member_count']
    
    def get_member_count(self, obj):
        return obj.members.count()
    get_member_count.short_description = 'Member Count'

@admin.register(Request)
class RequestsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'crew', 'status']
    list_filter = ['status']
    search_fields = ['user__username', 'crew__name']