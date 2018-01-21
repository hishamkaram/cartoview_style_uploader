from geonode.layers.models import Style
from django.shortcuts import render
from geoserver.catalog import Catalog
import os
from .forms import StyleUploadForm
from .helpers import get_connection_params
import logging
import time
from sys import stdout
formatter = logging.Formatter(
    '[%(asctime)s] p%(process)s  { %(name)s %(pathname)s:%(lineno)d} \
                            %(levelname)s - %(message)s', '%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)


class Cartoview_style_uploader(object):
    def __init__(self):
        geoserver_info = get_connection_params()
        self.gs_catalog = Catalog(**geoserver_info)

    def get_new_style_name(self, sld_name):
        style = self.gs_catalog.get_style(sld_name)
        if not style:
            return sld_name
        else:
            timestr = time.strftime("%Y%m%d_%H%M%S")
            return "{}_{}".format(sld_name, timestr)

    def gs_upload_save(self, slds):
        for sld in slds:
            name, ext = os.path.splitext(sld.name)
            style_name = self.get_new_style_name(name)
            sld_body = sld.read()
            self.gs_catalog.create_style(style_name, sld_body, True)
            style = self.gs_catalog.get_style(style_name)
            style_url = style._build_href(ext, create=False)
            Style.objects.create(
                name=style_name, sld_title=style_name, sld_body=sld_body,
                sld_url=style_url)

    def upload_style(self, request):
        form = StyleUploadForm()
        if request.method == "POST":
            form = StyleUploadForm(request.POST or None, request.FILES or None)
            slds = request.FILES.getlist('styles')
            if form.is_valid():
                self.gs_upload_save(slds)
        context = {'form': form}
        return render(request,
                      template_name='cartoview_style_uploader/index.html',
                      context=context)


style_uploader = Cartoview_style_uploader()
