import json
import requests
from django.conf import settings

from bakr_bot.football.models import League, LeagueUserMembership
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

    if resp.status_code == 200:
        info = resp.json()
        create_user.delay(info)
        return info
    else:
        return None


def get_supported_leagues_message(user_psid, site_domain):
    """Return a facebook messenger generic message ofleagues supported by KoraInbox.
    Note: You can only list up to 10 elements in a generic message.
    """
    user, _ = User.objects.get_or_create(facebook_psid=user_psid)
    supported_leagues = League.objects.filter(is_supported=True)[:10]
    elements = []

    for league in supported_leagues:
        title = league.name_ar + " - " + league.name
        logo_url = site_domain + league.logo.url

        if LeagueUserMembership.objects.filter(user=user, league=league).exists():
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
                    # "payload": f"{payload_action}_LEAGUE_{league.id}"
                    "payload": json.dumps({
                        "action": payload_action,
                        "item": {
                            "type": "league",
                            "id": league.id
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


#
#  url = 'http://livescore-api.com/api-client/leagues/table.json?key=v4dX5KXYsyjpifce&secret=kpDPNBRC3oNuYXJu2Wr8Hp69YpyhELvZ&league={league_id}&season=
#    ...: {season}' 
# In [31]: for league in League.objects.all()[:5]: 
#     ...:     resp = requests.get(url.format(league_id=league.livescore_id, season=2)).json() 
#     ...:     print(resp.get('data').get('table') if resp.get('data') else 'No data for league #{}: {} - {}'.format(league.livescore_id, league.country.name, 
#     ...: league.name)) 
#     ...:     table = resp.get('data').get('table') if resp.get('data') else None 
#     ...:     if table: 
#     ...:         for standing in table: 
#     ...:             Team.objects.get_or_create(league=league, name=standing['name'], livescore_league_id=['league_id'], livescore_id=standing['team_id'])     
