from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime, date, timedelta
import datetime
from django.views.decorators.cache import cache_control
from .models import useradmin
from django.http import JsonResponse
from django.http import HttpResponse, FileResponse, HttpResponseRedirect

#====================================================================================
#----------------------------------------home----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    today = datetime.datetime.now().date()
    if 'id' in request.session:
        id=request.session['id']
        userType=request.session['userType']
        if (useradmin.objects.filter(id=id, role=userType)).exists():
            dis = useradmin.objects.get(id=id, role=userType)
            # return HttpResponse()
            return render(request, 'Home/index.html', {'id': id, 'userDeatils': dis, 'userType' : dis.role})    
    return render(request,'Home/index.html')


#====================================================================================
#----------------------------------------signin page----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signinPage(request):
    if request.method == 'POST':
        useremail = request.POST.get('email')
        password = request.POST.get('password')
        if (useradmin.objects.filter(email=useremail, password=password)).exists():
            dis = useradmin.objects.get(email=useremail, password=password)
            request.session['id'] = dis.id
            request.session['userType'] = dis.role
            return redirect('home')
    else:
        msg = "wrong user name or password or account does not exist!!"
        return render(request, 'signin.html', {'msg': msg})
    return render(request,'signin.html')


#====================================================================================
#----------------------------------------signup page----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signupPage(request):
    return render(request,'signin.html')


#====================================================================================
#----------------------------------------Add crew page----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addCrewPage(request):
    if 'id' in request.session:
        id=request.session['id']
        userType=request.session['userType']
        if (useradmin.objects.filter(id=id, role=userType)).exists():
            dis = useradmin.objects.get(id=id, role=userType)
            return render(request, 'Home/addCrew.html', {'id': id, 'userDeatils': dis, 'userType' : dis.role})   
    return render(request,'Home/addCrew.html')


#====================================================================================
#----------------------------------------Logout----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    request.session.flush()
    return redirect('home')
