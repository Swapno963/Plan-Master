from django.contrib import admin

# 
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' :('name',)}
    list_display = ['name','slug']


admin.site.register(Project, ProjectAdmin)