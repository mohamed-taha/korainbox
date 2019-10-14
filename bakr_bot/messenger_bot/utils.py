import json
import requests
from django.conf import settings

from bakr_bot.football.models import Competition, CompetitionUserMembership
from bakr_bot.users.tasks import create_user
from bakr_bot.users.models import User


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


def get_reply_to_text_message(message: dict) -> dict:
    """Handle a text message sent by user and return a reply.

    Args:
        - message: message body sent by FaceBook.

    Returns:
        - reply: the reply message object which might hold a text or generic msg.
    """
    # TODO: check if message has `nlp` key
        # TODO: check if it has entity `ok` ->  return text reply

        # TODO check if has entity `thanking` -> return text reply

        # TODO: check entity `scheduleInquiry` and `competition` ->
            # TODO: check entity `date/time` then filter the query based on it
            # else: get soonest
        # else: check `compeition` only -> ask user if he wants the schdule (default: or for now assume he wants so)
        # else: check `schduleInquiry` only -> ask user which competition he wants (default: show schdule for all competitions)
    # TODO: return constant reply for unknown messages ( TODO: should be informative like give examples of questions or list of buttons)
    pass