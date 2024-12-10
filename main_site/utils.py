def get_site_url():
    from django.contrib.sites.models import Site

    scheme = "http"
    domain = Site.objects.get_current().domain
    return "{}://{}".format(scheme, domain)
