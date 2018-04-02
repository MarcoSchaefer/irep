APPLICATION_PREFIX = "/api"

JWT_KEY = "14834c55af7e2ca2adda98495f6e64a2cc032cb7"

JWT_LIFETIME = 3600*6 #seconds

DATABASE_URI = "mysql+pymysql://root:123890q@localhost/interrep"

PASSWORD_MIN_LENGTH = 6

PASSWORD_MAX_LENGTH = 50

UPLOAD_FOLDER = './images'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

MAX_CONTENT_LENGTH = 2 * 1024 * 1024
