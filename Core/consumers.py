import json
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from .models import ChannelLogs, Channels, Teams



@channel_session_user_from_http
def ws_connect(message):

    if message.user.is_authenticated:

        # accept connection
        message.reply_channel.send({'accept':True})
        Group('system').add(message.reply_channel)

        a,team,channel = message['path'].split('/')
        Group('{}-{}'.format(team,channel)).add(message.reply_channel)



@channel_session_user
def ws_disconnect(message):

    pass



@channel_session_user
def ws_receive(message):


    if message.user.is_authenticated:

        a, team, channel = message['path'].split('/')
        payload = json.loads(message['text'])

        types = ['text']

        current_team = Teams.objects.get(url=team)
        current_channel = Channels.objects.get(team=current_team, url=channel)



        if payload['message']['type'] in types:
            params = {
                'channel' : current_channel,
                'user' : message.user,
                'message': payload['message']['data']
            }

            entry = ChannelLogs(**params)
            entry.save()



            tx_data = {
                'type' : 'text',
                'id' : entry.id,
                'created' : str(entry.created),
                'data' : entry.message,
                'user' : {
                    'id' : message.user.id,
                    'displayname' : message.user.profile.displayname
                }

            }



            tx_param = {
                'text': json.dumps(tx_data)
            }

            print(tx_param['text'])

            Group('{}-{}'.format(team, channel)).send(tx_param)













