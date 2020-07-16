from django.db import models
from django.utils import timezone
from django.db.models import Q

from datetime import date, datetime
import os

from user.models import Student, Member
from threads.models import Category, SubCategory, Thread
from sgr.settings import BASE_DIR
from user.views import get_object

class Complain(models.Model):

	### CONSTANTS
	categories = (
		('A','Administrative Office'),
		('I', 'Infrastructure'),
		('C', 'Committee/Teacher'),
		('M', 'Management activites'),
		('O', 'Other' )
	)
	sub_categories = ( 
		( ( 'A', 'Admission' ), ( 'C', 'Concession' ), ( 'S', 'Scholarship/Freeship' ), ( 'O', 'Other' ) ),
		( ( 'C', 'Canteen' ), ( 'A', 'Classroom' ), ( 'G', 'Gymnasium' ), ( 'L', 'Library' ),
		  ( 'I', 'Lift' ), ( 'P', 'Parking' ), ( 'Y', 'Playground' ),
		  ( 'R', 'Practical Lab' ), ( 'T', 'Toilets/Washrooms' ), ( 'W', 'Workshop' ),
		  ( 'X', 'Xerox Office' ), ( 'O', 'Other' ) ),
		( ( 'B', 'Branch Committees' ), ( 'E', 'E-Cell' ), ( 'N', 'NSS' ), ( 'W', 'Women Development' ),
		  ( 'O', 'Other' ) ),
		( ( 'A', 'Attendance' ), ( 'C', 'Cleanliness' ), ( 'T', 'Timetable' ),
		  ( 'O', 'Other' ) ),
		( ( 'O', 'Other' ), )
	)

	id = models.CharField(max_length = 12, primary_key = True)
	subject = models.CharField(max_length = 35)
	category = models.CharField(max_length = 30)
	sub_category = models.CharField(max_length = 30)
	brief = models.TextField()
	file = models.FileField(upload_to = 'complain/', blank = True, null = True)
	complainer = models.ForeignKey(Student, on_delete = models.CASCADE)
	reg_datetime = models.DateTimeField( default = timezone.now )
	last_edit_at = models.DateTimeField( null = True, blank = True )
	sorted = models.BooleanField(default = False)
	sorted_by = models.ForeignKey( 
		Member,
		related_name = "sorted_by_member+",
		on_delete = models.SET_NULL,
		null = True,
		blank = True
	)
	sorted_at = models.DateTimeField( null = True, blank = True )
	solver = models.ForeignKey(
		Member,
		related_name = 'solving_member+',
		on_delete = models.SET_NULL,
		null = True,
		blank = True
	)
	solving_date = models.DateField( null = True, blank = True )
	# rejection of complain by sorter
	action = models.CharField( max_length = 10, default = '' )		# actions - ACCEPTED / REJECTED 
	action_msg = models.TextField( null = True, blank = True )
	actioned_at = models.DateTimeField( null = True, blank = True )
	actioned_by = models.ForeignKey(
		Member,
		related_name = 'action_taken_by+',
		on_delete = models.SET_NULL,
		null = True,
		blank = True
	)
	# thread
	thread = models.ForeignKey( Thread, on_delete = models.CASCADE, null = True, blank = True )
	threaded_by = models.ForeignKey(Member, on_delete = models.CASCADE, null = True, blank = True )
	threaded_at = models.DateTimeField(null = True, blank = True)
	# pinned 
	pinned_in_thread = models.BooleanField(default = False)
	pinned_by = models.ForeignKey( 
		Member,
		related_name = 'complain_pinned_by_member+',
		on_delete = models.SET_NULL,
		null = True,
		blank = True
	)
	pinned_at = models.DateTimeField( null = True, blank = True )
	
	def __str__( self ):
		return self.id
	
	def accept( self, member ):
		''' Make changes in Complain object and saves it. '''
		self.action = 'ACCEPTED'
		self.action_msg = ''
		self.actioned_at = datetime.now()
		self.actioned_by = member
		self.save( update_fields = [
				'action',
				'action_msg',
				'actioned_at',
				'actioned_by',
			]
		)

	def generate_id(self, category, sub_category):
		''' Generates and initialize id for object when called. '''
		categories = Category.get_code_name_list()
		sub_categories = SubCategory.get_code_name_list()
		today = date.today()
		curr_date = today.strftime('%y%m%d')
		# opening file in reading mode
		count_file = open(os.path.join(BASE_DIR, 'count_files/complain_id.txt'), 'r')
		# preprocessing of data - splitting a single string into list of lines
		count_data = count_file.read().split('\n')
		# opening file in writing mode
		count_file = open(os.path.join(BASE_DIR, 'count_files/complain_id.txt'), 'w')
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
		while len(generated_id) < 4:
			generated_id = '0' + generated_id
		generated_id = curr_date + code + generated_id
		print(generated_id, 'id  id')
		self.id = generated_id
		

	def init( request ):
		''' Initializes Complain object with data received by post method. '''
		complain = Complain()
		complain.subject = request.POST.get('subject')
		complain.category = request.POST.get('category')
		complain.sub_category = request.POST.get('sub_category')
		complain.brief = request.POST.get('brief')
		complain.complainer = Student.objects.get(user = request.user)
		complain.file = request.FILES.get('file')
		return complain
		
	
	def init_for_edit( self, request ):
		''' Initializes saved Complain object with edited data received by post method. '''
		self.subject = request.POST.get('subject')
		self.category = request.POST.get('category')
		self.sub_category = request.POST.get('sub_category')
		self.brief = request.POST.get('brief')
		self.action = ''
		self.last_edit_at = datetime.now()
		self.file = request.FILES.get('file')
		
	def init_for_reject( self, request, member ):
		''' Initializes saved Complain object for rejection. '''
		self.action = 'REJECTED'
		self.action_msg = request.POST.get( 'rejection_msg' )
		self.actioned_at = datetime.now()
		self.actioned_by = member 
		
	def init_for_thread( self, request, member, thread ):
		''' Initializes the Complain object with thread. '''
		self.thread = thread
		self.threaded_at = datetime.now()
		self.threaded_by = member
		if self.action != 'REJECTED' :
			self.action = 'ACCEPTED'
			self.action_msg = ''
			self.actioned_at = datetime.now()
			self.actioned_by = member
		print( request.POST.get( str( thread ) ), 'thread it pin_it' )
		if request.POST.get( str(thread) ) == "True":
			print( 'entered' )
			self.pinned_in_thread = True
			self.pinned_at = datetime.now()
			self.pinned_by = member
	
	def is_valid(self):
		valid = True
		if self.subject == '' or self.subject == None:
			valid = False
		elif self.category == '' or self.category == None or self.category == 'Select Category':
			valid = False
		elif self.sub_category == '' or self.sub_category == None or self.sub_category == 'Select Sub Category':
			valid = False
		elif self.brief == '' or self.brief == None or self.brief == 'Add your complain in brief here...':
			valid = False
		elif self.complainer == None:
			valid = False
		print(valid, 'is_valid')
		if valid:
			self.generate_id(self.category, self.sub_category)
		return valid
		
		
	def is_edit_valid(self):
		valid = True
		if self.subject == '' or self.subject == None:
			valid = False
		elif self.category == '' or self.category == None or self.category == 'Select Category':
			valid = False
		elif self.sub_category == '' or self.sub_category == None or self.sub_category == 'Select Sub Category':
			valid = False
		elif self.brief == '' or self.brief == None or self.brief == 'Add your complain in brief here...':
			valid = False
		elif self.complainer == None:
			valid = False
		return valid
		
	def is_reject_valid( self ) :
		''' Checks if rejection message is not null. '''
		if self.action_msg == '' or self.action_msg == None or self.action_msg == 'Add your message for rejection here...' :
			return False
		return True

	def get_complain( request, id_no ):
		''' Returns Complain object if present or else adds message and returns None. '''
		try:
			complain = Complain.objects.get( id = id_no )
		except ObjectDoesNotExist:
			messages.error( f'No Complaint exist with ID { id_no }. ')
			complain = None
		return complain


	### Searching methods

	def get_filename(self):
		return self.file.name[ 9 : ]
		
	def save_edit( self ):
		''' Saves content added in Complain object during editing. '''
		self.save( update_fields = [
				'subject',
				'category',
				'sub_category',
				'brief',
				'last_edit_at',
				'action',
			]
		)
		
	def save_reject( self ):
		''' Saves changes made for rejection of Complain object. '''
		self.save( update_fields = [
				'action',
				'action_msg',
				'actioned_at',
				'actioned_by',
			]
		)

	def search_id(query):
		return Q(id__icontains = query)

	def search_subject(query):
		return Q(subject__icontains = query)

	def search_category(query):
		return Q(category__icontains = query)

	def search_sub_category(query):
		return Q(sub_category__icontains = query)

	def search_brief(query):
		return Q(brief__icontains = query)
		
	def thread_it( self ):
		''' Saves the initialized Conplain object with Thread object. '''
		self.save( update_fields = [
				'thread',
				'threaded_at',
				'threaded_by',
				'action',
				'action_msg',
				'actioned_by',
				'actioned_at',
				'pinned_in_thread',
				'pinned_at',
				'pinned_by'
			]
		)



class Note(models.Model):
	note = models.TextField()
	file = models.FileField(upload_to = 'note/', blank = True, null = True)
	complain = models.ForeignKey(Complain, on_delete = models.SET_NULL, null = True, blank = True )
	reg_datetime = models.DateTimeField(default = timezone.now)
	thread = models.ForeignKey( Thread, on_delete = models.SET_NULL, null = True, blank = True )
	pinned = models.BooleanField(default = False)
	pinned_by = models.ForeignKey(
		Member,
		related_name = 'by_member in thread/complain+',
		on_delete = models.SET_NULL,
		null = True,
		blank = True
	)
	pinned_at = models.DateTimeField( null = True, blank = True )
	solver = models.ForeignKey(Member, on_delete = models.CASCADE)
	
	def __str__( self ):
		return str( self.id )

	def init_all(self, request):
		self.note = request.POST.get('note')
		self.file = request.FILES.get('file')
		id = request.POST.get('complain_id')
		if id != None and id != '':
			self.complain = Complain.objects.get(id = id)
		self.solver = Member.objects.get(user = request.user)
		
	def is_none( self ):
		''' Checks Note object if data is None, then returns True or else returns False. '''
		is_none = True
		if self.note is not None:
			 is_none = False
		if self.complain is not None or self.thread is not None:
			is_none = False
		if self.solver is not None:
			is_none = False
		return is_none

	def is_valid(self):
		''' Checks Note object is data valid or not, before saving. '''
		valid = True
		if self.note == '' or self.note == None:
			valid = False
		if self.solver == '' or self.solver == None:
			valid = False
		if self.thread is None or self.thread == '' or self.complain is None and self.complain == '':
			valid = False
		return valid
		
	def get_note( request, id ):
		''' Returns Note of id_no if present or else returns None and a error message. '''
		try:
			note = Note.objects.get( id = id )
		except ObjectDoesNotExist:
			messages.error( request, f'No Note with id { id_no }. ' )
			note = None
		return note
		
		
	def get_filename( self ):
		return self.file.name[ 5 : ]
		
	def init_for_thread( request, thread ):
		''' Initialize the Note as required for the Thread. '''
		note = Note()
		note.note = request.POST.get( 'note' )
		note.file = request.FILES.get( 'file' )
		note.solver = get_object( request )
		note.thread =  thread
		if request.POST.get( 'pin_it' ) =='Yes' and note.solver:
			note.pinned = True
			note.pinned_by = note.solver
			note.pinned_at = timezone.now()
		return note
		
	def pin( self, member ):
		''' Makes changes in model of Note for pinning. '''
		self.pinned = True
		self.pinned_by = member
		self.pinned_at = timezone.now()
		self.save( update_fields = [
				'pinned',
				'pinned_by',
				'pinned_at',
			]
		)
		
	def unpin( self ):
		''' Makes chnages in model of Note for unpinning. '''
		self.pinned = False
		self.pinned_by = None
		self.pinned_at = None
		self.save( update_fields = [
				'pinned',
				'pinned_at',
				'pinned_by',
			]
		)
