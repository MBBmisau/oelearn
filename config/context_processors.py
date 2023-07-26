from .models import SchoolSettings, SchoolAddress


def get_config_to_context(request):
    site = request.site
    try:
        settings = SchoolSettings.objects.get(site=site)
    except SchoolSettings.DoesNotExist:
        settings = None
    try:
        address = SchoolAddress.objects.get(site=site)
    except SchoolAddress.DoesNotExist:
        address = None
    if address is not None:
        social_links = address.social_links.all(),
    else:
        social_links = None
    return {
        'settings':settings,
        'address':address,
        'social_links': social_links,
    }
