from main_site.models import SiteSettings


def get_site_settings(request):
    settings = SiteSettings.objects.first()
    all_cells = False
    if settings:
        all_cells = all([settings.homepage_cell_6, settings.homepage_cell_5, settings.homepage_cell_4, settings.homepage_cell_3, settings.homepage_cell_2, settings.homepage_cell_1])
    return {
        "settings": settings,
        "all_cells": all_cells,
    }
