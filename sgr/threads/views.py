from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages

from datetime import date

from .models import Category, Redressal, SubCategory, Thread
from complain.models import Complain, Note
from user.views import get_object


# Create your views here.

def add_thread( request ):
	'''Handles requests for adding new Thread. '''
	if request.user.is_staff:
		member = get_object( request )
		if member is not None:
			context = { 'categories' : Category.get_list() }
			print( Category.get_list() )
			print( Category.get_code_name_list() )
			print( SubCategory.get_code_name_list() )
			if request.method == 'POST':
				thread = Thread.init_for_add( request, member )
				if thread.category != 'Select Category' :
					context.update( { 
							'thread' : thread,
							'sub_categories' : SubCategory.get_list( request, thread.category )
						}
					)
				if thread.is_add_valid( request ):
					if thread.id != '' :
						thread.save()
						messages.success( request, f'Thread { thread.id } is added. ')
						return redirect( f'/thread/{ thread.id }/')
					else :
						messages.error( request, ' Thread Creation Limit reached for this subcatgory. ')
				else:
					if thread.sub_category != 'Select Sub Category' :
						messages.error( request, ' Please fill form before submitting it. ' )
					else :
						messages.info( request, ' Please select Sub Category. ' )
					context.update( { 'thread' : thread } )
			return render( request, 'threads/add.html', context )
	return render( request, 'permission_denied.html' )

def add_note( request, id_no ):
	''' Adds note in specified Thread. '''
	if request.user.is_staff:
		thread = Thread.get_thread( request, id_no )
		context = { 'id_no' : id_no }
		print( thread, id_no )
		if thread is not None:
			note = Note.init_for_thread( request, thread )
			print( note.note)
			if note.is_valid():
				note.save()
				thread.increase_note_count()
				messages.success( request, f'New Note { note } is added in thread { note.thread }. ' )
				return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )
			elif note.is_none():
				pass
			else:
				messages.info( request, 'Please fill out full form and then submit it. ' )
		else:
			messages.error( request, f' Thread { id_no } does not exist. ' )
		return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )
	messages.error( request, ' Only Committee Member can add Note in Thread')
	return render( request, 'permission_denied.html')
		
def add_redressal( request, id_no ):
	''' Adds redressal to the thread. '''
	if request.user.is_staff:
		thread = Thread.get_thread( request, id_no )
		member = get_object( request )
		if thread is not None and  member is not None:
			if thread.redressal is None or thread.redressal.action != 'APPROVE':
				if request.method == 'POST' :
					thread.init_for_redressal( request, member )
					if thread.is_redress_valid():
						thread.redress()
						messages.success( request, f' Thread { thread } is redressed successfully. ' )
					else:
						messages.info( request, ' Please fill out full form first, before submitting it. ')
			else:
				messages.info( request, ' Thread is already redressed. ')
		else:
			messages.error( request, f' Thread { id_no } does not exist. ' )
		return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )
	return render( request, 'permission_denied.html' )
	
def approve_redressal( request, id_no ):
	''' Function for approval in redressal of Thread. '''
	if request.user.is_staff:
		member = get_object( request )
		thread = Thread.get_thread( request, id_no )
		if member is not None and thread is not None:
			if thread.redressal.action == '' or thread.redressal.action == 'REJECT':
				thread.redressal.approve( member )
				messages.success( request, f' Redressal of Thread { id_no } is approved. ')
			else:
				messages.info( request, f' Redressal of Thread { id_no } is already approved. ' )
		return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )
	return render( request, 'permission_thread.html' )
	
def attach_complain( request, id_no, complain_id ):
	''' Attaches Complain of same category and sub_category to thread. '''
	if request.user.is_staff :
		thread = Thread.get_thread( request, id_no )
		complain = Complain.get_complain( request, complain_id )
		member = get_object( request )
		if thread is not None and complain is not None and member is not None :
			if member.role == 'Sorter' :
				if complain.thread == None:
					if thread.category == complain.category :
						if thread.sub_category == complain.sub_category :
							complain.init_for_thread( request, member, thread )
							complain.thread_it()
							thread.increase_complain_count()
							messages.success( request, f' Complain { complain } is attached to Thread { thread }. ' )
						else :
							messages.error( request, f" Sub category doesn't match for Complaint { complain } and Thread { thread }. " )
					else :
						messages.error( request, f" Category doesn't match for Complaint { complain } and Thread { thread }. " )
				else :
					messages.error( request, f" Complaint { complain } id already attached to Thread { complain.thread }. " )
			else :
				messages.info( request, f" You don't have access to attach Complaint to a Thread. " )
			return redirect( f'/complain/{ complain_id }/' )
	return render( request, 'permission_denied.html' )	

def detail(request, id_no):
	if request.user.is_staff:
		thread = Thread.get_thread(  request, id_no )
		member = get_object( request )
		pinned_complain_list = Complain.objects.filter( thread = thread, pinned_in_thread = True )
		unpinned_complain_list = Complain.objects.filter( thread = thread, pinned_in_thread = False)
		pinned_note_list = Note.objects.filter( thread = thread, pinned = True )
		unpinned_note_list = Note.objects.filter( thread = thread, pinned = False)
		curr_date = date.today()
		context = { 
			'thread' : thread,
			'member' : member,
			'pinned_complain_list' : pinned_complain_list,
			'unpinned_complain_list' : unpinned_complain_list,
			'pinned_note_list' : pinned_note_list,
			'unpinned_note_list' : unpinned_note_list,
			'curr_date' : curr_date
		}
		return render( request, 'threads/detail.html', context )
	return render( request, 'permission_denied.html' )
	
def list( request ):
	''' Lists all Thread and render it on a page. '''
	if request.user.is_staff:
		thread_list = Thread.objects.all()
		context = {
			'thread_list' : thread_list,
			'search_types' : Thread.SEARCH_TYPES,
			'filter_options' : Thread.FILTER_OPTIONS
		}
		return render( request, 'threads/list.html', context )
	return render( request, 'permission_denied.html' )
	
def load_categories( request ) :
	''' Loads all categories into DB in_case of first_boot or update the Categories. '''
	Category.load_data()
	return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )
	
def load_subcategories( request ) :
	''' Loads all subcategories in to DB in case of first boot or update the SubCategories. '''
	SubCategory.load_data()
	return redirect( '/' )
	
	
def reject_redressal( request, id_no ):
	if request.user.is_staff:
		thread = Thread.get_thread( request, id_no )
		member = get_object( request )
		if member is not None and thread is not None:
			if thread.redressal.action == '' or thread.redressal.action == 'APPROVE':
				thread.redressal.init_for_reject( request, member )
				if thread.redressal.is_reject_valid():
					thread.redressal.reject()
					messages.success( request, f' Redressal of Thread { thread } is rejected. ')
				else:
					messages.info( 'Please fill rejection message first then submit it. ')
			else:
				messages.info( request, f' Redressal of Thread { id_no } is already rejected. ')
		return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )
	return render( request, 'permission_detnied.html' )
	
def search_filter( request ):
	''' Search and Sort Thread QuerySet and returns list of it. '''
	if request.user.is_staff :
		context = { 'search_types' : Thread.SEARCH_TYPES, 'filter_options' : Thread.FILTER_OPTIONS }
		if request.method == 'POST' :
			query = request.POST.get( 'query' )
			filter_option = request.POST.get( 'filter_option' )
			print( filter_option )
			search_type = request.POST.get( 'search_type' )
			if query != '':
				print( 'se')
				search_result = Thread.search( query, search_type )
			else:
				print( 'not' )
				search_result = Thread.objects.all()
			if filter_option != Thread.FILTER_OPTIONS[0] :
				thread_list = Thread.filter_qs( search_result, filter_option )
			context.update( { 
					'thread_list' : thread_list,
					'query' : query,
					'search_type' : search_type,
					'filter_option' : filter_option
				}
			)
		return render( request, 'threads/list.html', context )

def select_to_solve(request, id_no):
	if request.user.is_staff:
		#add code for checking for date
		member = get_object( request )
		thread = Thread.get_thread( request, id_no )
		if thread is not None  and member is not None:
			if thread.redressal is None or not thread.redressal.action == 'APPROVE' :
				curr_date = date.today()
				if thread.solving_date != curr_date :
					thread.solver = member
					thread.solving_date = curr_date
					thread.save( update_fields = [ 'solver', 'solving_date' ] )
					messages.success( request, f" Thread { thread } is  selected for solving. " )
				else :
					if thread.solver.user == request.user:
						return redirect(f'/thread/{ thread }/' )
					messages.info( request, f" Thread { id_no } is already selected by other member for solving. " )
			else :
				messages.info( request, f" Thread { id_no } is approved. Now, it can't be solved. " )
			return redirect( f'/thread/{ thread }/' )
	return redirect('/permission-denied/')

def deselect_to_solve(request, id_no):
	if request.user.is_staff:
		thread = Thread.get_thread( request, id_no )
		member = get_object( request )
		if thread is not None and member is not None :
			if thread.redressal is None or not thread.redressal.action == 'APPROVE':
				curr_date = date.today()
				if thread.solver != None and thread.solver.user == request.user:
					if thread.solving_date == curr_date:
						thread.solving_date = None
						thread.solver = None
						thread.save( update_fields = [ 'solver', 'solving_date' ] )
						messages.success( request, f' Thread { thread } is deselected for solving. ' )
					else :
						messages.info( request, f" Thread { thread } is not selected by no one. " )
				else :
					messages.info( request, f" Thread { thread } is selected by different user, you can't deselect it." )
			else :
				messages.info( request, f" Thread { thread } is already approved. Now, it can't be solved. " )
		return redirect( f'/thread/{ thread }/' )
	return render( request, 'permisssion_denied.html' )
