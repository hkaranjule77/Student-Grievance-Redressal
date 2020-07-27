from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .models import Complain, Note
from threads.models import Category, SubCategory, Thread
from user.models import Student, Member
from user.views import get_object

from datetime import date

# Create your views here.
def list(request) :
	if request.user.is_authenticated:
		obj = get_object( request )			# Member / Student object
		if obj is not None :
			if request.user.is_staff:
				if obj.role == 'Solver' :
					complain_list = Complain.objects.filter( action_by_sorter = 'ACCEPTED' )
				elif obj.role == 'Sorter' :
					complain_list = Complain.objects.filter( action_by_sorter = '' )
				else :
					complain_list = Complain.objects.all()
			else :
				complain_list = Complain.objects.filter( complainer = obj )
			messages.info( request, f' Complain count : { len(complain_list) }' )
			context = { 
				'complain_list' : complain_list, 
				'search_options' : Complain.search_options,
				'filter_options' : Complain.filter_options
			}
			return render(request, 'complain/list.html', context)
	return render( request, 'permission_denied.html' )
    
def accept( request, id_no ):
	''' Accepts Complain object for solving. '''
	if request.user.is_staff:
		member = get_object( request )
		complain = Complain.get_complain( request, id_no )
		if member is not None and complain is not None:
			if complain.action_by_sorter == '' or complain.action_by_sorter == 'REJECTED' :
				complain.accept( member )
				messages.success( request, f' Complain { complain } is ACCEPTED for solving. ' )
			else:
				messages.info( request, f' Complain { complain } is already Accepted. ' )
			return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )
	return render( request, 'permission_denied.html' )

def add(request):
	if request.user.is_authenticated:
		if request.user.is_staff:
			messages.info( 'Members are not allowed to add complaint.' )
			return render( request, 'permission-denied.html' )
		student = get_object( request )
		if student is not None:
			print( Category.get_list() )
			today_date = date.today()
			context = { 'categories' : Category.get_list() }
			if student.count_date != today_date:
				student.reinitialize_count()
			if student.complain_count < 5:
				if request.method == "POST":
					complain = Complain.init( request )
					if complain.category != 'Select Category' :
						context.update( { 
								'sub_categories' : SubCategory.get_list( request, complain.category ),
								'complain' : complain
							}
						)
					if complain.is_valid():
						print( complain.id, complain.category, complain.sub_category )
						complain.save()
						student.increase_count()							# Increases Complain count
						messages.success( request,  'Complaint registered. Track it on dashboard . ' )
						messages.info( request, f' You can register { str( 5 - student.complain_count ) } more complaints')
						return redirect( f'/complain/{ complain }' ) 
					else:
						context.update( { 'complain' : complain } )
						if complain.sub_category != 'Select Sub Category' :
							messages.error( request, ' Please fill full form, before submitting it. ' )
						else :
							messages.info( request, ' Please select Sub Category for Complain. ' )
			else:
				messages.info( request, 'Complaint registration limit reached for today. You have used all your 5 registrations. ')
				return render( request, 'permission_denied.html')
			return render(request, 'complain/add.html', context)
	return redirect('/permission-denied.html/')
	
def approve_redressal( request, id_no ) :
	''' Approves redressal of a complain '''
	if request.user.is_staff :
		member = get_object( request )
		complain = Complain.get_complain( request, id_no )
		if member is not None and complain is not None :
			if complain.redressal and complain.redressal.action != 'Approve' :
				complain.redressal.approve( member )
				messages.success( request, f" Redressal of Complaint { complain } is accepted successfully. " )
			else :
				messages.info( request, f" Redressal of Complaint { complian } is already redressed. ")
			return redirect( f'/complain/{ complain }/' )
	return render( request, 'permission_denied.html' )
	
def detail_for_solve( request, member, complain ):
	''' Extensive functions of complain details for solving of Complain object. '''
	curr_date = date.today()
	if complain.solving_date != curr_date:
		context = { 'complain' : complain, 'select_button' : True}
		return render(request, 'complain/solve_detail.html', context)
	notes = Note.objects.filter(complain = complain)
	context = {'complain' : complain, 'select_button' : False, 'notes' : notes }
	return render( request, 'complain/solve_detail.html', context )
        
def detail_for_sort( request, member, complain ) :
	''' Extended funcion of complain details for sorting of Complain object.  '''
	thread_list = Thread.objects.filter( category = complain.category, sub_category = complain.sub_category )
	context = { 'complain': complain, 'thread_list' : thread_list }
	return render( request, 'complain/sort_detail.html', context )

def detail(request, id_no):
	complain = Complain.get_complain( request, id_no )
	obj = get_object( request )
	if request.user.is_staff :
		if obj.role != 'Sorter' :
			page = detail_for_solve( request, obj, complain )
			print( 1 )
		else:
			page = detail_for_sort( request, obj, complain )
			print( 3 )
		return page
	elif request.user.is_authenticated:
		if complain.complainer == obj:
			context = { 'complain' : complain }
			return render( request, 'complain/stu_detail.html', context )
		else:
			messages.info( request, 'This complain is registered by other student, it cannot be accessed.' )
	return redirect( '/permission-denied/' )
		
def edit( request, id_no ):
	''' Grants edit access to complainer(student) id complain is rejected. '''
	if request.user.is_authenticated:
		student = get_object( request )
		complain = Complain.get_complain( request, id_no )
		if student is not None and complain is not None:
			if student == complain.complainer:
				if complain.action_by_sorter == 'REJECTED':
					context = { 
						'complain' : complain,
						'categories' : Complain.categories,
						'sub_categories' : Complain.sub_categories
					}
					if request.method == "POST":
						complain.init_for_edit( request )
						if complain.is_edit_valid():
							complain.save_edit()
							messages.success( request, f'Complain { complain } edit successfully saved and sent for approval. ' )
							return redirect( f'/complain/{ complain }/' )
						else:
							messages.error( request, f'Please fill out all required columns of form then submit it, ')
					return render( request, 'complain/edit.html', context )
				else:
					messages.info( request, 'You can only edit complain only if it is rejected by committee. ' )
			else:
				messages.info( f"You don't have edit access to required Complain { complain }. " )
			return redirect( f'/complain/{ complain }/' )
	return render( request, 'permission_denied.html' )

def select(request, id_no):
	if request.user.is_staff:
		#add code for checking for date
		complain = Complain.get_complain( request, id_no )
		if complain is not None :
			if complain.redressal is None or not complain.redressal.action == 'APPROVE' :
				curr_date = date.today()
				if complain.solving_date != curr_date :
					solver = Member.objects.get(user = request.user)
					complain.solver = solver
					complain.solving_date = curr_date
					complain.save(update_fields = ['solver', 'solving_date'])
					messages.success( request, f" Complaint { id_no } is  selected for solving." )
				else :
					if complain.solver.user == request.user:
						return redirect(f'/complain/{complain.id}/')
					messages.info( request, f" Complaint { id_no } is already selected by other member for solving. " )
			else :
				messages.info( request, f" Complaint { id_no } is approved. Now, it can't be solved. " )
			return redirect( f'/complain/{ complain.id }/' )
	return redirect('/permission-denied/')
        
        
def deselect(request, id_no):
    if request.user.is_staff:
        try:
            complain = Complain.objects.get(id = id_no)
        except ObjectDoesNotExist:
            context = { 'err_msg' : "No such Complain exist." }
            return render(request, 'error.html', context)
        if complain.redressal is None or not complain.redressal.action == 'APPROVE':
            curr_date = date.today()
            if complain.solver != None and complain.solver.user == request.user:
                if complain.solving_date == curr_date:
                    complain.solving_date = None
                    complain.solver = None
                    complain.save(update_fields = ['solver', 'solving_date'])
                    messages.success( request, f' Complaint { complain } is deselected for solving. ' )
                else:
                    messages.info( request, f" Complaint { complain } is not selected by no one. " )
                select_button = True
            else:
                messages.info( request, f" Complaint { complain } is selected by different user, you can't deselect it." )
                if complain.solver and complain.solving_date == curr_date:
                    select_button = False
                else:
                    select_button = True
        else:
            select_button = False
            messages.info( request, f"Complaint { complain } is already approved. Now, it can't be solved. " )
        context = { 'complain' : complain, 'select_button' : select_button }
        return redirect( f'/complain/{ complain.id }/' )
    return redirect('/permisssion-denied/')
    
def pin_complain( request, id_no ):
	''' Pins complainr in top of other complaints in thread in which it is added. '''
	if request.user.is_staff:
		complain = Complain.get_complain( request, id_no )
		if complain is not None:
			if not complain.pinned_in_thread:
				complain.pinned_in_thread = True
				complain.save( update_fields = [ 'pinned_in_thread' ] )
				messages.success( request, f' Complaint { complain.id } is pinned in thread { complain.thread }. ' )
			else:
				messages.info( request, f' Complaint { complain.id } is already pinned in thread { complain.thread }. ' )
		return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )
	return render( request, 'permission_denied.html' )

def redress( request, id_no ) :
	''' Adds Redress to complaint. '''
	if request.user.is_staff :
		member = get_object( request )
		print( 'reached')
		complain = Complain.get_complain( request, id_no )
		if member is not None :
			if complain is not None :
				if complain.redressal is None or not complain.redressal.action == 'APPROVE' :
					complain.init_for_redressal( request, member )
					if complain.is_redress_valid() :
						complain.save_redress()
						print( complain.redressal )
						messages.success( request, f" Complaint { complain } is Redressed successfully. " )
					else :
						messages.error( request, " Please type redressal in given section before submitting it. ")
						context = { 'complain' : complain, 'member' : member, 'redressal' : complain.redressal }
						return render( request, 'complain/solve_detail.html', context )
				else :
					messages.error( request, f" Complaint { complain } is already redressed. " )
				return redirect( f'/complain/{ complain }/' )
			else :
				messages.error( request, f" There was problem in fetching details of Complaint { id_no }. ")
		else :
			messages.error( request, f" There is problem in fetching your access details. " )
	return render( request, 'permission_denied.html' )
	
	
def reject( request, id_no ):
	''' Rejects Complain object and sents for editing to student( complainer ). '''
	if request.user.is_staff:
		member = get_object( request )
		complain = Complain.get_complain( request, id_no )
		if member is not None and complain is not None:
			if complain.action_by_sorter != 'REJECTED' :
				if request.method == "POST" :
					complain.init_for_reject( request, member )
					if complain.is_reject_valid():
						complain.save_reject()
						messages.success( request, f'Complaint { complain } is REJECTED and sent back to student for editing. ')
					else:
						messages.error( request, ' Please fill a message for rejection of a complaint. ' )
			else :
				messages.info( request, f' Complaint { complain } is ALREADY REJECTED. ' )
			return redirect( f'/complain/{ complain }/' )
	return render( request, 'permission_denied.html' )
	
def reject_redressal( request, id_no ) :
	''' Rejects the redressal of Complain object. '''
	if request.user.is_staff :
		member = get_object( request )
		complain = Complain.get_complain( request, id_no )
		if member is not None and complain is not None :
			if complain.redressal and complain.redressal != 'Reject' :
				complain.redressal.init_for_reject( request, member )
				if complain.redressal.is_reject_valid() :
					complain.redressal.reject()
					messages.success( request, f" Redressal of Complaint { complain } is rejected. ")
				else :
					messages.error( request, " Please fill rejecion reason before submitting form. " )
					notes = Note.get_list( complain = complain )
					complain = Complain.get_complain( request, complain.id )
					reject = True					# parameter for showing rejection form
					context = { 'complain' : complain, 'member' : member, 'reject' : reject, 'notes' : notes }
					return render( request, 'complain/solve_detail.html', context )
			else :
				messages.info( request, f" Redressal of Complaint { complain } is rejected already. ")
			return redirect( f'/complain/{ complain }/' )
	return render( request, 'permission_denied.html' )
	
def unpin_complain( request, id_no ):
	''' Unpins the complaint in the thread in which it is added. '''
	if request.user.is_staff:
		complain = Complain.get_complain( request, id_no )
		if complain is not None:
			if complain.pinned_in_thread:
				complain.pinned_in_thread = False
				complain.save( update_fields = [ 'pinned_in_thread' ] )
				messages.success( request, f' Complain { complain.id } is unpinned in thread { complain.thread }. ')
			else:
				messages.info( request, f' Complain { complain.id } is already unpinned in thread { complain.thread }. ')
		return HttpResponseRedirect( request.META.get('HTTP_REFERER'))
	return render( request, 'permission_denied.html' )
            
def search(request):
	if request.user.is_staff:
		query = request.POST.get('query')
		opt = request.POST.get('opt')
		filter_input = request.POST.get( 'filter' )
		if query == None:
			query = ""
		if query == "" :
			queryset = Complain.objects.all()
		else:
			queryset = Complain.objects.none()
			if opt == Complain.search_options[0] or opt == Complain.search_options[1]:
				q1 = Complain.search_id(query = query)
				q1 = Complain.objects.filter(q1)
				queryset = queryset.union(q1)
			if opt == Complain.search_options[0] or opt == Complain.search_options[2]:
				q2 = Complain.search_subject(query = query)
				q2 = Complain.objects.filter(q2)
				queryset = queryset.union(q2)
			if opt == Complain.search_options[0] or opt == Complain.search_options[3]:
				q3 = Complain.search_category(query = query)
				q3 = Complain.objects.filter(q3)
				queryset = queryset.union(q3)
			if opt == Complain.search_options[0] or opt == Complain.search_options[4]:
				q4 = Complain.search_sub_category(query = query)
				q4 = Complain.objects.filter(q4)
				queryset = queryset.union(q4)
			if opt == Complain.search_options[0] or opt == Complain.search_options[5]:
				q5 = Complain.search_brief(query = query)
				q5 = Complain.objects.filter(q5)
				queryset = queryset.union(q5)
		queryset.distinct()
		# Filtering section
		if filter_input == Complain.filter_options[1] :
			queryset = queryset.filter( action_by_sorter = '' )
			print(1)
		elif filter_input == Complain.filter_options[2] :
			queryset = queryset.filter( action_by_sorter = 'ACCEPTED' )
			print(2)
		elif filter_input == Complain.filter_options[3] :
			queryset = queryset.exclude( thread = None )
			print(3)
		elif filter_input == Complain.filter_options[4] :
			queryset = queryset.exclude( thread = None )
			print(4)
		elif filter_input == Complain.filter_options[5] :
			queryset = queryset.exclude( redressal = None )
			print(5)
		elif filter_input == Complain.filter_options[6] :
			queryset = queryset.filter( redressal__action = 'APPROVE' )
			print(6)
		messages.info( request, f' search count : {len(queryset)}' )
		context = { 
			'complain_list' : queryset,
			'query' : query,
			'search_by' : opt,
			'filter_option' : filter_input,
			'search_options' : Complain.search_options,
			'filter_options' : Complain.filter_options 
		}
		return render(request, 'complain/list.html', context)
	return redirect('/permission-denied/')



   ### NOTES ###

def add_note(request, id_no):
	if request.user.is_staff:                                      # checking if user if member
		complain = Complain.get_complain( request, id_no )
		member = get_object( request )
		if member is not None and complain is not None :
			if member != complain.solver :                # verifying if user is solver
				messages.info( request, 
					f' Complaint { id_no } is already selected by other member. So, note cannot be added.'
				)
				return render(request, 'permission_denied.html', context)
			else:
				note = Note()
				note.init_all( request, member, complain )
				if note.is_valid():
					note.save()
					messages.success( request, f' Note { note.id } is added in Complaint.{ id_no }. ' )
				else:
					messages.error( request, ' Please type your note before adding it. ' )
					context = { 'note' : note, 'complain' : complain, 'member' : member }
					return render( request, 'complain/solve_detail.html', context )
		return redirect( f'/complain/{ complain.id }/' )
	return redirect('/permission-denied/')
    
def pin_note( request, id_no ):
	''' Pins Note in the Complain / Thread. '''
	if request.user.is_staff:
		note = Note.get_note( request, id_no )
		member = get_object( request )
		if note is not None:
			if not note.pinned == True:
				note.pin( member )
				if note.thread:
					messages.success( request, f'Note { note } id is pinned in Thread { note.thread }. ')
				else:
					messages.success( request, f'Note {note } is pinned in Complain { note.complain }. ')
			else:
				if note.thread:
					messages.info( request, f'Note { note } is already pinned. ')
				else:
					messaged.info( request, f'Note {note } is already pinned in Complain { note.complain }. ' )
		return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )
	return render( request, 'permission_denied.html' )
		
def unpin_note( request, id_no ):
	''' Unpins the note from thread / complain. '''
	if request.user.is_staff:
		note = Note.get_note( request, id_no )
		if note is not None:
			if note.pinned:
				note.unpin()
				if note.thread:
					messages.success( request, f' Note { note } is unpinned in Thread { note.thread }. ' )
				else:
					messages.success( request, f' Note { note } is unpinned in Complain { note.complain }. ' )
			else:
				messages.info( request, f' Note { note } is unpinned already. ')
		return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )
	return render( request, 'permission_denied.html' )
