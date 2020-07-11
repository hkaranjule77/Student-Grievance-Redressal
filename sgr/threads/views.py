from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import Thread
from complain.models import Complain, Note
from user.views import get_object


# Create your views here.

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
			if not thread.approved:
				if not thread.redressed:
					thread.init_for_redressal( request, member )
					if thread.is_redress_valid():
						thread.redress()
						messages.success( request, f' Thread { thread } is redressed' )
					else:
						messages.info( request, ' Please fill out full form first, before submitting it. ')
				else:
					messages.info( request, ' Thread is already redressed. ')
			else:
				messages.info( request, f' Thread { thread } is already approved. ')
		else:
			messages.error( request, f' Thread { id_no } does not exist. ' )
		return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )
	return render( request, 'permission_denied.html' )
	
def approve_thread( request, id_no ):
	''' Function for approval in redressal of Thread. '''
	if request.user.is_staff:
		member = get_object( request )
		thread = Thread.get_thread( request, id_no )
		if member is not None and thread is not None:
			if thread.action == '' or thread.action == 'REJECT':
				thread.approve( member )
				messages.success( request, f' Redressal of Thread { id_no } is approved. ')
			else:
				messages.info( request, f' Redressal of Thread { id_no } is already approved. ' )
		return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )
	return render( request, 'permission_thread.html' )

def detail(request, id_no):
	if request.user.is_staff:
		thread = Thread.get_thread(  request, id_no )
		member = get_object( request )
		pinned_complain_list = Complain.objects.filter( thread = thread, pinned_in_thread = True )
		unpinned_complain_list = Complain.objects.filter( thread = thread, pinned_in_thread = False)
		pinned_note_list = Note.objects.filter( thread = thread, pinned = True )
		unpinned_note_list = Note.objects.filter( thread = thread, pinned = False)
		context = { 
			'thread' : thread,
			'member' : member,
			'pinned_complain_list' : pinned_complain_list,
			'unpinned_complain_list' : unpinned_complain_list,
			'pinned_note_list' : pinned_note_list,
			'unpinned_note_list' : unpinned_note_list,
		}
		return render( request, 'threads/detail.html', context )
	return render( request, 'permission_denied.html' )
	
def list( request ):
	''' Lists all Thread and render it on a page. '''
	if request.user.is_staff:
		thread_list = Thread.objects.all()
		context = { 'thread_list' : thread_list }
		return render( request, 'threads/list.html', context )
	return render( request, 'permission_denied.html' )
	
	
def reject_thread( request, id_no ):
	if request.user.is_staff:
		thread = Thread.get_thread( request, id_no )
		member = get_object( request )
		if member is not None and thread is not None:
			if thread.action == '' or thread.action == 'APPROVE':
				thread.init_for_reject( request, member )
				if thread.is_reject_valid():
					thread.reject()
					messages.success( request, f' Redressal of Thread { thread } is rejected. ')
				else:
					messages.info( 'Please fill rejection message first then submit it. ')
			else:
				messages.info( request, f' Redressal of Thread { id_no } is already rejected. ')
		return HttpResponseRedirect( request.META.get( 'HTTP_REFERER' ) )
	return
