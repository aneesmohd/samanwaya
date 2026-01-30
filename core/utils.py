from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import os
from django.conf import settings
from django.contrib.staticfiles import finders

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    sUrl = settings.STATIC_URL        # Typically /static/
    mUrl = settings.MEDIA_URL         # Typically /media/
    
    # Check if the URI starts with STATIC_URL or MEDIA_URL and strip it
    if uri.startswith(mUrl):
        path = os.path.join(settings.MEDIA_ROOT, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        # Allow for finding static files using Django finders
        path = uri.replace(sUrl, "")
        path = finders.find(path)
    else:
        return uri  # handle absolute paths or other cases

    # make sure that file exists
    if not path or not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result, link_callback=link_callback)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
