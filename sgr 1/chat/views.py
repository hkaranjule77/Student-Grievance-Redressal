from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
from user.models import Student,Member
from user.views import get_object
from django.db.models import Q
# Create your views here.
def chatbox(request):
    member_obj = get_object(request)
    msg_lis=Message.objects.filter(member=member_obj).values('student').distinct()
    msg_list = msg_lis.order_by('-date')
    return render(request, "chatbox.html", {'student': msg_list})

def chatsearch(request):
    search1 = request.GET.get('chatsearch')
    s2 = request.GET.get('studsearch')
    if search1:
        search2 = Message.objects.filter(Q(student__user__first_name__icontains=search1) | Q(student__sid__icontains=search1) | Q(student__user__last_name__icontains=search1) | Q(msg__icontains=search1) ).order_by('-date')
        return render(request, "chatsearch.html", {"search": search2})
    elif s2:
        s3 = Student.objects.filter(Q(sid=s2) | Q(user__first_name__icontains=s2) | Q(user__last_name__icontains=s2)).order_by('-date')
        return (request, 'chatsearch.html', {'srch': s3})

def chatpage(request, id):
    member_obj = get_object(request)
    # stud = Student.objects.filter(sid=id) #Retrived student having same id which is passed in func as arguement
    stud = get_object(request, username=id)
    print(member_obj, stud)
    prev_msg= Message.objects.filter(Q(student=stud) & Q(member=member_obj)).order_by('-date') #retriving previous conversation of student n member

    if request.method=='POST':
        msg = request.POST.get('msg_from_member')
        global oc
        oc = request.POST.get('openclose')
        l = Message(msg=msg,student=stud,member=member_obj,msg_flag='member')
        l.save()
        return render(request, 'chatbox.html')
    if request.method=="GET":
        if prev_msg:
            return render(request, 'chatpage.html', {'student':stud, 'msg': prev_msg})
             # sending only student details
        else:
            return render(request, "chatpage.html", {'student':stud})

def allstudent(request):
    # list1= User.objects.filter(is_staff=False).order_by('first_name')
    # length = len(list1)
    # for i in range(length):
    #     list2.append(Student.objects.filter(Q(list1[i].first_name)))
    if request.method=="GET":
        list1 = Student.objects.all()
        return render(request, "allstudent.html", {'student': list1})
    else:
        list1 = Student.objects.all()
        return render(request, "allstudent.html", {'student': list1})




def studchatpage(request, id):
    studobj = get_object(request)
    memb = Member.objects.get(mid=id)
    if request.method=='POST':
        msg = request.POST.get('msg_from_student')
        l = Message(msg=msg, member=memb, student=studobj, msg_flag="student")
        l.save()
    else:
        if oc == 'close':
            msg_list = Message.objects.filter(Q(student=studobj) & Q(member=memb) & Q(msg_flag="member"))
            return render(request, "studchatpage.html", {'msg': msg_list, 'member': memb})
        elif oc=="open" :
            msg_list = Message.objects.filter(Q(student=studobj) & Q(member=memb))
            return render(request, "studchatpage.html", {'msg': msg_list, 'oc': 'oc', 'member': memb})




def studchatbox(request):
    studobj = get_object(request)
    member_list = list(Message.objects.filter(student=studobj).order_by('-date').values('member').distinct())
    return render(request, "studchatbox.html", {'member' : member_list})
