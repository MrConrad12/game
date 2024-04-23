HEIGHT = 700
WIDTH = 1280
ACC = 0.5
FRIC = -0.12
FPS = 60
START_MENU = 'start_menu'
GAME = 'game'
LEVEL = 'level'
GRAVITY = 0.8
LEVEL_SELECT = "level_select"
CARD_SIZE = 240
EFFECT_SOUND = "../assets/raw/event_effects/"
BGM_PATH = "../assets/raw/background_music/"
FONT_PATH = "assets/font/LilitaOne-Regular.ttf"
SELECTABLE_PLAYER_POS_X = WIDTH * 6/8 + 50
SELECTABLE_PLAYER_POS_Y = HEIGHT / 4
BUTTON_PATH = "assets/bouton/"
ITEM_PATH = "assets/items/"
PLAYER_DATA = {
    'player1':{
        'lives': 3,
        'damage': 3,
        'speed': 1,
        'jump': 10,
        'aptitude': 'None'
    },
    'player2':{
        'lives': 3,
        'damage': 4,
        'jump': 15,
        'speed': 2,
        'aptitude': 'double_jump'
    },
    'player3':{
        'lives' : 3,
        'damage' : 2,
        'jump': 15,
        'speed': 3,
        'aptitude': 'sprint'
    },
    'player4':{
        'lives' : 4,
        'damage' : 3,
        'jump': 18,
        'speed': 1,
        'aptitude': 'swim'
    }
}