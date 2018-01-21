from .views import style_uploader
from . import APP_NAME
from django.conf.urls import url, patterns
urlpatterns = patterns('',
                       url(r'^$', style_uploader.upload_style,
                           name="%s.index" % (APP_NAME)),
                       )
