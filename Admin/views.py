from django.shortcuts import render
from datetime import datetime, date, timedelta
import datetime
from django.views.decorators.cache import cache_control


#====================================================================================
#----------------------------------------home----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    today = datetime.datetime.now().date()
    if 'id' in request.session:
        id=request.session['id']
        return render(request, 'home/index.html', {'id': id, 'userDeatils': dis, 'userType' : userType})    
    return render(request,'home/index.html')

#====================================================================================
#----------------------------------------signin page----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signinPage(request):
    return render(request,'signin.html')

#====================================================================================
#----------------------------------------signup page----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signupPage(request):
    return render(request,'signup.html')