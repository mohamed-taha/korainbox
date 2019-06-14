import requests
from django.conf import settings


def get_user_info(user_psid):
    """Return user basic info through FB Graph API.

    :params user_psid: String, User page scoped ID
    :returns Dict of 'first_name', 'last_name', 'profile_pic', 'id'
     or None
    """

    url = settings.FB_GRAPH_API_URL + user_psid + '?access_token=' + settings.FB_PAGE_ACCESS_TOKEN

    resp = requests.get(url)

    return resp.json() if resp.status_code == 200 else None

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