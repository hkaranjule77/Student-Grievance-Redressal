from django.shortcuts import render, redirect
from django.db.models import QuerySet
from django.core.exceptions import ObjectDoesNotExist

from .models import Complain
from user.models import Student, Member

from datetime import date


# Create your views here.
def list(request):
    if request.user.is_staff:
        complain_list = Complain.objects.all()
    elif request.user.is_authenticated:
        student = Student.objects.get(user = request.user)
        complain_list = Complain.objects.filter(complainer = student)
    else:
        return redirect('/permission-denied/')
    context = { 'complain_list' : complain_list }
    return render(request, 'complain/list.html', context)

def add(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            context = { 'message' : 'Members are not allowed to add complain.' }
            return render(request, 'permission-denied.html', context)
        complain = Complain.init(request)
        print(complain.subject, 'complain')
        if complain.is_valid():
            print('valid')
            complain.save()
            message = 'Complain registered. Track it on Complain Tab'
            context = { 'categories' : Complain.categories, 'sub_categories' : Complain.sub_categories,
                        'message' : message }
        else:
            context = { 'categories' : Complain.categories, 'sub_categories' : Complain.sub_categories }
        return render(request, 'complain/add.html', context)
    else:
        return redirect('/permission-denied.html/')

def detail(request, id_no):
    try:
        complain = Complain.objects.get(id = id_no)
    except ObjectDoesNotExist:
        context = { 'message' : 'No such complain exist' }
        return render(request, 'error.html', context)
    curr_date = date.today()
    if complain.solve_date != curr_date:
        context = { 'complain' : complain, 'button' : True}
        return render(request, 'complain/detail.html', context)
    context = {'complain' : complain, 'button' : False}
    return render(request, 'complain/detail.html', context)

def select(request, id_no):
    if request.user.is_staff:
        #add code for checking for date
        try:
            complain = Complain.objects.get(id = id_no)
        except ObjectDoesNotExist:
            context = { 'message' : 'No such complain exist' }
            return render(request, 'error.html', context)
        if not complain.approved:
            curr_date = date.today()
            if complain.solve_date != curr_date:
                solver = Member.objects.get(user = request.user)
                complain.solver = solver
                complain.solve_date = curr_date
                complain.save(update_fields = ['solver', 'solve_date'])
                message = "This complain selected for solving."
            else:
                if complain.solver.user == request.user:
                    return redirect(f'/complain/{complain.id}/')
                message = "This complain is already selected by other member."
        else:
            message = "Complain is approved. Now, it can't be solved"
        context = {'complain' : complain, 'select_button' : False, 'message' : message}
        return render(request, 'complain/detail.html', context)
    return redirect('/permission-denied/')
        
        
def deselect(request, id_no):
    if request.user.is_staff:
        try:
            complain = Complain.objects.get(id = id_no)
        except ObjectDoesNotExist:
            message = "No such Complain exist."
        if not complain.approved:
            curr_date = date.today()
            if complain.solver != None and complain.solver.user == request.user:
                if complain.solve_date == curr_date:
                    complain.solve_date = None
                    complain.solver = None
                    complain.save(update_fields = ['solver', 'solve_date'])
                    message = 'Deselected the complain'
                else:
                    message = "Currently, it's not selected by no one."
                select_button = True
            else:
                message = "Currently, its selected by different user, you can't deselect it."
                if complain.solver and complain.solve_date == curr_date:
                    select_button = False
                else:
                    select_button = True
        else:
            select_button = False
            message = "Complain is already approved. Noe, it can't be solved"
        context = { 'complain' : complain, 'select_button' : select_button, 'message' : message}
        return render(request, 'complain/detail.html', context)
    return redirect('/permisssion-denied/')
            
def search(request):
    if request.user.is_staff:
        options = ('all','id', 'subject', 'category', 'sub_category', 'brief')
        query = request.POST.get('query')
        opt = request.POST.get('opt')
        if query == None:
            query = ""
        if query =="":
            queryset = Complain.objects.all()
            print('hi')
        else:
            print('filter',opt, options[0])
            queryset = Complain.objects.none()
            if opt == options[0] or opt == options[1]:
                q1 = Complain.search_id(query = query)
                q1 = Complain.objects.filter(q1)
                queryset = queryset.union(q1)
            if opt == options[0] or opt == options[2]:
                q2 = Complain.search_subject(query = query)
                q2 = Complain.objects.filter(q2)
                queryset = queryset.union(q2)
            if opt == options[0] or opt == options[3]:
                q3 = Complain.search_category(query = query)
                q3 = Complain.objects.filter(q3)
                queryset = queryset.union(q3)
            if opt == options[0] or opt == options[4]:
                q4 = Complain.search_sub_category(query = query)
                q4 = Complain.objects.filter(q4)
                queryset = queryset.union(q4)
            if opt == options[0] or opt == options[5]:
                q5 = Complain.search_brief(query = query)
                q5 = Complain.objects.filter(q5)
                queryset = queryset.union(q5)
        print(queryset,'aalk')
        queryset.distinct()
        message = f' search count : {len(queryset)}'
        context = {'queryset' : queryset, 'query' : query, 'options' : options, 'message' : message }
        return render(request, 'complain/search.html', context)
    return redirect('/permission-denied/')