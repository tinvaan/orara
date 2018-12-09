from django.contrib import admin

from flocks.models import OraraConnections, UserBookmarks


class OraraConnectionsAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'approved')


class UserBookmarksAdmin(admin.ModelAdmin):
    list_display = ('user', 'bookmark')


admin.site.register(OraraConnections, OraraConnectionsAdmin)
admin.site.register(UserBookmarks, UserBookmarksAdmin)
