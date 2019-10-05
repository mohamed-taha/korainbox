def competition_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/league_<id>/<filename>
    return f'competition_{instance.id}_{filename}'


def get_supported_competitions_message(user_psid, site_domain):
    """Return a facebook messenger generic message of a competition matches schedule.
    Note: You can only list up to 10 elements in a generic message.
    """
    user, _ = User.objects.get_or_create(facebook_psid=user_psid)
    supported_competitions = Competition.objects.filter(is_supported=True)[:10]


    return message
