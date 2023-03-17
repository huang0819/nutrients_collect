APP_NAME = 'Nutrient data collect tool'
APP_WIDTH = 1920
APP_HEIGHT = 1080

MESSAGE_HEIGHT = 300
MESSAGE_WIDTH = 600


class UI_PAGE_NAME:
    LOADING = 0
    ERROR = 1
    COLLECT = 2


class COLOR:
    MAIN = '#4D9AA8'
    MAIN_SUB = '#3b7580'
    WHITE = '#FFFFFF'
    BLACK = '#2C2C2C'
    GREY = '#D2D2D2'
    RED = '#C75450'
    GREEN = '#388836'


class Message:
    LOADING = '處理中，請稍候。'
    CAMERA_ERR = '無法使用深度攝影機，請重新確認後再開啟應用程式。'
    NET_ERR = '網路連線異常，請重新確認後再開啟應用程式。'
