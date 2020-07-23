from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Q
from django.utils import timezone

from datetime import date
import os

from sgr.settings import BASE_DIR
from user.models import Member


class Category( models.Model ) :
	code = models.CharField( primary_key = True, max_length = 1 )
	name = models.CharField( max_length = 25 )
	
	def get_category( request, category ) :
		''' Returns Category Object of specified category string. '''
		try :
			category_obj = Category.objects.get( name = category )
		except ObjectDoesNotExist :
			messages.error( request, f' No such Category exists. ' )
			return None
		else :
			return category_obj
			
	def get_code_name_list() :
		''' Returns a List of code, name of all Category objects. '''
		cat_obj = Category.objects.all()
		category_list = [ [ obj.code, obj.name ] for obj in cat_obj ]
		return category_list
		

	def get_list():
		''' Returns a List of all Category name. '''
		category_qs = Category.objects.all()
		category_list = [ category.name for category in category_qs ]
		return category_list
	
class SubCategory( models.Model ) :
	''' Model Class for storing different categories of Complain and Thread Model '''
	code = models.CharField( max_length = 1 )
	name = models.CharField( max_length = 25 )
	category = models.ForeignKey( Category, on_delete = models.CASCADE )
	
	def get_code_name_list() :
		''' Returns a List of [ code, name ] of Sub Category object nested according to category. '''
		final_list = list()
		for cat_obj in Category.objects.all() :
			sub_cat_obj = SubCategory.objects.filter( category = cat_obj )
			sub_list = [ [ sub_category.code, sub_category.name ] for sub_category in sub_cat_obj ]
			final_list.append( sub_list )
		return final_list
	
	def get_list( request, category ):
		''' Returns a List of Subcategories based on passed category string. '''
		category_obj = Category.get_category( request, category )
		if category_obj is not None :
			print( category_obj.name )
			sub_cat_obj = SubCategory.objects.filter( category = category_obj )
			sub_cat_list = [ sub_category.name for sub_category in sub_cat_obj ]
			print( sub_cat_list )
			return sub_cat_list

class Thread(models.Model):
	# required data
	id = models.CharField( primary_key = True, max_length = 15 )
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
	action = models.CharField( default = '', max_length = 15 )		# actions - APPROVE / REJECT
	action_msg = models.TextField( null = True )
	action_by = models.ForeignKey( 
		Member, 
		related_name = 'member_on_ thread+',
		on_delete = models.CASCADE, 
		null = True, 
		blank = True 
	)
	action_at = models.DateTimeField( null = True, blank = True )
	
	# constants
	
	search_types = (
		'All',
		'Title',
		'Description',
		'Created by',
		
	)
	
	

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
		
	def generate_id(self, category, sub_category):
		''' Generates and initialize id for object when called. '''
		categories = Category.get_code_name_list()
		sub_categories = SubCategory.get_code_name_list()
		today = date.today()
		curr_date = today.strftime('%y%m%d')
		# opening file in reading mode
		count_file = open(os.path.join(BASE_DIR, 'count_files/thread_id.txt'), 'r')
		# preprocessing of data - splitting a single string into list of lines
		count_data = count_file.read().split('\n')
		# opening file in writing mode
		count_file = open(os.path.join(BASE_DIR, 'count_files/thread_id.txt'), 'w')
		# if first line of date does not match with current date
		if curr_date != count_data[0]:
			print( 1 )
			data = ''
			category_index = 0
			for category_wise in sub_categories:
				for sub_code, sub_cat in category_wise:
					if sub_cat == sub_category:
						data+='1 '
						code = categories[ category_index ][ 0 ] + sub_code
					else:
						data+='0 '
				data+='\n'
				category_index += 1
			data = curr_date+ '\n' + data
			count_file.write(data)
			count_file.close()
			generated_id = '0'
		else:
			print( 2 )
			# preprocessing of data / conversion into list of counts from string
			for index in range(len(count_data)):
				count_data[index] = count_data[index].split(' ')
			# writes date in first line of the opened count file
			count_file.write(curr_date+'\n')
			print( count_data, 'count_data' )
			# count incrementing part
			cat_index = 1
			for cat_code, cat in categories:
				sub_index = 0
				for sub_cat_code, sub in sub_categories[cat_index-1]:
					if (sub == sub_category and cat == category):
						print(sub, cat)
						try:
							generated_id = count_data[cat_index][sub_index]
						except IndexError:
							count_data[cat_index][sub_index] = '1'
							generated_id = '0'
						else:
							count_data[cat_index][sub_index] = str( int(generated_id) + 1 )
						# generates code from category, sub_category, required for id 
						code = cat_code + sub_cat_code
					# writes count for every sub_category in file
					count_file.write(count_data[cat_index][sub_index]+' ')
					sub_index += 1
				#creates new line in count file before start iterating for next category
				count_file.write('\n')
				cat_index += 1
			count_file.close()
		if int( generated_id ) < 10 :
			generated_id = curr_date + code + generated_id
			print(generated_id, 'id  id')
			self.id = generated_id
		
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
		
	def init_for_add( request, member ):
		''' Initializes new Thread object with data received by post method. '''
		thread = Thread()
		thread.title = request.POST.get( 'title' )
		thread.category = request.POST.get( 'category' )
		thread.sub_category = request.POST.get( 'sub_category' )
		thread.description = request.POST.get( 'description' )
		thread.created_by = member
		return thread
		
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
		
	def is_add_valid( self, request ):
		''' Validates data initialized by method 'init_for_all' before saving in DB. '''
		valid = True
		if self.title == '' or self.title == None:
			valid = False
		elif self.category == '' or self.category == None or self.category == 'Select Category':
			valid = False
		elif self.sub_category == '' or self.sub_category == None or self.sub_category == 'Select Sub Category':
			valid = False
		elif self.description == '' or self.description == None or self.description == 'Add description here...':
			valid = False
		elif self.created_by == None:
			 valid = False
		if valid == True : 
			self.generate_id( self.category, self.sub_category )
		return valid
		
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
		
	def search( query, search_type ):
		''' Single function for search of Thread objects. '''
		search_qs = Thread.objects.none()
		if search_type == search_types[0] or search_type == search_types[1] :
			search_qs.union( Q( title__icontains = query ) )
		elif search_type == search_types[0] or search_type == search_types[2] :
			search_qs.union( Q( description__icontains = query ) )
		elif search_type == search_types[0] or search_type == search_types[3] :
			search_qs.union( (	Q( created_by__mid__icontains = query ) | 
					Q( created_by__user__first_name__icontains = query ) | 
					Q( created_by__user__last_name__icontains = query )
				)
			)
		return search_qs
