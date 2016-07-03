import os

threads=4
bind = '0.0.0.0:{}'.format(os.environ.get('PORT', '5000'))
accesslog =  '-'
errorlog = '-'
loglevel = 'warning'
