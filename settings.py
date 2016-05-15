SECRET_KEY = '\x10\x1a^\xdf\xb8R}z\xce\xb4\x83\xb9b\x13\xd3]\x9a\x11\x12\x17\xb6\x05\xaf\xdb'
DEBUG = True
DB_USERNAME = 'teaguexiao'
DB_PASSWORD = ''
BLOG_DATABASE_NAME = 'blog'
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@localhost:3306/%s' % (DB_USERNAME, DB_PASSWORD,BLOG_DATABASE_NAME)

