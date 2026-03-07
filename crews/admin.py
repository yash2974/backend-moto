from django.contrib import admin

from crews.models import Crew

# Register your models here.
@admin.register(Crew)
class CrewAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'get_member_count']
    
    def get_member_count(self, obj):
        return obj.members.count()
    get_member_count.short_description = 'Member Count'