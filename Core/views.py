from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from .models import Profile, Teams, Channels, ChannelLogs
from random import randint
from Tong.utils import utils
import json


class Root(View):

    template = 'index.html'

    def get(self, request):

        context = {
            'title':'Home'
        }

        if request.user.is_authenticated:
            return redirect('/profile')


        return render(request, self.template, context)

class Register(View):

    template = ''

    def get(self, request):
        return redirect('/')


    def post(self, request):


        input_params = {

            'username':request.POST.get('email'),
            'password':request.POST.get('password'),
            'displayname':request.POST.get('displayname')

        }

        if input_params['username'] and input_params['password']\
            and not User.objects.filter(email=input_params['username']):


            self.template = 'register.html'

            context = {
                'title' : 'Register'
            }

            user = User.objects.create_user(input_params['username'],
                                            input_params['username'],
                                            input_params['password'])

            login(request, user)

            return render(request, self.template, context)


        elif input_params['displayname']:

            request.user.profile.displayname = input_params['displayname']

            request.user.profile.url = '{}-{}'.format(utils.stripforurl(input_params['displayname']),
                                                      randint(10000,20000))

            request.user.save()

            return redirect('/users/{}'.format(request.user.profile.url))


        else:
            return redirect('/signin')

class Signin(View):

    template = 'signin.html'

    def get(self, request):

        return render(request, self.template)



    def post(self, request):

        input_params = {

            'username': request.POST.get('email'),
            'password' : request.POST.get('password')

        }

        user = authenticate(username=input_params['username'],
                            password=input_params['password'])

        if user and user.is_active:
            login(request, user)
            return redirect('/profile')

        else:
            return redirect('/signin')

class Signout(View):
    template = ''

    def get(self, request):
        logout(request)
        return redirect('/')

class ProfileView(View):

    template ='profile.html'

    def get(self,request):

        teams = Teams.objects.filter(owner=request.user)

        context = {
            'title' : 'Home',
            'teams' : teams
        }

        return render(request, self.template, context)

class CreateTeam(View):

    def post(self, request):

        input_params = {
            'teamname' : request.POST.get('teamname')
        }

        url_name = utils.stripforurl(input_params['teamname'])
        url_number = randint(20001, 30000)

        team_params = {
            'owner' : request.user,
            'displayname' : input_params['teamname'],
            'url' : '{}-{}'.format(url_name,url_number)
        }

        team = Teams.objects.create(**team_params)

        channel_params = [
            {
                'team':team,
                'displayname' : 'Public',
                'url' : 'public'

            },
            {
                'team':team,
                'displayname' : 'Admin',
                'url': 'admin'
            },
            {
                'team': team,
                'displayname': 'Fun',
                'url': 'fun'
            },

        ]

        for channel in channel_params:
            Channels.objects.create(**channel)


        return redirect('/')

class ViewTeam(View):

    template = 'teamview.html'

    def get(self, request, url=None, channel=None):

        team = Teams.objects.get(url=url)
        channels = Channels.objects.filter(team=team)
        current_channel = Channels.objects.get(team=team,url=channel)
        history = ChannelLogs.objects.filter(channel=current_channel)

        data_params = {
            'team': {
                'name' : team.displayname,
                'url': team.url,
            },
            'channel' : {
                'name' : current_channel.displayname,
                'url' : current_channel.url,
                'history' : {}
            }
        }

        for message in history:
            data_params['channel']['history'][message.id] = {
                'user': {
                    'displayname' : message.user.profile.displayname,
                    'url' : message.user.profile.url,
                },
                'data': message.message,
                'created': str(message.created),
            }

        context = {
            'title': team.displayname,
            'team' : team,
            'channels':channels,
            'data': json.dumps(data_params)
        }

        return render(request,self.template,context)

