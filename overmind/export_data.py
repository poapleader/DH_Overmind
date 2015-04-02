from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import RequestContext
import datetime
import requests

#Attaempt to Export Interactions

def export_data():

	# api/interactions/
	# 	id, created, updated, last_click, last_url, input_text, cover_text, selected_image, other, time_stamp, kiosk
	interactions = requests.get('https://www.cardisle.com/api/interactions/', auth=('dhenry', 'Bluyacker1')).json()

	print interactions[0];

