from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User

from django.contrib.auth.models import User


class Root(View):

    template = 'index.html'

    def get(self, request):

        context = {
            'title':'Home'
        }


        return render(request, self.template, context)


class Register(View):

    template = ''

    def post(self, request):

        username, password = request.POST.get('email'), request.POST.get('password')


        if username and password and not User.objects.filter(username=username):

            self.template = 'register.html'

            context = {
                'title' : 'Register'
            }

            #user = User.objects.create_user(username, username, password)



            return render(request, self.template, context)


        else:
            return HttpResponse('error')


