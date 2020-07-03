from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

from user.models import Member, Student
from .models import TableDetail, DBDetail

def add_table(request):
	if request.user.is_staff:
		try:
			member = Member.objects.get(user = request.user)
		except ObjectDoesNotExist:
			context = { 'err_msg' :
						'No such Member exist.\n Please log in with valid account. If problem continues report it.' }
			return render(request, 'error.html', context)
		if member.role == 'DB Admin':
			context = { 'table_types' : TableDetail.table_types,
						'years' : Student.years,
						'branches' : Student.branches,
						'name_storage_types' : TableDetail.name_storage_types
						}
			table = TableDetail.init(request)
			if table.is_valid():
				table.save()
				context.update( { 'message' :
							'Table details added. Please checkout in table column' } )
			elif table.is_empty():
				return render(request, 'verification/add_table.html', context)
			else:
				context.update( { 'message' :
								  'Please fill out full form then Submit it.' } )
			return render(request, 'verification/add_table.html', context)
	return render(request, 'pemission_denied.html')


def db_details(request) :
	if request.user.is_staff:
		try:
			member = Member.objects.get(user = request.user)
		except ObjectDoesNotExist:
			context = { 'err_msg' : 'No such Member exist'}
			return render(request, 'error.html', context)
			
		print(member.role=='DB Admin')
		if member.role == 'DB Admin':
			context = { 'db_types' : DBDetail.db_types }
			if (request.method =='POST') :
				username=request.POST['USERNAME']
				password1=request.POST['pass']
				password2=request.POST['conpass']
				dbname=request.POST['DBName']
				hostname1=request.POST['HOSTNAME']
				dbtype=request.POST['DBtype']

				if password1==password2 :
					db=DBDetail.objects.create(username=username,hostname=hostname1,db_name=dbname,db_type=dbtype)
					db.set_password(password1)
					db.save();
					
					messages.info(request,'DBdetails Saved Succesfully')
					return render (request,'verification/dbdetails.html', context)
			  
				   
				else :
					messages.info(request,'Passwords not matched ')
					return render (request,'verification/dbdetails.html', context)
						
			return  render (request,'verification/dbdetails.html',context)
			
	return render( request, 'permission_denied.html')
