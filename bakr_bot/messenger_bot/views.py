import json
import logging
from pprint import pprint

from django.conf import settings
from django.http.response import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from pymessenger.bot import Bot

from bakr_bot.football.models import Competition, CompetitionUserMembership
from bakr_bot.messenger_bot import constants
from bakr_bot.messenger_bot.utils import get_supported_competitions_message, get_user_info
from bakr_bot.users.models import User

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
        incoming_message = json.loads(self.request.body.decode('utf-8'))

        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                sender_id = message['sender']['id']
                pprint(message)

                # Hanlde text messages
                if 'message' in message:
                    if 'هاي' in message['message']['text']:
                        bot.send_text_message(sender_id, 'هاي :D')
                    else:  # Hanlde Unknown Messages
                        # bot.send_action(sender_id, 'typing_on')
                        bot.send_text_message(sender_id, constants.REPLY_TO_UNKNOWN_MESSAGE_0)
                        # TODO: Replace with dynamic generated buuton list
                        bot.send_text_message(sender_id, constants.REPLY_TO_UNKNOWN_MESSAGE_1)

                # Hanle PostBack messages
                if 'postback' in message:
                    postback_payload = json.loads(message['postback']['payload'])
  
                    # Handle User clicked `Get Started` button
                    if postback_payload['action'] == 'get_started_button':
                        try:
                            user = User.objects.get(facebook_psid=sender_id)
                            first_name = user.first_name
                        except User.DoesNotExist:
                            logger.info("[Get Started button]: User %s not found", str(sender_id))
                            user_info = get_user_info(sender_id)
                            first_name = '' if user_info is None else user_info.get('first_name')
                        finally:

                            bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_0.format(first_name=first_name))
                            bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_1)
                            bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_2)
                            bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_3)

                            bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_4)

                            supported_competitions_message = get_supported_competitions_message(sender_id)
                            bot.send_message(sender_id, supported_competitions_message)

                    # Hanlde User clicked `Follow` Competition button
                    if(postback_payload['action'] == 'follow'
                        and postback_payload['item']['type'] == 'competition'):
                        user, _ = User.objects.get_or_create(facebook_psid=sender_id)
                        try:
                            competition = Competition.objects.get(pk=postback_payload['item']['id'])
                            _, created = CompetitionUserMembership.objects.get_or_create(
                                user=user, competition=competition)

                            if created:
                                bot.send_text_message(
                                    sender_id, constants.FOLLOW_COMPETITION_SUCCESS_MESSAGE.format(
                                        competition_name=competition.name_ar + ' - ' + competition.name))
                            else:
                                bot.send_text_message(
                                    sender_id, constants.FOLLOW_COMPETITION_ALREADY_FOLLOWING_MESSAGE.format(
                                        competition_name=competition.name_ar + ' - ' + competition.name))
                        except Competition.DoesNotExist:
                            logger.warning(
                                "[Follow Competition]: Competition {} not found!".format(postback_payload["item"]["id"]))
                    
                    # Hanlde User clicked `UnFollow` Competition button
                    if(postback_payload['action'] == 'unfollow'
                        and postback_payload['item']['type'] == 'competition'):
                        user, _ = User.objects.get_or_create(facebook_psid=sender_id)
                        try:
                            competition = Competition.objects.get(pk=postback_payload['item']['id'])
                            competition_user_membership = CompetitionUserMembership.objects.get(
                                user=user, competition=competition)

                            competition_user_membership.delete()
                            bot.send_text_message(
                                sender_id, constants.UNFOLLOW_COMPETITION_SUCCESS_MESSAGE.format(
                                    competition_name=competition.name_ar + ' - ' + competition.name))
                        except Competition.DoesNotExist:
                            logger.warning(
                                "[UnFollow Competition]: Competition {} not found!".format(postback_payload["item"]["id"]))
                        except CompetitionUserMembership.DoesNotExist:
                            logger.warning(
                                "[UnFollow Competition]: Competition-User-Membership for competition {} and user {} not found!".format(
                                    postback_payload["item"]["id"], sender_id))

        return HttpResponse("success", status=200)
