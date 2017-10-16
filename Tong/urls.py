from django.conf.urls import url
from django.contrib import admin
from Core.views import Root, Register

urlpatterns = [
    url(r'^admin/', admin.site.urls),


    # register
    url(r'^register', Register.as_view()),

    # sign in
    # url(r'^signin', Signin.as_view()),


    # home
    url(r'^', Root.as_view()),

]
