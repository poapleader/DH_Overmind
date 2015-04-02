from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
from datetime import datetime, tzinfo, timedelta
from django.utils.timezone import utc, get_default_timezone
import requests
import dateutil.parser
import pytz


from hardware.models import Kiosk, Printer

# Create your views here.
def index(request):
	### Pull All Relevant API Information from 'https://www.cardisle.com/api/ ###

	# api/kiosks/
	#	id, desciptor, details, created, updated, location
	kiosks = requests.get('https://www.cardisle.com/api/kiosks/', auth=('dhenry', 'Bluyacker1')).json()

	# api/printers/
	#	id, created, updated, printer_name, estimated_stock_remaining, low_toner, kiosk
	printers = requests.get('https://www.cardisle.com/api/printers/', auth=('dhenry', 'Bluyacker1')).json()

	# api/statuses/
	#	id, created, updated, low_ink_level, printer_status, card_printed, printer
	statuses = requests.get('https://www.cardisle.com/api/statuses/', auth=('dhenry', 'Bluyacker1')).json()

	# api/pings/
	#	id, created, updated, kiosk
	pings = requests.get('https://www.cardisle.com/api/pings/', auth=('dhenry', 'Bluyacker1')).json()

	# api/interactions/
	# 	id, created, updated, last_click, last_url, input_text, cover_text, selected_image, other, time_stamp, kiosk
	interactions = requests.get('https://www.cardisle.com/api/interactions/', auth=('dhenry', 'Bluyacker1')).json()

	# api/purchases
	#	id, created, updated, card_name, card_inside_text, cc_name, cc_amount, notes, kiosk, card
	purchases = requests.get('https://www.cardisle.com/api/purchases/', auth=('dhenry', 'Bluyacker1')).json()

	#Build Kiosk Output Array
	printers_list = []
	for kiosk in kiosks:
		kiosk_id=kiosk['id']
		for printer in printers:
			if printer['kiosk']==kiosk_id:
				printers_list.append(printer['estimated_stock_remaining'])
		kiosk['printers'] = printers_list
		printers_list = []

	#Format and Save Variables that are going to be used by index.html
	template = get_template('hardware/index.html')
	index_html = template.render(RequestContext(request,
		{
			'kiosks': kiosks,
			'interactions': interactions,
			'statuses': reversed(statuses),
			'last_interaction': interactions[-1],
			'last_printer_status': statuses[-1],
			'total_number_kiosks': len(kiosks),
			'status_length': len(statuses),
			'purchases_length': len(purchases),
		}))

	return HttpResponse(index_html)


def detail(request, kiosk_id):

	# api/interactions/
	# 	id, created, updated, last_click, last_url, input_text, cover_text, selected_image, other, time_stamp, kiosk
	interactions = reversed(requests.get('https://www.cardisle.com/api/interactions/', auth=('dhenry', 'Bluyacker1')).json())

	interaction_list = []
	visit = []
	visit_list = []
	last_interaction_timestamp = datetime.utcnow().replace(tzinfo=utc)
	visit_timegap_def = timedelta(minutes=2)
	#Visit Summary Informational Variables
	visit_dateList = []
	interactionCount = 0
	visit_interactionCount = []
	visit_maxDepth = []
	visit_dictionary = {}
	visit_overmind = []
	time_delta = []

	for interaction in interactions:
		#Convert the Time String from ISO8601 Format to Python Format
		interaction['time_stamp'] = dateutil.parser.parse(interaction['time_stamp'])

		# Strip All Interactions with the right Kiosk ID from the complete list of interactions
		if int(interaction['kiosk'])==int(kiosk_id):
			#Test timegap between this interaction and the previous one
			if last_interaction_timestamp - interaction['time_stamp'] < visit_timegap_def:
				#Create a Visit or List of Interactions
				visit.append(interaction)
				#Store Time Delta between interactions
				time_delta.append(last_interaction_timestamp - interaction['time_stamp'])
				#Increment Interaction Counter
				interactionCount += 1
				#Reset the Last Interaction Timestamp
				last_interaction_timestamp = interaction['time_stamp']
			else:
				#Save Information from last interaction
				visit_dictionary['visit_date']=interaction['time_stamp']
				visit_dictionary['interactions_count']=interactionCount
				visit_dictionary['interactions_list']=visit
				visit_dictionary['time_delta']=time_delta
				visit_list.append(visit_dictionary)
				#Reset Variables
				interactionCount = 0
				visit = []
				visit_dictionary = {}
				# Use this interaction to start a new Visit
				visit.append(interaction)
				#Reset the Last Interaction Timestamp
				last_interaction_timestamp = interaction['time_stamp']

#			interaction_list.append(interaction)

		else:
			print 'No Match'

	print'Visit List Length'
	print len(visit_list)

	print'Visit Dictionary Length'
	print len(visit_dictionary)
	#print visit_dictionary[0]

	template = get_template('hardware/interactions.html')
	detail_html = template.render(RequestContext(request,
		{
#			'interaction_list': interaction_list,
#			'interactions': interactions,
#			'visit_dictionary': visit_dictionary,
			'kiosk_id': kiosk_id,
			'visit_list': visit_list,
		}))

	return HttpResponse(detail_html)

	#Convert Last Interaction Time String into Datetime Object
	#last_interaction = interactions[-1]
	#year = last_interaction.time[0:4]
	#month = last_interaction.time[5:7]
	#day = last_interaction[8:10]
	#hour = last_interaction[11:13]
	#minute = last_interaction[14:16]
	#second = last_interaction[17:19]
	#microsecond = last_interaction[20:25]
	#test_time = datetime.datetime[year,month,day[,hour[,minute[,second[microsecond]]]]
