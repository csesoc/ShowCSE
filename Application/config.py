class Config(object):
    APP_NAME = "ShowCSE"
    MONGOALCHEMY_DATABASE = "webskale"
    SECRET_KEY = 'SUPER SECRET KEY'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://webskale@127.0.0.1/webskale'
    

    UPLOADED_FILES_DEST = 'Application/static/uploads'
    UPLOADED_FILES_URL = '/static/'
    


