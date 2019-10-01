import json
import logging
from pprint import pprint

from django.contrib.sites.models import Site
from django.conf import settings
from django.http.response import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from pymessenger.bot import Bot

from bakr_bot.messenger_bot import constants
from bakr_bot.messenger_bot.utils import get_user_info, get_supported_leagues_message

logger = logging.getLogger(__name__)
current_site = Site.objects.get_current()
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
        incoming_message = json.loads(self.request.body.decode('utf-8'))

        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                sender_id = message['sender']['id']
                pprint(message)

                # Hanlde text messages
                if 'message' in message:

                    # bot.send_text_message(sender_id, 'Hey :D')

                    # Select leagues to follow
                    # TODO: move under `Get Started` handling
                    bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_4)
                    site_domain = current_site.domain
                    supported_leagues_message = get_supported_leagues_message(sender_id, site_domain)

                    bot.send_message(sender_id, supported_leagues_message)

                # Hanle PostBack messages
                if 'postback' in message:  # FIXME: this somehow is not working
                    user_info = get_user_info(sender_id)
                    postback_payload = json.loads(message['postback']['payload'])

                    # Handle User clicked `Get Started` button
                    if postback_payload['action'] == 'get_started_button':
                        if user_info is not None:
                            bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_0.format(
                                first_name=user_info.get('first_name')))
                        else:
                            bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_0.format(first_name=''))
                        bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_1)
                        bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_2)
                        bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_3)

                    # Hanlde User clicked `Follow` League button
                    if(postback_payload['action'] == 'follow'
                       and postback_payload['item']['type'] == 'league'):
                        # TODO: > Get or create user > Get league > Create membership relation (Async(task)?)
                        # TODO: > Respond to user "تمت المتابعه بنجاح هابعتلك كل يوم فيه ماتشات بلا بلا بلا"
                        pass

        return "success"
