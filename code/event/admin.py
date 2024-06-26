from django.contrib import admin
from .models import Event, Ticket, Saved, ImageGallery

class EventAdmin(admin.ModelAdmin):
    pass

class TicketInline(admin.TabularInline):
    pass

class SavedInline(admin.TabularInline):
    pass
class ImageGalleryInline(admin.TabularInline):
    pass


admin.site.register(Event, EventAdmin)
admin.site.register(Ticket)
admin.site.register(Saved)
admin.site.register(ImageGallery)