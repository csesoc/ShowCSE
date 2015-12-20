class Config(object):
    APP_NAME = "ShowCSE"
    MONGOALCHEMY_DATABASE = "webskale"
    SECRET_KEY = 'SUPER SECRET KEY'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://webskale@127.0.0.1/webskale'
    

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