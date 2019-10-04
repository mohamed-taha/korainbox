import logging
from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from bakr_bot.football.models import Competition

logger = logging.getLogger(__name__)


@shared_task(max_retries=5)
def get_supported_competitions_today_matches():
    """Get supported competitions' matches from extrernal API
    and save them in Database.
    """
    logger.info("Started getting today matches for supported competitions")

    # Get matches for each upooprted competition from the API
    supported_competitions = Competition.objects.filter(is_supported=True)
    now = timezone.now()

    for competition in supported_competitions:
        competition.update_fixtures(date=now.date().strftime('%Y-%m-%d'))

        competition_today_fixtures = competition.fixtures.filter(event_date=now.date()).exists()

        if competition_today_fixtures:
            logger.info("Scheduling today matches for competition {}".format(competition.name))
            # Schedule a task for ech comptetion follower to notify him on his time
            for user in competition.followers.all():
                send_user_competition_today_matches.apply_aync(
                    (user.id, competition.id,), eta=now + timedelta(hours=8)
                )  # Notify user on 8 AM server time(UTC); 10 AM Egypt time;
        else:
            logger.info("No matches today {} for competition {}".format(
                now.date().strftime('%Y-%m-%d'), competition.name))


@shared_task(max_retries=3)
def send_user_competition_today_matches(user_id, compeition_id):
    pass