from django.shortcuts import render
from django.http import HttpResponse

from hardware.models import Kiosk, Printer

# Create your views here.
def index(request):
	kiosk_location_list = Kiosk.objects.order_by('kiosk_name')
	number_launched_kiosks = Kiosk.objects.filter().count()
	number_active_kiosks = Kiosk.objects.filter(kiosk_status="Active")
	number_idle_kiosks = Kiosk.objects.filter(kiosk_status="I")
	context = {'kiosk_location_list': kiosk_location_list}
	return render(request, 'hardware/index.html', context)