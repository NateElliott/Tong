from django.conf.urls import url
from django.contrib import admin
from Core.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),


    # register
    url(r'^register', Register.as_view()),

    # sign in
    url(r'^signin', Signin.as_view()),

    # sign out
    url(r'^signout', Signout.as_view()),

    # profile
    url(r'^profile', ProfileView.as_view()),

    # create teams
    url(r'^teams/create', CreateTeam.as_view()),

    # team view
    url(r'^teams/(?P<url>[-\w]+)/(?P<channel>[-\w]+)', ViewTeam.as_view()),
    url(r'^teams/(?P<url>[-\w]+)', ViewTeam.as_view()),



    # home
    url(r'^', Root.as_view()),

]
