from django.shortcuts import render, redirect

#sgr_views

def contact_dev( request ):
	return render( request, 'contact_dev.html')

def contact_us( request):
	return render( request, 'contact_us.html' )

def home(request):
    if request.user.is_authenticated:
        return redirect('/user/dashboard/')
    return render(request, 'home.html')
    
def about_us( request ):
	return render( request, 'about_us.html' )
    
def perm_denied(request):
    return render(request, 'permission_denied.html')
    
def temp(request):
	return render( request, 'temp.html')
