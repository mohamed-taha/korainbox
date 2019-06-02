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