APPLICATION_PREFIX = "/api"

JWT_KEY = "14834c55af7e2ca2adda98495f6e64a2cc032cb7"

JWT_LIFETIME = 3600*24*180 #seconds

#Localhost
DATABASE_URI = "mysql+pymysql://root:123456@localhost/interrep"

#Heroku
#DATABASE_URI = "mysql+pymysql://i15wen96kq8gpz08:h00gonk9n0ysxg9o@cdm1s48crk8itlnr.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/m49pi0jo12u2bbib"

PASSWORD_MIN_LENGTH = 6

PASSWORD_MAX_LENGTH = 50

UPLOAD_FOLDER = './images'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

MAX_CONTENT_LENGTH = 2 * 1024 * 1024

PERMISSIONS_REQUIRED = {
    'CreateRepublic':['create_rep'],
    'CreatePlayer':['create_player'],
    'ModifyRepublic':['modify_rep'],
    'ModifyPlayer':['modify_player'],
    'DeleteRepublic':['delete_rep'],
    'DeletePlayer':['delete_player'],
    'ToggleMarket':['toggle_market'],
    'SetDeadline':['toggle_market'],
    'ModifyPlayerValue':['modify_player'],
    'CreateMatch':['create_match'],
    'UpdateMatch':['update_match'],
    'DeleteMatch':['delete_match']
    }
