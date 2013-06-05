from django.contrib import admin

from wevolve.projects.models import Project, ProjectPart, UserProject


class ProjectAdmin(admin.ModelAdmin):
    pass


class ProjectPartAdmin(admin.ModelAdmin):
    pass


class UserProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'project', 'permission')
    date_hierarchy = 'created'
    list_filter = ['created', 'permission']
    search_fields = ['user__first_name']


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectPart, ProjectPartAdmin)
admin.site.register(UserProject, UserProjectAdmin)
