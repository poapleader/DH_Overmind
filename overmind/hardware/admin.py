from django.contrib import admin
from hardware.models import Kiosk, Printer

# Register your models here.
class KioskAdmin(admin.ModelAdmin):
	fieldsets = [
		(None,					{'fields': ['kiosk_name','launch_date', 'current_location', 'kiosk_status']}),
		('Internal Hardware', 	{'fields': ['top_printer','bottom_printer']}),
		('Inventory Levels', 	{'fields': ['current_white_envelopes', 'current_brown_envelopes']}),
	]
admin.site.register(Kiosk, KioskAdmin)
admin.site.register(Printer)
