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
    path('crewHome', crewHome, name='crewHome'),
    path('shipHome', shipHome, name='shipHome'),
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
    path('containerManager', containerManager, name='containerManager'),
    path('shipStatusUpdate/<id>', shipStatusUpdate, name='shipStatusUpdate'),
    path('portStatusUpdate/<id>', portStatusUpdate, name='portStatusUpdate'),
    path('containerStatusUpdate/<id>', containerStatusUpdate, name='containerStatusUpdate'),
    path('containerCollectStatusUpdate/<id>', containerCollectStatusUpdate, name='containerCollectStatusUpdate'),
    path('containerDropStatusUpdate/<id>', containerDropStatusUpdate, name='containerDropStatusUpdate'),
    path('crewProfilePage', crewProfilePage, name='crewProfilePage'),
    path('shipRoute', shipRoute, name='shipRoute'),

]