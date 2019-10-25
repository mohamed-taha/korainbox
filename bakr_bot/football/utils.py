from datetime import datetime, timedelta

def competition_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/competition_<id>/<filename>
    return f'competition_{instance.id}_{filename}'


def team_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/team_<id>/<filename>
    return f'team_{instance.id}_{filename}'


def fixture_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/fixture_<id>/<filename>
    return f'fixture_{instance.id}_{filename}'


def build_fixtures_messneger_generic_message(fixtures):
    elements = []

    for fixture in fixtures:
        title = fixture.name_ar
        logo_url = fixture.competition.logo_thumbnail.url  # TODO: Replace by img of the 2 teams and watermark
        subtitle = (datetime.combine(fixture.event_date, fixture.event_time) + timedelta(hours=2)).strftime("%Y-%m-%d  %H:%M")

        # TODO: Add follow/unfollow buttons
        element = {
            "title": title,
            "image_url": logo_url,
            "subtitle": subtitle
        }

        elements.append(element)

    matches_schedule_message = {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements
            }
        }
    }
    
    return matches_schedule_message
