from django.shortcuts import render


#====================================================================================
#----------------------------------------home----------------------------------------

def home(request):
    return render(request,'home/index.html')