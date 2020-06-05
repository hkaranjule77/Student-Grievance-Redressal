from django.shortcuts import render, redirect
#from django.db.models.exceptions import DoesNotExist

from .models import Complain
from user.models import Member

from datetime import date

# Create your views here.
def list(request):
    all_complain = Complain.objects.all()
    context = { 'all_complain' : all_complain }
    return render(request, 'complain/list.html', context)

def detail(request, id_no):
    complain = Complain.objects.get(id = id_no)
    curr_date = date.today()
    if complain.solve_date != curr_date:
        context = { 'complain' : complain, 'button' : True}
        return render(request, 'complain/detail.html', context)
    context = {'complain' : complain, 'button' : False}
    return render(request, 'complain/detail.html', context)

def select(request, id_no):
    if request.user.is_staff:
        #add code for checking for date
        complain = Complain.objects.get(id = id_no)
        curr_date = date.today()
        if complain.solve_date != curr_date:
            solver = Member.objects.get(user = request.user)
            complain.solver = solver
            complain.solve_date = curr_date
            complain.save(update_fields = ['solver', 'solve_date'])
            message = "This complain selected for solving."
            context = { 'complain' : complain, 'button' : False, 'message' : message}
            return render(request, 'complain/detail.html', context)
        else:
            if complain.solver.user == request.user:
                return redirect(f'/complain/{complain.id}/')
            message = "This complain is already selected by other member."
            context = {'complain' : complain, 'button' : False, 'message' : message}
            return render(request, 'complain/detail.html', context)
    return redirect('/permission-denied/')
        
        
def deselect(request, id_no):
    if request.user.is_staff:
        complain = Complain.objects.get(id = id_no)
        curr_date = date.today()
        if complain.solver != None and complain.solver.user == request.user:
            if complain.solve_date == curr_date:
                complain.solve_date = None
                complain.solver = None
                complain.save(update_fields = ['solver', 'solve_date'])
                message = 'Deselected the complain'
            else:
                message = "Currently, it's not selected by no one."
            button = True
        else:
            message = "Currently, its selected by different user, you can't deselect it."
            if complain.solver and complain.solve_date == curr_date:
                button = False
            else:
                button = True
        context = { 'complain' : complain, 'button' : button, 'message' : message}
        return render(request, 'complain/detail.html', context)
    return redirect('/permisssion-denied/')
            
def search(request):
    if request.user.is_staff:
        query = request.POST.get('query')
        if query == None or query =="":
            queryset = Complain.objects.all()
        else:
            queryset = Complain.objects.filter(subject = query)
            queryset2 = Complain.objects.filter(id = query)
            queryset = queryset.union(queryset2)
        context = {'queryset' : queryset, 'query' : query }
        return render(request, 'complain/search.html', context)
    return redirect('/permission-denied/')