import os
from urllib.parse import urlparse

class Config(object):
    APP_NAME = "ShowCSE"
    ENV_SETTING_PREFIX = "SHOWCSE_"
    SECRET_KEY = 'super-secret-key'

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@127.0.0.1/showcse?charset=utf8mb4'
    SQLALCHEMY_POOL_RECYCLE = 60 * 10  # 10 Minutes Pool Recycle.

    UPLOADED_FILES_DEST = 'Application/static/uploads'
    UPLOADED_FILES_URL = '/static/'

    LDAP_HOST = '127.0.0.1:1389'
    LDAP_BASE_DN = 'OU=IDM,DC=ad,DC=unsw,DC=edu,DC=au'
    LDAP_USER_DN = 'OU=IDM_People'
    LDAP_BIND_DIRECT_CREDENTIALS = True
    LDAP_BIND_DIRECT_SUFFIX = "@ad.unsw.edu.au"
    LDAP_BIND_DIRECT_GET_USER_INFO = True
    LDAP_USER_SEARCH_SCOPE = "SEARCH_SCOPE_WHOLE_SUBTREE"
    LDAP_USER_LOGIN_ATTR = 'cn'
    LDAP_GET_USER_ATTRIBUTES = ['dn', 'cn', 'memberOf', 'givenName', 'sn']

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class Production(Config):
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = build_url(
            os.environ['DATABASE_URL'], 
            scheme='mysql+pymysql') + '?charset=utf8mb4'
        self.SECRET_KEY = os.environ['SECRET_KEY']
        self.SENTRY_DSN = os.environ.get('SENTRY_DSN')

    LDAP_HOST = 'ad.unsw.edu.au:389'
    SENTRY_ENABLED = True
    DEBUG = False


def get_config_class():
    import os
    config_name = os.environ.get('CONFIG_CLASS', 'Config')
    config_class = globals().get(config_name)
    if config_class is None:
        raise Exception("Configuration class '{}' could not be loaded".format(config_name))
    
    print("Using configuration class: '{}'".format(config_class.__name__))

    return config_class

def build_url(url, scheme=None, username=None, password=None, hostname=None, 
              port=None, path=None):
    dsn = urlparse(url)

    if scheme is None: 
        scheme = dsn.scheme
    if username is None: 
        username = dsn.username
    if password is None: 
        password = dsn.password
    if hostname is None: 
        hostname = dsn.hostname
    if port is None: 
        port = dsn.port
    if path is None: 
        path = dsn.path

    def build_auth():
        if username is not None or password is not None:
            return '{}:{}@'.format(username or '', password or '')
        return ''

    def build_port():
        if port is not None:
            return ':{}'.format(port)
        return ''

    return '{scheme}://{auth}{hostname}{port}{path}'.format(
        scheme=scheme,
        auth=build_auth(),
        hostname=hostname or '',
        port=build_port(),
        path=path
    )
