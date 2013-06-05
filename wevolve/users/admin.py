from django.contrib import admin

from wevolve.users.models import Profile, Skill, UserSkill


class ProfileAdmin(admin.ModelAdmin):
    pass


class SkillAdmin(admin.ModelAdmin):
    pass


class UserSkillAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Skill, SkillAdmin)
admin.site.register(UserSkill, UserSkillAdmin)
