from django.shortcuts import render

#sgr_views

def home(request):
	return render(request, 'home.html')
    
def perm_denied(request):
    return render(request, 'perm_denied.html')