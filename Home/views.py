from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime, date, timedelta
import datetime
from django.views.decorators.cache import cache_control
from .models import useradmin, Crew, Port, Ship
from django.http import JsonResponse
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.contrib import messages

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
            request.session['name'] = dis.name
            request.session['userType'] = dis.role
            messages.success(request, "Sign In Successfully")
            return redirect('home')
        else:
            msg = "wrong user name or password or account does not exist!!"
            messages.error(request, msg)
            return render(request, 'signin.html')
    return render(request,'signin.html')


#====================================================================================
#----------------------------------------signup page----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signupPage(request):
    return render(request,'signin.html')


#====================================================================================
#----------------------------------------Add crew page----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addCrew(request):
    if 'id' in request.session:
        if request.method == 'POST':
            name = request.POST.get("name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            password = request.POST.get("password")
            if (useradmin.objects.filter(id=request.session['id'], role=request.session['userType'])).exists():
                dis = useradmin.objects.get(id=request.session['id'], role=request.session['userType'])
                ob = Crew()
                ob.name = name
                ob.email = email
                if(Crew.objects.filter(email = email).exists()):
                    messages.error(request, "Email Already Registered")
                    return render(request,'Home/addCrew.html')
                ob.phone = phone
                ob.password = password
                ob.added_user = dis.id
                ob.save()
                messages.success(request, "New Crew Added")
            return render(request,'Home/addCrew.html')
        return render(request,'Home/addCrew.html')
    return redirect('signinPage')


#====================================================================================
#----------------------------------------Add port page----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addPort(request):
    if 'id' in request.session:
        if request.method == 'POST':
            name = request.POST.get("name")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            location = request.POST.get("location")
            password = request.POST.get("password")
            if (useradmin.objects.filter(id=request.session['id'], role=request.session['userType'])).exists():
                dis = useradmin.objects.get(id=request.session['id'], role=request.session['userType'])
                ob = Port()
                ob.name = name
                ob.email = email
                if(Port.objects.filter(email = email).exists()):
                    messages.error(request, "Email Already Registered")
                    return render(request,'Home/addPort.html')
                ob.location = location
                ob.phone = phone
                ob.password = password
                ob.added_user = dis.id
                ob.save()
                messages.success(request, "New Port Added")
                return render(request,'Home/addPort.html')
        return render(request,'Home/addPort.html')
    return redirect('signinPage')

#====================================================================================
#----------------------------------------Crew Manager----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def crewManager(request):
    if 'id' in request.session:
        crew = Crew.objects.all()
        crewdrop = Crew.objects.filter(status = 1)
        ship = Ship.objects.all()
        shipdrop = Ship.objects.filter(status = 1)
        return render(request,'Crew/crewManager.html',{'crew' : crew, 'ship' : ship, 'crewdrop' : crewdrop, 'shipdrop' : shipdrop})
    return redirect('signinPage')

#====================================================================================
#----------------------------------------Add Ship----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addShip(request):
    if 'id' in request.session:
        if request.method == 'POST':
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            if (useradmin.objects.filter(id=request.session['id'], role=request.session['userType'])).exists():
                dis = useradmin.objects.get(id=request.session['id'], role=request.session['userType'])
                ob = Ship()
                ob.name = name
                if(Ship.objects.filter(name = name).exists()):
                    messages.error(request, "Ship Name Already Registered")
                    return render(request,'Home/addSip.html')
                ob.phone = phone
                ob.save()
                messages.success(request, "New Ship Added")
                return render(request,'Home/addShip.html')
        return render(request,'Home/addShip.html')
    return redirect('signinPage')


#====================================================================================
#----------------------------------------Crew Status Update----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def crewStatusUpdate(request, id):
    if 'id' in request.session:
        if request.method == 'POST':
            messages.success(request, "Status Updated")
            crew = Crew.objects.get(id = id)
            if crew.status == 1:
                Crew.objects.filter(id = id).update(status=0)
            else:
                Crew.objects.filter(id = id).update(status=1)
        return redirect('crewManager')
    return redirect('signinPage')

#====================================================================================
#----------------------------------------Add Ship To Crew ----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addShipToCrew(request, id):
    if 'id' in request.session:
        if request.method == 'POST':
            crew = request.POST.get("crew")
            ship = request.POST.get("ship")
            messages.success(request, "Updated")
        return redirect('crewManager')
    return redirect('signinPage')



#====================================================================================
#----------------------------------------Logout----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    request.session.flush()
    messages.success(request, "Logout Successfull")
    return redirect('home')
