import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(max_retries=5)
def get_supported_leagues_matches():
    """Get supported leagues' matches from extrernal API
    and save them in Database.
    """
    # TODO: get all supported leagues

    # TODO: get matches for each league from the API

    # TODO: save the matches to the league

    logger.info("Get matches success")
