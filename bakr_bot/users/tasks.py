from celery import shared_task

from bakr_bot.users.models import User


@shared_task
def create_user(user_info):
    """Create a user from user_info dict.

    :param user_info(Dict): User's info object.
    """

    user, created = User.objects.update_or_create(facebook_psid=user_info['id'], defaults={
        'first_name': user_info.get('first_name'), 'last_name': user_info.get('last_name')})
