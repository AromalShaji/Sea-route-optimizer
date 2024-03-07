from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime, date, timedelta
import datetime
from django.views.decorators.cache import cache_control
from .models import useradmin, Crew, Port, Ship, Container
from django.http import JsonResponse
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.contrib import messages


#====================================================================================
#----------------------------------------ship route ----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def shipRoute(request):
    today = datetime.datetime.now().date()
    if 'id' in request.session:
        id=request.session['id']
        userType=request.session['userType']
        if (Ship.objects.filter(id=id, role=userType)).exists():
            dis = Ship.objects.get(id=id, role=userType)
            return render(request, 'Ship/route.html', {'id': id, 'userDeatils': dis, 'userType' : dis.role})    
        return render(request,'Ship/route.html')
    return render(request,'Crew/home.html')
    
    


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
#----------------------------------------Crew home----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def crewHome(request):
    today = datetime.datetime.now().date()
    if 'id' in request.session:
        id=request.session['id']
        userType=request.session['userType']
        if (Crew.objects.filter(id=id, role=userType)).exists():
            dis = Crew.objects.get(id=id, role=userType)
            ship = Ship.objects.get(id = dis.ship)
            container = Container.objects.filter(ship = dis.ship)
            return render(request, 'Crew/home.html', {'id': id, 'userDeatils': dis, 'userType' : dis.role, 'ship' : ship, 'container' : container})    
        return render(request,'Crew/home.html')
    return render(request,'signin.html')



#====================================================================================
#----------------------------------------Ship home----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def shipHome(request):
    today = datetime.datetime.now().date()
    if 'id' in request.session:
        id=request.session['id']
        userType=request.session['userType']
        if (Ship.objects.filter(id=id, role=userType)).exists():
            dis = Ship.objects.get(id=id, role=userType)
            container = Container.objects.filter(ship = dis.id)
            crew = Crew.objects.filter(ship = dis.id)
            return render(request, 'Ship/home.html', {'id': id, 'userDeatils': dis, 'userType' : dis.role, 'container' : container, 'crew' : crew})    
        return render(request,'Ship/home.html')
    return render(request,'signin.html')



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
            messages.success(request, "Login Successfully")
            return redirect('home')
        elif (Crew.objects.filter(email=useremail, password=password)).exists():
            dis = Crew.objects.get(email=useremail, password=password)
            request.session['id'] = dis.id
            request.session['name'] = dis.name
            request.session['userType'] = dis.role
            messages.success(request, "Login Successfully")
            return redirect('crewHome')
        elif (Ship.objects.filter(name=useremail, password=password)).exists():
            dis = Ship.objects.get(name=useremail, password=password)
            request.session['id'] = dis.id
            request.session['name'] = dis.name
            request.session['userType'] = dis.role
            messages.success(request, "Login Successfully")
            return redirect('shipHome')
        else:
            msg = "wrong user name or password or account does not exist!!"
            messages.error(request, msg)
            return render(request, 'signin.html')
    return render(request,'signin.html')



#====================================================================================
#----------------------------------------signup page----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signupPage(request):
    return render(request,'signup.html')



#====================================================================================
#----------------------------------------crew profile----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def crewProfilePage(request):
    if 'id' in request.session:
        if request.method == 'POST':
            password = request.POST.get("password")
            if(Crew.objects.filter(id=request.session['id'], role=request.session['userType'])).exists():
                Crew.objects.filter(id=request.session['id'], role=request.session['userType']).update(password = password)
                messages.success(request, "Profile Updated")
                crew = Crew.objects.get(id=request.session['id'], role=request.session['userType'])
                return render(request,'Crew/profile.html', {'crew' : crew})
            crew = Crew.objects.get(id=request.session['id'], role=request.session['userType'])
            messages.success(request, "Something went wrong!")
            return render(request,'Crew/profile.html', {'crew' : crew})
        crew = Crew.objects.get(id=request.session['id'], role=request.session['userType'])
        return render(request,'Crew/profile.html', {'crew' : crew})
    return redirect('signinPage')



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
#----------------------------------------Ship Manager----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def shipManager(request):
    if 'id' in request.session:
        crew = Crew.objects.all()
        crewdrop = Crew.objects.filter(status = 1)
        ship = Ship.objects.all()
        shipdrop = Ship.objects.filter(status = 1)
        ship_crew_counts = {}
        for ships in ship:
            crew_count = Crew.objects.filter(ship=ships.id).count()
            ship_crew_counts[ships.id] = crew_count
        return render(request,'Ship/shipManager.html',{'crew' : crew, 'ship' : ship, 'crewdrop' : crewdrop, 'shipdrop' : shipdrop, 'ship_crew_counts' : ship_crew_counts})
    return redirect('signinPage')



#====================================================================================
#----------------------------------------Port Manager----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def portManager(request):
    if 'id' in request.session:
        port = Port.objects.all()
        portdrop = Port.objects.filter(status = 1)
        return render(request,'Port/portManager.html',{'port' : port, 'portdrop' : portdrop})
    return redirect('signinPage')


#====================================================================================
#----------------------------------------Container Manager----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def containerManager(request):
    if 'id' in request.session:
        container = Container.objects.all()
        ship = Ship.objects.all()
        return render(request,'Container/containerManager.html',{'container' : container, 'ship' : ship})
    return redirect('signinPage')



#====================================================================================
#----------------------------------------Add Ship----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addShip(request):
    if 'id' in request.session:
        if request.method == 'POST':
            name = request.POST.get("name")
            phone = request.POST.get("phone")
            password = request.POST.get("password")
            if (useradmin.objects.filter(id=request.session['id'], role=request.session['userType'])).exists():
                dis = useradmin.objects.get(id=request.session['id'], role=request.session['userType'])
                ob = Ship()
                ob.name = name
                if(Ship.objects.filter(name = name).exists()):
                    messages.error(request, "Ship Name Already Registered")
                    return render(request,'Home/addShip.html')
                ob.phone = phone
                ob.password = password
                ob.added_user = dis.id
                ob.save()
                messages.success(request, "New Ship Added")
                return render(request,'Home/addShip.html')
        return render(request,'Home/addShip.html')
    return redirect('signinPage')


#====================================================================================
#----------------------------------------Add Container----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addContainer(request):
    if 'id' in request.session:
        shipdrop = Ship.objects.filter(status = 1)
        if request.method == 'POST':
            number = request.POST.get("number")
            source = request.POST.get("source")
            date = request.POST.get("date")
            destination = request.POST.get("destination")
            ship = request.POST.get("ship")
            ob = Container()
            ob.containerNumber = number
            ob.source = source
            ob.destination = destination
            ob.date = date
            ob.ship = ship
            dis = useradmin.objects.get(id=request.session['id'], role=request.session['userType'])
            ob.added_user = dis.id
            ob.save()
            messages.success(request, "New Container Added")
            return render(request,'Home/addContainer.html', {'shipdrop' : shipdrop})
        return render(request,'Home/addContainer.html', {'shipdrop' : shipdrop})
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
#----------------------------------------Container Collect  Status Update----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def containerCollectStatusUpdate(request, id):
    if 'id' in request.session:
        if request.method == 'POST':
            container = Container.objects.get(id = id)
            if container.status == 1:
                if container.drop_status == 0:
                    if container.collect_status == 1:
                        Container.objects.filter(id = id).update(collect_status=0)
                        messages.success(request, "Status Updated")
                    else:
                        Container.objects.filter(id = id).update(collect_status=1)
                        messages.success(request, "Status Updated")
                else:
                    messages.error(request, "Container is Already Droped")
        return redirect('crewHome')
    return redirect('signinPage')



#====================================================================================
#----------------------------------------Container Drop  Status Update----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def containerDropStatusUpdate(request, id):
    if 'id' in request.session:
        if request.method == 'POST':
            container = Container.objects.get(id = id)
            if container.status == 1:
                if container.collect_status == 1:
                    if container.drop_status == 1:
                        Container.objects.filter(id = id).update(drop_status=0)
                        messages.success(request, "Status Updated")
                    else:
                        Container.objects.filter(id = id).update(drop_status=1)
                        messages.success(request, "Status Updated")
                else:
                    messages.error(request, "Container is not collected")
        return redirect('crewHome')
    return redirect('signinPage')



#====================================================================================
#----------------------------------------Container Status Update----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def containerStatusUpdate(request, id):
    if 'id' in request.session:
        if request.method == 'POST':
            messages.success(request, "Status Updated")
            container = Container.objects.get(id = id)
            if container.status == 1:
                Container.objects.filter(id = id).update(status=0)
            else:
                Container.objects.filter(id = id).update(status=1)
        return redirect('containerManager')
    return redirect('signinPage')


#====================================================================================
#----------------------------------------Port Status Update----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def portStatusUpdate(request, id):
    if 'id' in request.session:
        if request.method == 'POST':
            messages.success(request, "Status Updated")
            port = Port.objects.get(id = id)
            if port.status == 1:
                Port.objects.filter(id = id).update(status=0)
            else:
                Port.objects.filter(id = id).update(status=1)
        return redirect('portManager')
    return redirect('signinPage')



#====================================================================================
#----------------------------------------Crew Status Update----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def shipStatusUpdate(request, id):
    if 'id' in request.session:
        if request.method == 'POST':
            messages.success(request, "Status Updated")
            ship = Ship.objects.get(id = id)
            if ship.status == 1:
                Ship.objects.filter(id = id).update(status=0)
            else:
                Ship.objects.filter(id = id).update(status=1)
        return redirect('shipManager')
    return redirect('signinPage')



#====================================================================================
#----------------------------------------Add Ship To Crew ----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addShipToCrew(request):
    if 'id' in request.session:
        if request.method == 'POST':
            crew = request.POST.get("crew")
            ship = request.POST.get("ship")
            date = request.POST.get("date")
            time = request.POST.get("time")
            Crew.objects.filter(id = crew, status = 1).update(ship = ship, date = date, time = time)
            messages.success(request, "Updated")
        return redirect('crewManager')
    return redirect('signinPage')



#====================================================================================
#----------------------------------------Add crew To ship ----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def addCrewToShip(request):
    if 'id' in request.session:
        if request.method == 'POST':
            crew = request.POST.get("crew")
            ship = request.POST.get("ship")
            date = request.POST.get("date")
            time = request.POST.get("time")
            Crew.objects.filter(id = crew, status = 1).update(ship = ship, date = date, time = time)
            messages.success(request, "Updated")
        return redirect('shipManager')
    return redirect('signinPage')



#====================================================================================
#----------------------------------------Logout----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    request.session.flush()
    messages.success(request, "Logout Successfull")
    return redirect('signinPage')
