def competition_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/league_<id>/<filename>
    return f'competition_{instance.id}_{filename}'


def build_fixtures_messneger_generic_message(fixtures):
    elements = []

    for fixture in fixtures:
        title = fixture.name_ar
        logo_url = fixture.competition.logo.url  # TODO: Replace by img of the 2 teams and watermark
        subtitle = str(fixture.event_date) + " \t " + str(fixture.event_time)  # FIXME: localize the date and time

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
