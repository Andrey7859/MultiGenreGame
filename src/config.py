import enum, logging

class UIEnum(enum.Enum):
    Main_menu = 0
    Inform = 1
    Settings = 2
    Pause = 3
    Game = 4
    GameOver = 5

class EventsEnum(enum.Enum):
    movement = 0
    jump = 1
    achievement = 2
    collectCoin = 3

class LevelEnum(enum.Enum):
    Strategy = 0
    Shooter = 1
    Platformer = 2

class TileEnum(enum.Enum):
    _None = 0
    Door = 1
    Chest = 2
    Coin = 3
    Portal = 4
    Enemies = 5
    Buff = 6

gameState = UIEnum.Main_menu.value
prev_gameState = gameState
currentLevel = LevelEnum.Platformer.value

savedValues = {}

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    formatter = logging.Formatter('%(levelname)s %(message)s')
    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

DebugLogger = setup_logger('DEBUG', 'logs/DebugLogs.log', logging.DEBUG)
InfoLogger = setup_logger('INFO', 'logs/InfoLogs.log', logging.INFO)
WarningLogger = setup_logger('WARNING', 'logs/WarningLogs.log', logging.WARNING)
CriticalLogger = setup_logger('CRITICAL', 'logs/CriticalLogs.log', logging.CRITICAL)

# logging.basicConfig(level= logging.DEBUG, filename= "logs/logs.log", filemode= "w")

TILE_SIZE = 32
WIDTH, HEIGHT = 1280, 720
FPS = 60                        # limits FPS to 60
SPEED_SCALE = 30
FONT_SIZE = 16
OFFSET = 10
SOUND_PLAYING_DELAY = 30 

CAMERA_BORDERS = {
	'left': 200,
	'right': 400,
	'top':100,
	'bottom': 150
}

curr_window_width = WIDTH
curr_window_height = HEIGHT
