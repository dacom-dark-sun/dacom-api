from django.contrib import admin

from community.models import Community


class CommunityAdmin(admin.ModelAdmin):
    readonly_fields = 'api_key',


admin.site.register(Community, CommunityAdmin)
