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
    path('addCrewPage', addCrewPage, name='addCrewPage'),
    path('logout', logout, name='logout'),
]