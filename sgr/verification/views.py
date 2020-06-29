from django.shortcuts import render

from user.models import Member, Student
from .models import TableDetail

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
                return render(request, 'verification/add_table.html')
            else:
                context.update( { 'message' :
                                  'Please fill out full form then Submit it.' } )
            return render(request, 'verification/add_table.html', context)
    return render(request, 'pemission_denied.html')