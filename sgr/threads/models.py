from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

from user.models import Member

class Thread(models.Model):
	# required data
	title = models.CharField(max_length = 25)
	category = models.CharField( max_length = 25 )
	sub_category = models.CharField( max_length = 25 )
	description = models.TextField()
	complain_count = models.IntegerField( default = 0 )
	note_count = models.IntegerField( default = 0 )
	created_by = models.ForeignKey( Member, on_delete = models.CASCADE )
	created_at = models.DateTimeField( default = timezone.now )
	# for solving
	solver = models.ForeignKey(
		Member, 
		on_delete = models.SET_NULL, 
		null = True, 
		blank = True 
	)
	solver = models.DateField( null = True, blank = True )
	# redressal
	redressed = models.BooleanField( default = False )
	redressal = models.TextField( null = True, blank = True )
	redressal_file = models.FileField( upload_to = 'thread/redressal files/', null = True, blank = True )
	redressed_by = models.ForeignKey(
		Member,
		related_name = '+',
		on_delete = models.CASCADE,
		null = True, 
		blank = True 
	)
	redressed_at = models.DateTimeField( null = True, blank = True )
	# action of accept / reject of redressal by HOD / Principal. 
	action = models.CharField( default = '', max_length = 15 )
	action_msg = models.TextField( null = True )
	action_by = models.ForeignKey( 
		Member, 
		related_name = 'member_on_ thread+',
		on_delete = models.CASCADE, 
		null = True, 
		blank = True 
	)
	action_at = models.DateTimeField( null = True, blank = True )

	def __str__( self ):
		''' return a string of Thread id when object is called for printing purpose. '''
		return str( self.id )
		
	def approve( self, member ):
		''' Approves the redressal and saves changes for approval in Thread object. ''' 
		self.action = 'APPROVE'
		self.action_by = member
		self.action_at = timezone.now()
		self.action_msg = ''
		self.save( update_fields = [
				'action',
				'action_at',
				'action_by',
				'action_msg',
			]
		)
		
	def get_thread( request, id_no ):
		''' Returns Thread with specified id if present or else returns messages and None. '''
		try:
			#id_no = int(  id_no )
			thread = Thread.objects.get( id = id_no )
		except ObjectDoesNotExist:
			messages.error( request, f' Thread { id } does not exist. ' )
			thread = None
		return thread
		
	def increase_complain_count( self ):
		''' Increasea and saves the count of complaint in Thread model. '''
		self.complain_count += 1
		self.save( update_fields=[ 'complain_count' ] )

	def increase_note_count( self ):
		''' Increases and saves the count of note in Thread model. '''
		self.note_count += 1
		self.save( update_fields = [ 'note_count' ] )
		
	def init_for_redressal( self , request, member ):
		''' Initializes the Thread object with the redressal data recieved through post method. '''
		self.redressed = True
		self.redressal = request.POST.get( 'redressal' )
		self.redressal_file = request.FILES.get( 'redressal_file' )
		self.redressed_by = member
		self.redressed_at = timezone.now()
		
	def init_for_reject( self, request, member ):
		''' Initialize the thread object with rejection data received by post method. '''
		self.action = 'REJECT'
		self.action_msg = request.POST.get( 'rejection_msg')
		self.action_at = timezone.now()
		self.action_by = member
		
	def is_redress_valid( self ):
		''' Returns True if initialized redressal data of Thread object is valid or else returns False. '''
		valid = True
		if self.redressal == '' or self.redressal == None:
			valid = False
		if self.redressed_by is None:
			valid = False
		if self.redressed_at is None:
			valid = False
		return valid
		
	def is_reject_valid( self ):
		''' Checks if rejection message if not blank. '''
		if self.action_msg == '' or self.action_msg == None:
			return False
		return True
		
	def redress( self ):
		''' Saves initialized redressal data in Thread model. '''
		self.save( update_fields = [ 
				'redressed',
				'redressal',
				'redressed_by',
				'redressed_at',
			]
		)
		
	def reject( self ):
		''' Rejects redressal and saves the changes accordingly in Thread model. '''
		self.save( update_fields = [
				'action',
				'action_msg',
				'action_by',
				'action_at',
			]
		)
