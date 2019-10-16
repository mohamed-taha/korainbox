import json
import logging
import random
import requests
from typing import List, Union
from django.conf import settings

from bakr_bot.football.models import Competition, CompetitionUserMembership
from bakr_bot.football.utils import build_fixtures_messneger_generic_message
from bakr_bot.messenger_bot import constants
from bakr_bot.users.tasks import create_user
from bakr_bot.users.models import User

logger = logging.getLogger(__name__)


def get_user_info(user_psid):
    """Return user basic info through FB Graph API.

    :params user_psid: String, User page scoped ID
    :returns Dict of 'first_name', 'last_name', 'profile_pic', 'id'
     or None
    """

    url = settings.FB_GRAPH_API_URL + user_psid + '?access_token=' + settings.FB_PAGE_ACCESS_TOKEN

    resp = requests.get(url)
    resp.raise_for_status()

    if resp.status_code == 200:
        info = resp.json()
        create_user.delay(info)
        return info
    else:
        return None


def get_supported_competitions_message(user_psid):
    """Return a facebook messenger generic message of competitions supported by KoraInbox.
    Note: You can only list up to 10 elements in a generic message.
    """
    user, _ = User.objects.get_or_create(facebook_psid=user_psid)
    supported_competitions = Competition.objects.filter(is_supported=True)[:10]
    elements = []

    for competition in supported_competitions:
        title = competition.name_ar + " - " + competition.name
        logo_url = competition.logo.url

        if CompetitionUserMembership.objects.filter(user=user, competition=competition).exists():
            payload_action = "unfollow"
            button_title = " إلغاءالمتابعة "
        else:
            payload_action = "follow"
            button_title = " متابعة "

        element = {
            "title": title,
            "image_url": logo_url,
            "subtitle": "اعرف اخر الاخبار واستقبل تنبيهات بمواعيد ونتايج الماتشات",
            "buttons":[
                {
                    "type": "postback",
                    "title": button_title,
                    "payload": json.dumps({
                        "action": payload_action,
                        "item": {
                            "type": "competition",
                            "id": competition.id
                        }
                    })
                }              
            ]      
        }
        elements.append(element)

    message = {
        "attachment":{
            "type":"template",
            "payload":{
                "template_type":"generic",
                "elements": elements
            }
        }
    }

    return message


def get_replies_to_text_message(message: dict) -> List[Union[dict, str]]:
    """Handle a text message sent by user and return a reply.

    Args:
        - message: message body sent by FaceBook.

    Returns:
        - reply: a list of either string message, dicts(generic messages) or mix of them.
    """
    if message.get('nlp') is not None and message['nlp']['entities']:
        # TODO: check entity `scheduleInquiry` and `competition` ->
            # TODO: check entity `date/time` then filter the query based on it
            # else: get soonest
        # else: check `compeition` only -> ask user if he wants the schdule (default: or for now assume he wants so)
        # else: check `schduleInquiry` only -> ask user which competition he wants (default: show schdule for all competitions)

        # Handle competition schedule inquiry
        if('intent' in message['nlp']['entities'] and
           message['nlp']['entities']['intent'][0]['value'] == 'scheduleInquiry' and
           message['nlp']['entities']['intent'][0]['confidence'] >= 0.75):
            # Check which competition  # TODO: Handle 1+ competitions inquiried at the same message
            if('competition' in message['nlp']['entities'] and
               message['nlp']['entities']['competition'][0]['metadata'] is not None and
               message['nlp']['entities']['competition'][0]['confidence'] >= 0.75):
                competition_api_id = int(message['nlp']['entities']['competition'][0]['metadata'])
                try:
                    competition = Competition.objects.get(api_id=competition_api_id)
                    nearst_10_fixtures = competition.next_30_days_fixtures()  # TODO: Enhance by return a button to list all matches

                    if nearst_10_fixtures is not None:
                        return [
                            'اوك دي ماتشات الفتره الجايه في ' + competition.name_ar,
                            build_fixtures_messneger_generic_message(nearst_10_fixtures)
                        ]
                    else:
                        return ['مافيش ماتشات الشهر ده 🤷‍♂️ 🤦🏻‍♂️']
                except Competition.DoesNotExist:
                    logger.warning("Competition with API ID %d does not exits", competition_api_id)

        # Handle `ok` sentences, ex: okay, okay, tmam, اوك
        if 'ok' in message['nlp']['entities'] and message['nlp']['entities']['ok'][0]['confidence'] >= 0.75:
            return [message['nlp']['entities']['ok'][0]['value'] + ' 👌']

        # Hanlde `thanking` messages; ex: thanks , thank you, شكرا
        if 'thanking' in message['nlp']['entities'] and message['nlp']['entities']['thanking'][0]['confidence'] >= 0.75:
            emojis = ['🤗', '☺️', '🥰', '😉', '😊']
            if message['nlp']['entities']['thanking'][0]['metadata'] == 'thanks_ar':
                return ['العفو ' + random.choice(emojis)]
            else:
                return ['You Welcome ' + random.choice(emojis)]

    # Handle Unknown messages
    # TODO: Replace with informative reply like give examples of questions or list of buttons
    return [constants.REPLY_TO_UNKNOWN_MESSAGE_0, constants.REPLY_TO_UNKNOWN_MESSAGE_1]
