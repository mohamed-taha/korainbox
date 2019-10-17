import logging
from datetime import timedelta


from celery import shared_task
from django.conf import settings
from django.contrib.sites.models import Site
from django.utils import timezone
from django.template.defaultfilters import time as _time
from pymessenger.bot import Bot

from bakr_bot.football.models import Competition
from bakr_bot.users.models import User
from bakr_bot.football import constants
from bakr_bot.football.utils import build_fixtures_messneger_generic_message

logger = logging.getLogger(__name__)
current_site = Site.objects.get_current()
bot = Bot(settings.FB_PAGE_ACCESS_TOKEN)


@shared_task(max_retries=5)
def fetch_and_save_supported_competitions_fixtures():
    """Get supported competitions' matches from extrernal API
    and save them in Database.
    """
    logger.info("Started fetching supported competitions' fixtures")

    # Get matches for each supported competition from the API
    supported_competitions = Competition.objects.filter(is_supported=True)
    now = timezone.now()

    for competition in supported_competitions:
        competition.fetch_and_update_fixtures()

        competition_today_fixtures = competition.fixtures.filter(event_date=now.date()).exists()

        # TODO: Refactor to send all user followed competitions matches in 1 message
        # TODO: Avoid FB rate limits by braodcasting or distribute the messageing time.
        if competition_today_fixtures:
            logger.info("Scheduling today matches for competition %s", competition.name)
            # Schedule a task for ech comptetion follower to notify him on his time
            for user in competition.followers.all():
                send_user_competition_today_matches.apply_async(
                    (user.id, competition.id,), eta=now + timedelta(hours=8)
                )  # Notify user on 8 AM server time(UTC); 10 AM Egypt time;
        else:
            logger.info("No matches today %s for competition %s",
                        now.date().strftime('%Y-%m-%d'), competition.name)


@shared_task(max_retries=3)
def send_user_competition_today_matches(user_id, competition_id):
    try:
        user = User.objects.get(pk=user_id)
        comp = Competition.objects.get(pk=competition_id)
        now = timezone.now()

        comp_today_matches = comp.fixtures.filter(event_date=now.date())

        if comp_today_matches.exists():

            matches_schedule_message = build_fixtures_messneger_generic_message(comp_today_matches)

            bot.send_text_message(
                user.facebook_psid,
                constants.USER_COMPETITION_MATCHES_SCHEDULE_MESSAGE_0.format(
                    first_name=user.first_name, competition_name=comp.name_ar)
            )
            bot.send_message(user.facebook_psid, matches_schedule_message)
            logger.info("Competition %s today %s matches schedule successfully sent to user %d",
                        comp.name, now.date().strftime('%Y-%m-%d'), user.id)
        else:
            logger.warning("No matches today %s for competition %s",
                           now.date().strftime('%Y-%m-%d'), comp.name)
    except User.DoesNotExist:
        logger.warning("User with ID %d not found in DB", user_id)
    except Competition.DoesNotExist:
        logger.warning("Competition with ID %d not found in DB", competition_id)
