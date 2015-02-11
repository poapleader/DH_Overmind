import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class Printer(models.Model):
	serial_number = models.CharField(max_length=9) #This is the S/N: As read from the Printer
	printer_type = models.CharField(max_length=6, default='MG7120') #This is the type/model of printer eg. MG8220 or MG7120
	purchase_date = models.DateTimeField('Purchase Date') #This is the Date the Printer's Box was Opened 
	purchase_price = models.DecimalField('Purchase Price', max_digits=5, decimal_places=2) #This is the price paid to obtain the printer
	current_cardstock = models.IntegerField('Cardstock Remaining') #This is the current amount of CardStock in the Bottom Tray of the Printer
	lifetime_prints = models.IntegerField('Total Lifetime Prints', default=0) #This is the total number of prints ever executed by this printer
	
	#Current Ink Levels as Last Measured at the Printers measured in grams (g) this weight includes cartridge weight
	bk_inklevel = models.DecimalField('BK Ink Level', max_digits=4, decimal_places=2)
	gy_inklevel = models.DecimalField('GY Ink Level', max_digits=4, decimal_places=2)
	y_inklevel = models.DecimalField('Y Ink Level', max_digits=4, decimal_places=2)
	pgbk_inklevel = models.DecimalField('PGBK Ink Level', max_digits=4, decimal_places=2)
	c_inklevel = models.DecimalField('C Ink Level', max_digits=4, decimal_places=2)
	m_inklevel = models.DecimalField('M Ink Level', max_digits=4, decimal_places=2)

	#Total Ink Used over life of the Printer measured in grams (g)
	bk_inkused = models.DecimalField('Total BK Ink Used', max_digits=10, decimal_places=2, default=0)
	gy_inkused = models.DecimalField('Total GY Ink Used', max_digits=10, decimal_places=2, default=0)
	y_inkused = models.DecimalField('Total Y Ink Used', max_digits=10, decimal_places=2, default=0)
	pgbk_inkused = models.DecimalField('Total PGBK Ink Used', max_digits=10, decimal_places=2, default=0)
	c_inkused = models.DecimalField('Total C Ink Used', max_digits=10, decimal_places=2, default=0)
	m_inkused = models.DecimalField('Total M Ink Used', max_digits=10, decimal_places=2, default=0)

	def __str__(self):
		return self.serial_number

class Kiosk(models.Model):
	kiosk_name = models.CharField(max_length=50, primary_key=True) #The Unique ID for this Kiosk format: KIOSKXXXX where X is 0001, 0002, etc.
	launch_date = models.DateTimeField('Initial Launch Date') #The Date the Kiosk leaves the manufacturing center
	current_location = models.CharField(max_length=100) #Where the Kiosk is currently being Used
	ACTIVE = 'A' #The Kiosk is currently being used
	IDLE = 'I' #The Kiosk is currently standing Idle
	MAINT = 'M' #The Kiosk is being maintainted [Physically or Remotely]
	DOWN = 'D' #The Kiosk is not currently able to print Cards
	OFFLINE = 'O' #The Kiosk does not have a live data connection, i.e. we do not know its true status and it cannot accept payments
	KIOSK_STATUS_CHOICES = (
		(ACTIVE, 'Active'),
		(IDLE, 'Idle'),
		(MAINT, 'Maint'),
		(DOWN, 'Down'),
		(OFFLINE, 'Offline')
	)
	kiosk_status = models.CharField(max_length=10, choices=KIOSK_STATUS_CHOICES, default=IDLE)
	current_white_envelopes = models.IntegerField('White Envelopes') #Current Level of White Envelopes
	current_brown_envelopes = models.IntegerField('Brown Envelopes') #Current Level of Brown Envelopes	

	#Internal Hardware of the Kiosk
	top_printer = models.OneToOneField(Printer, related_name='Top Printer', primary_key=False) #Printer on the Top Shelf
	bottom_printer = models.OneToOneField(Printer, related_name='Bottom Printer', primary_key=False) #Printer on the Bottom Shelf
	#screen_serialnumber = models.CharField('Screen Serial Number', max_length=25, defualt='NotEntered')
	#computer_serialnumber = models.CharField('Computer Serial Number', max_length=25, defualt='NotEntered')
	
	lifetime_prints = models.IntegerField('Total Lifetime Prints', default=0) #This is the total number of prints ever executed by this kiosk

	def __str__(self):
		return self.kiosk_name