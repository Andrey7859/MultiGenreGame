import pygame, pygame_gui, json, threading
import config 

from observer import *
from command import *
from assetManager import *

from player import *
from level import *

class Game():
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        pygame.mixer.set_num_channels(64)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.settings = {}
        self.controls = {}
        self.parceJSON()
        logging.info("Game was started")

# Load all resources
        self.assetMngr = AssetManager('media')
        # self.assetMngr.loadImages()
        self.assetMngr.loadSounds()
        # self.assetMngr.loadFonts()

        self.publisher = Subject()
        self.publisher.addObserver(Audio(self.assetMngr))

        self.running = True
        self.speed = 7
        self.dt = 0                 # delta time in seconds since last frame
        self.isLevelInit = False
        # self.currentLevel = config.LevelEnum.Strategy.value
        self.currentLevel = 0

        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))

        self.createUIWidgets()
        threading.Thread(target=self.playBgMusic).start()

    def loadProgress(self):
        with open("configs/savefile.txt", "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                tmp = line.split(' = ')
                savedValues[tmp[0]] = tmp[1]
    
    def saveProgress(self):
        with open("configs/savefile.txt", "w") as f:
            for i in savedValues:
                string = i + " = " + savedValues[i]
                f.write(string)
    
    def playBgMusic(self):
        self.backgroundMusic = self.assetMngr.getSound('Main_menu')
        # self.backgroundMusic.play(-1)

    def parceJSON(self):
        self.settings = json.load(open("configs/settings.json", 'r'))
        
        for i in self.settings['controls']:
            self.controls[i] = self.settings['controls'][i]

        logging.info("------ SETTINGS ------")
        for i in self.settings:
            logging.debug(i + ' = ' + str(self.settings[i]))

    def createUIWidgets(self):
        self.CurrPercent = 70
        self.img = pygame.image.load('media/pygame_logo_100x100.png')
        
        label_game_width = 623
        button_width = 200
        button_height = 70
        image_width = 427
        arrow_btn_width = 94
        medium_size_btn_h = 50
        label_sp_width = 160
        label_sp_height = 55
        label_asc_width = 85
        label_asc_height = 35
        label_settings_width = 200 # где-то получилось, что текст сдвинулся, т.к. расположение текста в центре, а нужно сделать по левому краю
        label_settings_height = 25
        slider_width = 163
        slider_height = 20
        menu_width = 123
        menu_height = 20
        textEntryLine_width = 80
        textEntryLine_height = 28

# Main menu
        self.mainMenuWidgets = {}
        self.mainMenuWidgets['info_button'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((OFFSET * 3, OFFSET * 3), (70, 70)), text='Info', manager=self.manager)       # info_button
        self.mainMenuWidgets['main_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(( (WIDTH / 2) - (label_game_width / 2), HEIGHT / 8), (label_game_width, 70)), text="MultiGenreGame", manager=self.manager)     # label_name_game
        self.mainMenuWidgets['play_button'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH / 3) - (button_width / 2) - (OFFSET * 4), (HEIGHT / 3)), (button_width, button_height)), text='Play', manager=self.manager)       # play_button
        self.mainMenuWidgets['settings_button'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH / 3) - (button_width / 2) - (OFFSET * 4), (HEIGHT / 3) + (button_height + (OFFSET * 5))), (button_width, button_height)), text='Settings', manager=self.manager)      # settings_button
        self.mainMenuWidgets['exit_button'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH / 3) - (button_width / 2) - (OFFSET * 4), (HEIGHT / 3) + ((button_height  + (OFFSET * 5)) * 2)), (button_width, button_height)), text='Exit', manager=self.manager)       # exit_button
        self.mainMenuWidgets['left_arrow_button'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH * 0.66) - (arrow_btn_width) - OFFSET, (HEIGHT * 0.66) + (OFFSET * 2)), (arrow_btn_width, medium_size_btn_h)), text='Left arrow', manager=self.manager)       # left_arrow_button
        self.mainMenuWidgets['right_arrow_button'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH * 0.66) + OFFSET, (HEIGHT * 0.66) + (OFFSET * 2)), (arrow_btn_width, medium_size_btn_h)), text='Right arrow', manager=self.manager)     # right_arrow_button
        self.mainMenuWidgets['image'] = pygame_gui.elements.UIImage(pygame.Rect(((WIDTH * 0.66) - (image_width / 2), (HEIGHT / 3)), (image_width, 240)), self.img, self.manager)       # image
# Settings        
        self.settingsWidgets = {}
        self.settingsWidgets['info_settings_button'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((OFFSET * 3, OFFSET * 3), (70, 70)), text='Info', manager=self.manager)
        self.settingsWidgets['settings_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 2) - (label_sp_width / 2), (HEIGHT / 3) - (label_sp_height / 2) - OFFSET), (label_sp_width, label_sp_height)), text="Settings", manager=self.manager)
        self.settingsWidgets['Back_button'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((OFFSET * 3, (HEIGHT - medium_size_btn_h) - (OFFSET * 3)), ((button_width / 2), medium_size_btn_h)), text='Back', manager=self.manager)
        self.settingsWidgets['OK_button'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH - (button_width / 2)) - (OFFSET * 3), (HEIGHT - medium_size_btn_h) - (OFFSET * 3)), ((button_width / 2), medium_size_btn_h)), text='OK', manager=self.manager)
        
        self.settingsWidgets['Audio_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_asc_width - (OFFSET * 14) , (HEIGHT / 3) + (OFFSET * 2.2)), (label_asc_width, label_asc_height)), text="Audio", manager=self.manager)
        self.settingsWidgets['Sound_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_settings_width - (OFFSET * 6.3), (HEIGHT / 3) + (OFFSET * 6.9)), (label_settings_width, label_settings_height)), text="Sound", manager=self.manager)
        self.settingsWidgets['Sound_slider'] = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(((WIDTH / 3) - (OFFSET * 0.5), (HEIGHT / 3) + (OFFSET * 6.9)), (slider_width, slider_height)), start_value=self.settings['sound'], value_range=[0, 100], manager=self.manager)
        self.settingsWidgets['Music_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_settings_width - (OFFSET * 6.3), (HEIGHT / 2) + (OFFSET * 0.8)), (label_settings_width, label_settings_height)), text="Music", manager=self.manager)
        self.settingsWidgets['Music_slider'] = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(((WIDTH / 3) - (OFFSET * 0.5), (HEIGHT / 2) + (OFFSET * 0.8)), (slider_width, slider_height)), start_value=self.settings['music'], value_range=[0, 100], manager=self.manager)
        
        self.settingsWidgets['Screen_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_asc_width - (OFFSET * 14) , (HEIGHT * 0.66) - (label_asc_height / 2) - (OFFSET * 1.7)), (label_asc_width, label_asc_height)), text="Screen", manager=self.manager)
        self.settingsWidgets['Resolution_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_settings_width - (OFFSET * 6.3), (HEIGHT * 0.66) + (OFFSET * 1.3)), (label_settings_width, label_settings_height)), text="Resolution", manager=self.manager)
        self.settingsWidgets['Resolution_DDM'] = pygame_gui.elements.UIDropDownMenu(options_list=["480x640", "800x600", "1280x720", "1920x1080"], starting_option=self.settings['resolution'], relative_rect=pygame.Rect(((WIDTH / 3) - (OFFSET * 5.27), (HEIGHT * 0.66) + (OFFSET * 1.3)), (menu_width, menu_height)), manager=self.manager)
        self.settingsWidgets['Display_mode_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_settings_width - (OFFSET * 6.3), (HEIGHT * 0.66) + (OFFSET * 6.2)), (label_settings_width, label_settings_height)), text="Display mode", manager=self.manager)
        self.settingsWidgets['Screen_DDM'] = pygame_gui.elements.UIDropDownMenu(options_list=["Fullscreen", "Window", "Resizable"], starting_option=self.settings['screen'], relative_rect=pygame.Rect(((WIDTH / 3) - (OFFSET * 5.27), (HEIGHT * 0.66) + (OFFSET * 6.2)), (menu_width, menu_height)), manager=self.manager)
        

        self.settingsWidgets['Controls_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((WIDTH / 1.93, HEIGHT / 2.75), (label_asc_width, label_asc_height)), text="Controls", manager=self.manager)
        self.settingsWidgets['Left_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 5)), (label_settings_width, label_settings_height)), text="Left", manager=self.manager)
        self.settingsWidgets['Right_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 6) + label_settings_height), (label_settings_width, label_settings_height)), text="Right", manager=self.manager)
        self.settingsWidgets['Jump_platformer_label']= pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 7) + (label_settings_height * 2)), (label_settings_width, label_settings_height)), text="Jump (platformer)", manager=self.manager)
        self.settingsWidgets['Sit_down_platformer_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 8) + (label_settings_height * 3)), (label_settings_width, label_settings_height)), text="Sit down (platformer)", manager=self.manager)
        self.settingsWidgets['Fight_platformer_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 9) + (label_settings_height * 4)), (label_settings_width, label_settings_height)), text="fight (platformer)", manager=self.manager)
        self.settingsWidgets['Fire_platformer_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 10) + (label_settings_height * 5)), (label_settings_width, label_settings_height)), text="fire (platformer)", manager=self.manager)
        self.settingsWidgets['Weapon_change_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 11) + (label_settings_height * 6)), (label_settings_width, label_settings_height)), text="Weapon change", manager=self.manager)
        self.settingsWidgets['Fire_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 12) + (label_settings_height * 7)), (label_settings_width, label_settings_height)), text="Fire (shooter)", manager=self.manager)
        self.settingsWidgets['Front_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 13) + (label_settings_height * 8)), (label_settings_width, label_settings_height)), text="Front (shooter)", manager=self.manager)
        self.settingsWidgets['Back_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH * 0.66) - label_settings_width + (OFFSET * 0.92), (HEIGHT / 3) + (OFFSET * 14) + (label_settings_height * 9)), (label_settings_width, label_settings_height)), text="Back (shooter)", manager=self.manager)
        
        self.settingsControls = {}
        self.settingsControls["left"] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 5))), (textEntryLine_width, textEntryLine_height)), manager=self.manager, initial_text=self.controls['left'])
        self.settingsControls["right"] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 6) + label_settings_height)), (textEntryLine_width, textEntryLine_height)), manager=self.manager, initial_text=self.controls['right'])
        self.settingsControls["jump"] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 7) + label_settings_height * 2)), (textEntryLine_width, textEntryLine_height)), manager=self.manager, initial_text=self.controls['jump'])
        self.settingsControls["sit_down"] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 8) + label_settings_height * 3)), (textEntryLine_width, textEntryLine_height)), manager=self.manager, initial_text=self.controls['sit_down'])
        self.settingsControls["fight"] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 9) + label_settings_height * 4)), (textEntryLine_width, textEntryLine_height)), manager=self.manager, initial_text=self.controls['fight'])
        self.settingsControls["fire"] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 10) + label_settings_height * 5)), (textEntryLine_width, textEntryLine_height)), manager=self.manager, initial_text=self.controls['fire'])
        self.settingsControls["change_weapon"] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 11) + label_settings_height * 6)), (textEntryLine_width, textEntryLine_height)), manager=self.manager, initial_text=self.controls['change_weapon'])
        self.settingsControls["fire_shooter"] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 12) + label_settings_height * 7)), (textEntryLine_width, textEntryLine_height)), manager=self.manager, initial_text=self.controls['fire_shooter'])
        self.settingsControls["front"] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 13) + label_settings_height * 8)), (textEntryLine_width, textEntryLine_height)), manager=self.manager, initial_text=self.controls['front'])
        self.settingsControls["back"] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 14) + label_settings_height * 9)), (textEntryLine_width, textEntryLine_height)), manager=self.manager, initial_text=self.controls['back'])

        for widget in self.settingsControls:
            self.settingsControls[widget].set_text_length_limit(1)

# Pause
        self.pauseWidgets = {}
        self.pauseWidgets['Pause_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 2) - (label_sp_width / 2), (HEIGHT / 3) - (label_sp_height / 2)), (label_sp_width, label_sp_height)), text="Pause", manager=self.manager)
        self.pauseWidgets['continue_button'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH / 2) - (button_width / 2), (HEIGHT / 3) + (OFFSET * 5)), (button_width, button_height)), text='Continue', manager=self.manager)
        self.pauseWidgets['settings_pause_button'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH / 2) - (button_width / 2), (HEIGHT / 3) + (OFFSET * 8.5) + button_height), (button_width, button_height)), text='Settings', manager=self.manager)
        self.pauseWidgets['exit_pause_button'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((WIDTH / 2) - (button_width / 2), (HEIGHT / 3) + (OFFSET * 12) + (button_height * 2)), (button_width, button_height)), text='Exit', manager=self.manager)

    # Singleton pattern
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Game, cls).__new__(cls)
        return cls.instance

    def getCurrPercent(self):
        return self.CurrPercent

    def UIEvents(self, event):
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            # Main_menu             
            if event.ui_element == self.mainMenuWidgets['play_button']:
                config.state = config.UIEnum.Game.value

            if event.ui_element == self.mainMenuWidgets['settings_button']:
                config.prev_state = config.state
                config.state = config.UIEnum.Settings.value

            if event.ui_element == self.mainMenuWidgets['exit_button']:
                self.running = False

            if event.ui_element == self.mainMenuWidgets['left_arrow_button']:
                if (self.currentLevel == 0):
                    self.currentLevel = 2
                else:
                    self.currentLevel -= 1

                print(self.currentLevel)

            if event.ui_element == self.mainMenuWidgets['right_arrow_button']:
                if (self.currentLevel == 2):
                    self.currentLevel = 0
                else:
                    self.currentLevel += 1

                print(self.currentLevel)
            
            # Settings
            if event.ui_element == self.settingsWidgets['info_settings_button']:
                print('Button info was pressed!')

            if event.ui_element == self.settingsWidgets['Back_button']:
                config.state = config.UIEnum.Main_menu.value

            if event.ui_element == self.settingsWidgets['OK_button']:
                for widget in self.settingsControls:
                    self.controls[widget] = self.settingsControls[widget].get_text()

                logging.info("------ Keys was changed ------")
                for widget in self.controls:
                    logging.debug(widget + ' ' + self.controls[widget])

                config.state = config.UIEnum.Main_menu.value
                config.state = config.prev_state
            
            # Pause
            if event.ui_element == self.pauseWidgets['continue_button']:
                config.state = config.UIEnum.Game.value

            if event.ui_element == self.pauseWidgets['settings_pause_button']:
                config.prev_state = config.state
                config.state = config.UIEnum.Settings.value

            if event.ui_element == self.pauseWidgets['exit_pause_button']:
                config.state = config.UIEnum.Main_menu.value

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.settingsWidgets['Sound_slider']:
                bgMusicValue = self.backgroundMusic.get_volume()
                self.assetMngr.setAllVolumes(event.value / 100)
                self.assetMngr.setSoundVolume(self.backgroundMusic, bgMusicValue)
                print('Sound_slider:', event.value / 100)

            if event.ui_element == self.settingsWidgets['Music_slider']:
                self.assetMngr.setSoundVolume(self.backgroundMusic, event.value / 100)
                print('Music_slider:', event.value / 100)


        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if (event.ui_element == self.settingsWidgets['Resolution_DDM']):
                res = event.text.split('x')
                config.curr_window_width = int(res[0])
                config.curr_window_height = int(res[1])
                pygame.display.set_mode((config.curr_window_width, config.curr_window_height))
                
            if (event.ui_element == self.settingsWidgets['Screen_DDM']):
                if(event.text == 'Window'):
                    pygame.display.set_mode((config.curr_window_width, config.curr_window_height))
                    
                if(event.text == 'Fullscreen'):
                    info = pygame.display.Info() 
                    pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
                
                if(event.text == 'Resizable'):
                    pygame.display.set_mode((config.curr_window_width, config.curr_window_height), pygame.RESIZABLE)

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
        
            self.UIEvents(event)
            self.manager.process_events(event)

            if(config.state == config.UIEnum.Game.value):
                if(self.isLevelInit == True):
                    self.inputHandler = InputHandler(self.player, self.publisher, self.currentLevel)
                    self.inputHandler.handleInput(event, self.controls)

    def changeUIState(self):
        if (config.state == config.UIEnum.Main_menu.value):

            for widget in self.mainMenuWidgets:
                self.mainMenuWidgets[widget].show()

            for widget in self.settingsWidgets:
                self.settingsWidgets[widget].hide()

            for widget in self.settingsControls:
                self.settingsControls[widget].hide()

            for widget in self.pauseWidgets:
                self.pauseWidgets[widget].hide()

        if (config.state == config.UIEnum.Game.value):
            for widget in self.mainMenuWidgets:
                self.mainMenuWidgets[widget].hide()

            for widget in self.settingsWidgets:
                self.settingsWidgets[widget].hide()

            for widget in self.settingsControls:
                self.settingsControls[widget].hide()

            for widget in self.pauseWidgets:
                self.pauseWidgets[widget].hide()

            if (self.currentLevel == LevelEnum.Strategy.value):
                if(self.isLevelInit == False):
                    self.level = Level()
                    self.player = Player(self.level.getGroups(), self.level.getCollSprites(), self.publisher, self.currentLevel)
                    self.level.setup_level(self.player, self.currentLevel, "configs/strategy.txt")
                    self.isLevelInit = True

                if (self.isLevelInit == True):
                    self.level.update(self.dt)

            if (self.currentLevel == LevelEnum.Shooter.value):
                if(self.isLevelInit == False):
                    self.level = Level()
                    self.player = Player(self.level.getGroups(), self.level.getCollSprites(), self.publisher, self.currentLevel)
                    self.level.setup_level(self.player, self.currentLevel, "configs/shooter.txt")
                    #self.loadProgress()
                    #logging.info(str(savedValues))
                    self.isLevelInit = True

                if (self.isLevelInit == True):
                    self.level.update(self.dt)

            if (self.currentLevel == LevelEnum.Platformer.value):
                if(self.isLevelInit == False):
                    self.level = Level()
                    self.player = Player(self.level.getGroups(), self.level.getCollSprites(), self.publisher, self.currentLevel)
                    self.level.setup_level(self.player, self.currentLevel, "configs/levelPlatformer.txt")
                    self.loadProgress()
                    logging.info(str(savedValues))
                    self.isLevelInit = True

                if (self.isLevelInit == True):
                    self.level.update(self.dt)

        if (config.state == config.UIEnum.Pause.value):
            for widget in self.mainMenuWidgets:
                self.mainMenuWidgets[widget].hide()

            for widget in self.settingsWidgets:
                self.settingsWidgets[widget].hide()

            for widget in self.settingsControls:
                self.settingsControls[widget].hide()

            for widget in self.pauseWidgets:
                self.pauseWidgets[widget].show()

        if (config.state == config.UIEnum.Settings.value):
            self.screen.fill("black")

            for widget in self.mainMenuWidgets:
                self.mainMenuWidgets[widget].hide()

            for widget in self.settingsWidgets:
                self.settingsWidgets[widget].show()

            for widget in self.settingsControls:
                self.settingsControls[widget].show()

            for widget in self.pauseWidgets:
                self.pauseWidgets[widget].hide()

    def update(self):
        self.screen.fill("black")
        self.changeUIState()
        self.manager.update(self.dt)

    def render(self):
        self.manager.draw_ui(self.screen)
        pygame.display.update()

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()

            self.dt = self.clock.tick(FPS) / SPEED_SCALE

        logging.info("Game was stopped")
        pygame.quit()

game = Game()
game.run()