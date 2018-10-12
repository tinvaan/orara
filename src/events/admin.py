from django.contrib import admin

from events.models import OraraEvent, EventCustomers


class OraraEventAdmin(admin.ModelAdmin):
    list_display = ('name', 'venue', 'venue_area', 'website', 'tags_list')

    def get_queryset(self, request):
        return super(OraraEventAdmin, self).get_queryset(request).prefetch_related('tags')

    def tags_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


class EventCustomersAdmin(admin.ModelAdmin):
    list_display = ('event', 'customer')


admin.site.register(OraraEvent, OraraEventAdmin)
admin.site.register(EventCustomers, EventCustomersAdmin)