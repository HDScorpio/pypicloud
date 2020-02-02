from pyramid.paster import get_app, setup_logging

# NOTE: if need custom path to config file then edit this variable
ini_path = '/etc/pypicloud/production.ini'

setup_logging(ini_path)
application = get_app(ini_path, 'main')
