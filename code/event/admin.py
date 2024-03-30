from django.contrib import admin
from .models import Event, Ticket

class EventAdmin(admin.ModelAdmin):
    pass

class TicketInline(admin.TabularInline):
    pass


admin.site.register(Event, EventAdmin)
admin.site.register(Ticket)