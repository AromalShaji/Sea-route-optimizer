from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime, date, timedelta
import datetime
from django.views.decorators.cache import cache_control
from .models import useradmin, Crew, Port, Ship, Container, RoutePrediction, RouteInput
from django.http import JsonResponse
from django.http import HttpResponse, FileResponse, HttpResponseRedirect
from django.contrib import messages
from skimage.graph import route_through_array
import joblib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.lines import Line2D
import geopandas as gpd
# from joblib import load
from shapely.geometry import Point, LineString
# model = load(r"C:\Users\user\main project\marengo\Marengo\Model\DTR_model.joblib")
import random


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
    return render(request,'Ship/home.html')
    
def generate_route(start_point, end_point, start_time, end_time, lon_min, lon_max, lat_min, lat_max, draft, generation_count, pop_size, offspring):
    def distance(point1, point2):
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    population = [[random.uniform(lon_min, lon_max), random.uniform(lat_min, lat_max)] for _ in range(pop_size)]

    for generation in range(generation_count):
        fitness = [distance(start_point, route) + distance(route, end_point) for route in population]

        parents = []
        for _ in range(offspring):
            tournament = random.sample(range(pop_size), 3)
            winner = min(tournament, key=lambda x: fitness[x])
            parents.append(population[winner])

        offspring_list = []
        for i in range(offspring):  # Corrected variable name to avoid conflict with the parameter name
            parent1, parent2 = random.sample(parents, 2)
            crossover_point = random.randint(0, len(parent1) - 1)
            child = parent1[:crossover_point] + parent2[crossover_point:]
            offspring_list.append(child)

        population = sorted(population, key=lambda x: fitness[population.index(x)])
        for i in range(offspring):
            population[-(i+1)] = offspring_list[i]

        for i in range(pop_size):
            if random.random() < 0.1:
                mutation_point = random.randint(0, len(population[i]) - 1)
                population[i][mutation_point] += random.uniform(-1, 1)

    return population


def optimize_route(request):
    if request.method == 'POST':
         # Retrieve input data from the form
        lon_st = float(request.POST['lon_st'])
        lat_st = float(request.POST['lat_st'])
        lon_de = float(request.POST['lon_de'])
        lat_de = float(request.POST['lat_de'])
        stTime = request.POST['stTime']
        eTime = request.POST['eTime']
        generation_count = int(request.POST['generation_count'])
        pop_size = int(request.POST['pop_size'])
        offspring = int(request.POST['offspring'])
        lon_min = int(request.POST['lon_min'])
        lon_max = int(request.POST['lon_max'])
        lat_min = int(request.POST['lat_min'])
        lat_max = int(request.POST['lat_max'])
        draft = float(request.POST['draft'])


# Save input data to the database
        route_input = RouteInput.objects.create(
            lon_st=lon_st, lat_st=lat_st, lon_de=lon_de, lat_de=lat_de,
            stTime=stTime, eTime=eTime, generation_count=generation_count,
            pop_size=pop_size, offspring=offspring, lon_min=lon_min,
            lon_max=lon_max, lat_min=lat_min, lat_max=lat_max, draft=draft
        )
        
        
        # Extract input data from the RouteInput object
        lon_st = route_input.lon_st
        lat_st = route_input.lat_st
        lon_de = route_input.lon_de
        lat_de = route_input.lat_de
        stTime = route_input.stTime
        eTime = route_input.eTime
        generation_count = route_input.generation_count
        pop_size = route_input.pop_size
        offspring = route_input.offspring
        lon_min = route_input.lon_min
        lon_max = route_input.lon_max
        lat_min = route_input.lat_min
        lat_max = route_input.lat_max
        draft = route_input.draft
        
        # Define startpoint and endpoint
        startpoint = (lon_st, lat_st)
        endpoint = (lon_de, lat_de)

        # Generate the sea route
        route = generate_route(startpoint, endpoint, stTime, eTime, lon_min, lon_max, lat_min, lat_max, draft, generation_count, pop_size, offspring)


        # Load the machine learning model
        model_path = r"C:\Users\ciyak\Documents\GitHub\marengo\Marengo\Model\DTR_model.joblib"
        # joblib.dump(model_path, model_path, protocol=2)
        try:
            model = joblib.load(model_path)
        except Exception as e:
            return HttpResponse(f"Error loading the model: {e}")

        # # Perform prediction using the machine learning model
        # input_data = [[route_input.lon_st, route_input.lat_st, route_input.lon_de,
        #     route_input.lat_de, route_input.stTime, route_input.eTime,
        #     route_input.generation_count, route_input.pop_size,
        #     route_input.offspring, route_input.lon_min, route_input.lon_max,
        #     route_input.lat_min, route_input.lat_max, route_input.draft]]  # Ensure input data is in correct format
        # try:
        #     predicted_route = model.predict(input_data)
        # except Exception as e:
        #     return HttpResponse(f"Error predicting route: {e}")


# Placeholder data for visualization (as in the original code snippet)
        timeGridsDisplay = np.random.rand(10, 10)
        route_minfuelUSe_Display = np.random.rand(3, 10)
        route_minTime_Display = np.random.rand(3, 10)

        # Crop the world map with bounding points
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        world_cropped = world.cx[lon_min:lon_max, lat_min:lat_max]

        # Plotting the cropped map with a colorful background
        fig, ax = plt.subplots(figsize=(14, 7))
        world_cropped.plot(ax=ax, column='pop_est', cmap='viridis')

        # Plotting the sea route
        if route:
            route_line = LineString([Point(lon_st, lat_st)] + route + [Point(lon_de, lat_de)])
            gpd.GeoSeries(route_line).plot(ax=ax, color='blue')

        # Plotting the start and end points
        ax.plot(startpoint[0], startpoint[1], 'k^', markersize=15)
        ax.plot(endpoint[0], endpoint[1], 'k*', markersize=15)

        # Plotting the scatter plots
        im = ax.imshow(timeGridsDisplay, aspect='auto', vmin=np.min(timeGridsDisplay), cmap='viridis')
        route_minTime_Display_transposed = route_minTime_Display.T
        sc2 = ax.scatter(route_minfuelUSe_Display[0], route_minfuelUSe_Display[1], c=route_minfuelUSe_Display[2], cmap='YlGn', edgecolor='none')
        sc1 = ax.scatter(route_minTime_Display_transposed[0], route_minTime_Display_transposed[1], c=route_minTime_Display_transposed[2], cmap='YlOrRd', edgecolor='none', label='fastest')

        # Adding colorbar
        fig.colorbar(im, ax=ax, orientation='horizontal', label='time per grid cell', shrink=0.8)

        # Adding legend
        custom_lines = [
            Line2D([0], [0], color='blue', lw=4),
            Line2D([0], [0], marker='^', color='k', markersize=10, linestyle='None'),
            Line2D([0], [0], marker='*', color='k', markersize=10, linestyle='None'),
        ]
        ax.legend(custom_lines, ['sea route', 'start point', 'end point'], loc='upper right')

        # Convert the plot to a HTML string
        import io
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        import base64
        plot_data = base64.b64encode(buf.read()).decode('utf-8')

        # Close the plot
        plt.close()

        # Pass the visualization to the template for rendering
        return render(request, 'Ship/predicted_route_details.html', {'plot_data': plot_data})

    # Handle GET request if needed
    return redirect('shipRoute')
    #     # Redirect to a new page to display the predicted route
    #     return render('predicted_route_details.html', {'predicted_route': predicted_route})

    # # Handle GET request if needed
    # return redirect('shipRoute')

# def predicted_route_details(request):
#     # Retrieve predicted route details from the database
#     # Replace this with the actual code to retrieve data from your database
#     route_predictions = RoutePrediction.objects.all()  # You may need to filter this queryset based on your requirements
    
#     # Pass the route predictions to the template
#     return render(request, 'predicted_route_details.html', {'route_predictions': route_predictions})

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
            if dis.ship:
                ship = Ship.objects.get(id = dis.ship)
            else:
                ship = ""
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
        crewdrop = Crew.objects.filter(status = 1, ship = "")
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
        crewdrop = Crew.objects.filter(status = 1, ship = "")
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
#----------------------------------------Crew Ship Update----------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def crewShipUpdate(request, id):
    if 'id' in request.session:
        if request.method == 'POST':
            messages.success(request, "Ship Removed")
            crew = Crew.objects.get(id = id)
            if Crew.objects.filter(id=id, ship__isnull=False).exists():
                Crew.objects.filter(id=id).update(ship="")
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
                        Container.objects.filter(id = id).update(drop_status=0, status=1)
                        messages.success(request, "Status Updated")
                    else:
                        Container.objects.filter(id = id).update(drop_status=1, status=0)
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
            # date = request.POST.get("date")
            # time = request.POST.get("time")
            Crew.objects.filter(id = crew, status = 1).update(ship = ship)
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
            # date = request.POST.get("date")
            # time = request.POST.get("time")
            Crew.objects.filter(id = crew, status = 1).update(ship = ship)
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
