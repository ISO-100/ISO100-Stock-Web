#This is a sample file ,please change the name to setting.py in production env.
SECRET_KEY ='xxx' 
DEBUG = True
DB_USERNAME = 'sample'
DB_PASSWORD = 'sample'
BLOG_DATABASE_NAME = 'sample'
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@localhost:3306/%s' % (DB_USERNAME, DB_PASSWORD,BLOG_DATABASE_NAME)

