import os

class Config(object):
    APP_NAME = "ShowCSE"
    ENV_SETTING_PREFIX = "SHOWCSE_"
    SECRET_KEY = 'super-secret-key'

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://showcse@127.0.0.1/showcse'
    

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
    LDAP_HOST = 'ad.unsw.edu.au:389'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@mysql/{}".format(
        os.environ.get('MYSQL_USER'),
        os.environ.get('MYSQL_PASSWORD'),
        os.environ.get('MYSQL_DATABASE'),
    )
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SENTRY_ENABLED = True
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    DEBUG = False


def get_config_class():
    import os
    config_name = os.environ.get('CONFIG_CLASS', 'Config')
    config_class = globals().get(config_name)
    if config_class is None:
        raise Exception("Configuration class '{}' could not be loaded".format(config_name))
    
    print("Using configuration class: '{}'".format(config_class.__name__))

    return config_class