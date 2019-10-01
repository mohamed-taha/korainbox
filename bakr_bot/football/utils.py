def league_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/league_<id>/<filename>
    return f'league_{instance.id}_{filename}'