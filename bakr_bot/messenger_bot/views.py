import json
import logging
from pprint import pprint

from django.conf import settings
from django.contrib.sites.models import Site
from django.http.response import HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from pymessenger.bot import Bot

from bakr_bot.football.models import League, LeagueUserMembership
from bakr_bot.messenger_bot import constants
from bakr_bot.messenger_bot.utils import get_supported_leagues_message, get_user_info
from bakr_bot.users.models import User

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

                    bot.send_text_message(sender_id, 'Hey :D')

                # Hanle PostBack messages
                if 'postback' in message:
                    postback_payload = json.loads(message['postback']['payload'])
  
                    # Handle User clicked `Get Started` button
                    if postback_payload['action'] == 'get_started_button':
                        try:
                            user = User.objects.get(facebook_psid=sender_id)
                            first_name = user.first_name
                        except User.DoesNotExist:
                            logger.info("[Get Started button]: User {} not found".format(sender_id))
                            user_info = get_user_info(sender_id)
                            first_name = '' if user_info is None else user_info.get('first_name')
                        finally:

                            bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_0.format(first_name=first_name))
                            bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_1)
                            bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_2)
                            bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_3)

                            bot.send_text_message(sender_id, constants.WELCOME_MESSAGE_4)
                            site_domain = current_site.domain
                            supported_leagues_message = get_supported_leagues_message(sender_id, site_domain)

                            bot.send_message(sender_id, supported_leagues_message)

                    # Hanlde User clicked `Follow` League button
                    if(postback_payload['action'] == 'follow'
                        and postback_payload['item']['type'] == 'league'):
                        user, _ = User.objects.get_or_create(facebook_psid=sender_id)
                        try:
                            league = League.objects.get(pk=postback_payload['item']['id'])
                            _, created = LeagueUserMembership.objects.get_or_create(
                                user=user, league=league)

                            if created:
                                bot.send_text_message(
                                    sender_id, constants.FOLLOW_LEAGUE_SUCCESS_MESSAGE.format(
                                        league_name=league.name_ar + ' - ' + league.name))
                            else:
                                bot.send_text_message(
                                    sender_id, constants.FOLLOW_LEAGUE_ALREADY_FOLLOWING_MESSAGE.format(
                                        league_name=league.name_ar + ' - ' + league.name))
                        except League.DoesNotExist:
                            logger.warning(
                                "[Follow League]: League {} not found!".format(postback_payload["item"]["id"]))
                    
                    # Hanlde User clicked `UnFollow` League button
                    if(postback_payload['action'] == 'unfollow'
                        and postback_payload['item']['type'] == 'league'):
                        user, _ = User.objects.get_or_create(facebook_psid=sender_id)
                        try:
                            league = League.objects.get(pk=postback_payload['item']['id'])
                            league_user_membership = LeagueUserMembership.objects.get(
                                user=user, league=league)

                            league_user_membership.delete()
                            bot.send_text_message(
                                sender_id, constants.UNFOLLOW_LEAGUE_SUCCESS_MESSAGE.format(
                                    league_name=league.name_ar + ' - ' + league.name))
                        except League.DoesNotExist:
                            logger.warning(
                                "[UnFollow League]: League {} not found!".format(postback_payload["item"]["id"]))
                        except LeagueUserMembership.DoesNotExist:
                            logger.warning(
                                "[UnFollow League]: League-User-Membership for league {} and user {} not found!".format(
                                    postback_payload["item"]["id"], sender_id))

        return HttpResponse("success", status=200)
