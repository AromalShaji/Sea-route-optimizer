from django.urls import path
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #======================================================================================================
    #------------------------------------------------------------------------------------------------------
    #home
    path('', home, name='home'),
    path('signinPage', signinPage, name='signinPage'),
    path('signupPage', signupPage, name='signupPage'),
    path('addCrew', addCrew, name='addCrew'),
    path('logout', logout, name='logout'),
    path('addPort', addPort, name='addPort'),
    path('crewManager', crewManager, name='crewManager'),
    path('crewStatusUpdate/<id>', crewStatusUpdate, name='crewStatusUpdate'),
    path('addShip', addShip, name='addShip'),
    path('addShipToCrew', addShipToCrew, name='addShipToCrew'),
    path('addCrewToShip', addCrewToShip, name='addCrewToShip'),
    path('addContainer', addContainer, name='addContainer'),
    path('shipManager', shipManager, name='shipManager'),
    path('portManager', portManager, name='portManager'),
    path('shipStatusUpdate/<id>', shipStatusUpdate, name='shipStatusUpdate'),
    path('portStatusUpdate/<id>', portStatusUpdate, name='portStatusUpdate'),
]