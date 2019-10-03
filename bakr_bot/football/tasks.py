import logging

from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(max_retries=5)
def get_supported_competitions_matches():
    """Get supported competitions' matches from extrernal API
    and save them in Database.
    """
    # TODO: get all supported competitions

    # TODO: get matches for each competition from the API

    # TODO: save the matches to the database

    # TODO: schedule a task for eahc user to notify him on his time

    logger.info("Get matches success")
