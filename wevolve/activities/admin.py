from django.contrib import admin

from wevolve.activities.models import Activity


class ActivityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Activity, ActivityAdmin)
