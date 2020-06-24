from django.shortcuts import render, redirect

#sgr_views

def home(request):
    if request.user.is_authenticated:
        return redirect('/user/dashboard/')
    return render(request, 'home.html')
    
def perm_denied(request):
    return render(request, 'permission_denied.html')