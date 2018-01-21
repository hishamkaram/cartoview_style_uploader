from geonode.geoserver.helpers import ogc_server_settings, set_styles

def get_connection_params():
    username, password = ogc_server_settings.credentials
    service_url = ogc_server_settings.internal_rest
    return dict(service_url=service_url, username=username, password=password)
