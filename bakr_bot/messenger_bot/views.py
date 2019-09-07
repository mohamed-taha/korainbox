import json
import logging
from pprint import pprint

from django.conf import settings
from django.http.response import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from pymessenger.bot import Bot

from bakr_bot.messenger_bot import constants
from bakr_bot.messenger_bot.utils import get_user_info

logger = logging.getLogger(__name__)

bot = Bot(settings.FB_PAGE_ACCESS_TOKEN)

class MessengerBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == '123456789':
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Converts the text payload into a python dictionary
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        # Facebook recommends going through every entry since they might send
        # multiple messages in a single call during high load
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                # Check to make sure the received call is a message call
                # This might be delivery, optin, postback for other events 
                if 'message' in message:
                    # Print the message to the terminal
                    pprint(message)
                    bot.send_text_message(message['sender']['id'], 'Hey :D')
                if 'postback' in message:
                    print('post back')
                    user_info = get_user_info(message['sender']['id'])
                    print(user_info)

                    if user_info is not None:
                        bot.send_text_message(message['sender']['id'], constants.WELCOME_MESSAGE_0.format(first_name=user_info.get('first_name')))
                    else:
                        bot.send_text_message(message['sender']['id'], constants.WELCOME_MESSAGE_0.format(first_name=''))
                    bot.send_text_message(message['sender']['id'], constants.WELCOME_MESSAGE_1)
                    bot.send_text_message(message['sender']['id'], constants.WELCOME_MESSAGE_2)
                    bot.send_text_message(message['sender']['id'], constants.WELCOME_MESSAGE_3)
        return HttpResponse()
