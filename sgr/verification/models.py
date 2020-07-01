from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class DBDetail(models.Model):
	username = models.CharField(max_length = 20)
	password = models.CharField(max_length = 20)
	hostname = models.CharField(max_length = 20)
	db_name = models.CharField(max_length = 35)
	db_type = models.CharField(max_length = 15)

	db_types = ( 'MySQL', 'PostgreSQL', 'SQLite3' )  

	def set_password(self, password):
		'''Hashes the parameter password and stores in it hashed form.'''
		self.password = make_password(password)
		
	def verify_password(self, password):
		if check_password(password, self.password):
			return True
		return False



class TableDetail(models.Model):
	name = models.CharField(max_length = 25)
	type = models.CharField(max_length = 25)
	year = models.CharField(max_length = 20, null = True, blank = True)
	branch = models.CharField(max_length = 20, null = True, blank = True)
	year_col_name = models.CharField(max_length = 20, null = True, blank = True)
	branch_col_name = models.CharField(max_length = 20, null = True, blank = True)
	student_id_col_name = models.CharField(max_length = 20)
	name_storage_type = models.CharField(max_length = 35)
	firstname_col_name = models.CharField(max_length = 20, null = True, blank = True)
	lastname_col_name = models.CharField(max_length = 20, null = True, blank = True)
	fullname_col_name = models.CharField(max_length = 20, null = True, blank = True)
	email_col_name = models.CharField(max_length = 20)
	contact_no_col_name = models.CharField(max_length = 20)

	table_types = ( 'All Year data in One Table',
					'Year-Wise Table',
					'Branch-Wise Table' )

	name_storage_types = ( 'Firstname, Lastname in separate column',
				   "Full name in one column of format (Lastname Firstname Middlename)",
				   "Full name in one column of format (Firstname Middlename Lastname)")

	def init(request):
		'''Creates a TableDetail object and initializes it with form data from post method.'''
		table = TableDetail()
		# details related to table
		table.type = request.POST.get('table_type')
		table.name = TableDetail.get_request_data(request, 'table_name')
		if table.type == table.table_types[0]:
			table.branch_col_name = TableDetail.get_request_data(request, 'branch_col_name')
			table.year_col_name = TableDetail.get_request_data(request, 'year_col_name')
		elif table.type == table.table_types[1]:
			table.branch_col_name = TableDetail.get_request_data(request, 'branch_col_name')
		elif table.type == table.table_types[2]:
			table.year_col_name = TableDetail.get_request_data(request, 'year_col_name')
		table.student_id_col_name = TableDetail.get_request_data(request, 'student_id_col_name')
		# student name column
		table.name_storage_type = request.POST.get('name_storage_type')
		if table.name_storage_type == TableDetail.name_storage_types[0]:
			table.firstname_col_name = TableDetail.get_request_data(request, 'firstname_col_name')
			table.lastname_col_name = TableDetail.get_request_data(request, 'lastname_col_name')
		elif ( table.name_storage_type == TableDetail.name_storage_types[1] or
			   table.name_storage_type == TableDetail.name_storage_types[2] ):
			table.fullname_col_name = TableDetail.get_request_data(request, 'fullname_col_name')
			print('hello')
		# other details
		table.email_col_name = TableDetail.get_request_data(request, 'email_col_name')
		table.contact_no_col_name = TableDetail.get_request_data(request, 'contact_no_col_name')
		return table
		
	def is_valid(self):
		''' checks whether all parameters all duly filled before saving the object. '''
		valid = True
		if self.type == '' or self.type == None:
			valid = False
		elif self.name == '' or self.name == None:
			valid = False
		elif ( self.type == self.table_types[0] and
			   ( self.branch_col_name == '' or self.branch_col_name == None or
				 self.year_col_name == '' or self.year_col_name == None ) ):
			valid = False
		elif ( self.type == self.table_types[1] and
			   ( self.branch_col_name == '' or
				 self.branch_col_name == None ) ):
			valid = False
		elif ( self.type == self.table_types[2] and
			   ( self.year_col_name == '' or
				 self.year_col_name == None ) ):
			valid = False
		elif self.student_id_col_name == '' or self.student_id_col_name == None:
			valid = False
		elif self.name_storage_type == '' or self.name_storage_type == None:
			valid = False
		elif ( self.name_storage_type == self.name_storage_types[0] and
			   ( self.firstname_col_name == '' or self.firstname_col_name == None or
				 self.lastname_col_name == '' or self.lastname_col_name == None ) ):
			valid = False
		elif ( ( self.name_storage_type == self.name_storage_types[1] or
				 self.name_storage_type == self.name_storage_types[2] ) and
				 ( self.fullname_col_name == '' or self.fullname_col_name == None ) ):
			valid = False
		elif self.email_col_name == '' or self.email_col_name == None:
			valid = False
		elif self.contact_no_col_name == '' or self.contact_no_col_name == None:
			valid = False
		print(self.name_storage_type, self.fullname_col_name)
		return valid

	def is_empty(self):
		empty = True
		if self.name != '' and self.name != None:
			empty = False
		elif self.type != '' and self.type != None:
			empty = False
		elif self.student_id_col_name != '' and self.student_id_col_name != None:
			empty = False
		elif self.name_storage_type != '' and self.name_storage_type != None:
			empty = False
		elif self.email_col_name != '' and self.email_col_name != None:
			empty = False
		elif self.contact_no_col_name != '' and self.contact_no_col_name != None:
			empty = False
		return empty
		
	def get_request_data(request, input_name):
		''' returns if there is any data in request of a given input name or else returns None.'''
		try:
			for data in request.POST.getlist(input_name):
				if data != '' and data != None:
					return data
			return None
		except AttributeError:
			return request.POST.get(input_name)
