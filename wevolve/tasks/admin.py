from django.contrib import admin

from wevolve.tasks.models import Task, TaskSkill, TaskUser


class TaskAdmin(admin.ModelAdmin):
    pass


class TaskSkillAdmin(admin.ModelAdmin):
    pass


class TaskUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskSkill, TaskSkillAdmin)
admin.site.register(TaskUser, TaskUserAdmin)
