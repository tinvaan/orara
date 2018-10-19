from django.contrib import admin

from profiles.models import OraraUser, UserInterests, SocialProfiles


admin.site.site_header = "Orara | Dashboard"


class OraraUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'area', 'status', 'email')


class UserInterestsAdmin(admin.ModelAdmin):
    list_display = ('user', 'interests')


class SocialProfilesAdmin(admin.ModelAdmin):
    list_display = ('user', 'blog', 'twitter', 'linkedin', 'facebook',
                    'instagram', 'portfolio')


admin.site.register(OraraUser, OraraUserAdmin)
admin.site.register(UserInterests, UserInterestsAdmin)
admin.site.register(SocialProfiles, SocialProfilesAdmin)