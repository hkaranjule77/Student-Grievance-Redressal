from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *
from user.models import Student,Member
from user.views import get_object
from django.db.models import Q

# Create your views here.
def chatbox(request):
    member_obj = get_object(request)
    msglist=Message.objects.filter(member=member_obj).order_by("-date").distinct()
    # msg_list = list(dict.fromkeys(msglist))

    return render(request, "chatbox.html", {'student': msglist})

def chatsearch(request):
    search1 = request.GET.get('chatsearch')
    s2 = request.GET.get('studsearch')
    if search1:
        search2 = Message.objects.filter(Q(student__user__first_name__icontains=search1) | Q(student__sid__icontains=search1) | Q(student__user__last_name__icontains=search1) | Q(msg__icontains=search1) ).order_by('-date')
        return render(request, "chatsearch.html", {"search": search2})
    elif s2:
        s3 = Student.objects.filter(Q(sid=s2) | Q(user__first_name__icontains=s2) | Q(user__last_name__icontains=s2)).order_by('-date')
        return (request, 'chatsearch.html', {'srch': s3})

# def chatpage(request,sid):
#     member_obj = get_object(request)
#     stud = Student.objects.get(sid=sid) #Retrived student having same id which is passed in func as arguement
#     # stud = get_object(request, username=sid)
#
#     prev_msg= Message.objects.filter(Q(student=stud) & Q(member=member_obj)).order_by('-date') #retriving previous conversation of student n member
#
#     if request.method=='POST':
#         msg = request.POST.get('msg_from_member')
#         global oc
#         oc = request.POST.get('openclose')
#         l = Message(msg=msg,student=stud,member=member_obj,msg_flag='member')
#         l.save()
#         return render(request, 'chatbox.html')
#     if request.method=="GET":
#         if prev_msg:
#             return render(request, 'chatpage.html', {'student':stud, 'msg': prev_msg})
#              # sending only student details
#         else:
#             return render(request, "chatpage.html", {'student':stud})

def chatpage(request):
    if request.method=="POST":
        val = request.POST.get('student_value')
        stud = Student.objects.get(sid=val)
        member_obj = get_object(request)
        # prev_msg1 =Message.objects.filter(student=stud)
        # prev_msg2= Message.objects.filter(member=member_obj)
        prev_msg= Message.objects.filter(Q(student=stud) & Q(member=member_obj)).order_by('date')
        if prev_msg:
            return render(request, 'chatpage.html', {'student':stud, 'msg': prev_msg})
                     # sending only student details
        else:
            return render(request, "chatpage.html", {'student':stud})

def chatpage1(request):
    if request.method=="POST":
        val = request.POST.get('val')
        stud = Student.objects.get(sid=val)
        member_obj = get_object(request)
        msg = request.POST.get('msg_from_member')
        global oc
        oc = request.POST.get('openclose')
        # newly added
        stud.os_flag = oc
        stud.save()
        l = Message(msg=msg,student=stud,member=member_obj,msg_flag='member')
        l.save()
        # prev_msg1 =Message.objects.filter(student=stud)
        # prev_msg2= Message.objects.filter(member=member_obj)
        prev_msg= Message.objects.filter(Q(student=stud) & Q(member=member_obj)).order_by('date')
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
    # else:
    #     list1 = Student.objects.all()
    #     return render(request, "allstudent.html", {'student': list1})




def studchatpage(request):
    if request.method=='POST':
        val = request.POST.get('member_value')
        studobj = get_object(request)
        memb = Member.objects.get(mid=val)
        global oc
        if studobj.oc_flag == 'close':
            msg_list = Message.objects.filter(Q(student=studobj) & Q(member=memb) & Q(msg_flag="member")).order_by('date')
            return render(request, "studchatpage.html", {'msg': msg_list, 'member': memb})
        elif studobj.oc_flag=="open" :
            msg_list = Message.objects.filter(Q(student=studobj) & Q(member=memb))
            return render(request, "studchatpage.html", {'msg': msg_list, 'oc': 'oc', 'member': memb})

    #     msg = request.POST.get('msg_from_student')
    #     l = Message(msg=msg, member=memb, student=studobj, msg_flag="student")
    #     l.save()
    # else:
    #

def studchatpage1(request):
    if request.method=="POST":
        msg = request.POST.get('msg_from_student')
        val = request.POST.get('member_value')
        studobj = get_object(request)
        memb = Member.objects.get(mid=val)
        l = Message(msg=msg, member=memb, student=studobj, msg_flag="student")
        l.save()

        if studobj.oc_flag == 'close':
            msg_list = Message.objects.filter(Q(student=studobj) & Q(member=memb) & Q(msg_flag="member")).order_by('date')
            return render(request, "studchatpage.html", {'msg': msg_list, 'member': memb})
        elif studobj.oc_flag == "open" :
            msg_list = Message.objects.filter(Q(student=studobj) & Q(member=memb))
            return render(request, "studchatpage.html", {'msg': msg_list, 'oc': 'oc', 'member': memb})



def studchatbox(request):
    studobj = get_object(request)
    member_list = list(Message.objects.filter(student=studobj).order_by('-date').distinct())
    return render(request, "studchatbox.html", {'member' : member_list})
