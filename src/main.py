import pygame, pygame_gui

from observer import *
from command import *
from assetManager import *
from config import *

from player import *
from level import *

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        logging.info("Game was started")

# Load all resources
        self.assetMngr = AssetManager('media')
        # self.assetMngr.loadImages()
        # self.assetMngr.loadSounds()
        # self.assetMngr.loadFonts()

        self.publisher = Subject()
        self.publisher.addObserver(Audio())

        self.running = True
        self.speed = 7
        self.dt = 0                 # delta time in seconds since last frame

        self.level = Level()
        self.player = Player(self.level.getGroups(), self.level.getCollSprites())
        self.level.setup_level(self.player)

        self.inputHandler = InputHandler(self.player)
        self.manager = pygame_gui.UIManager((WIDTH, HEIGHT))

        self.createUIWidgets()

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
        self.settingsWidgets['Sound_slider'] = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(((WIDTH / 3) - (OFFSET * 0.5), (HEIGHT / 3) + (OFFSET * 6.9)), (slider_width, slider_height)), start_value=0, value_range=[0, 100], manager=self.manager)
        self.settingsWidgets['Music_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_settings_width - (OFFSET * 6.3), (HEIGHT / 2) + (OFFSET * 0.8)), (label_settings_width, label_settings_height)), text="Music", manager=self.manager)
        self.settingsWidgets['Music_slider'] = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(((WIDTH / 3) - (OFFSET * 0.5), (HEIGHT / 2) + (OFFSET * 0.8)), (slider_width, slider_height)), start_value=0, value_range=[0, 100], manager=self.manager)
        
        self.settingsWidgets['Screen_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_asc_width - (OFFSET * 14) , (HEIGHT * 0.66) - (label_asc_height / 2) - (OFFSET * 1.7)), (label_asc_width, label_asc_height)), text="Screen", manager=self.manager)
        self.settingsWidgets['Resolution_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_settings_width - (OFFSET * 6.3), (HEIGHT * 0.66) + (OFFSET * 1.3)), (label_settings_width, label_settings_height)), text="Resolution", manager=self.manager)
        self.settingsWidgets['Resolution_DDM'] = pygame_gui.elements.UIDropDownMenu(options_list=["1280 x 720", "2", "3"], starting_option="1280 x 720", relative_rect=pygame.Rect(((WIDTH / 3) - (OFFSET * 5.27), (HEIGHT * 0.66) + (OFFSET * 1.3)), (menu_width, menu_height)), manager=self.manager)
        self.settingsWidgets['Display_mode_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_settings_width - (OFFSET * 6.3), (HEIGHT * 0.66) + (OFFSET * 6.2)), (label_settings_width, label_settings_height)), text="Display mode", manager=self.manager)
        self.settingsWidgets['Screen_DDM'] = pygame_gui.elements.UIDropDownMenu(options_list=["Fullscreen", "2", "3"], starting_option="Fullscreen", relative_rect=pygame.Rect(((WIDTH / 3) - (OFFSET * 5.27), (HEIGHT * 0.66) + (OFFSET * 6.2)), (menu_width, menu_height)), manager=self.manager)
        self.settingsWidgets['Brightness_label'] = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(((WIDTH / 3) - label_settings_width - (OFFSET * 6.3), (HEIGHT * 0.66) + (OFFSET * 11.3)), (label_settings_width, label_settings_height)), text="Brightness", manager=self.manager)
        self.settingsWidgets['Brightness_slider'] = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect(((WIDTH / 3) - (OFFSET * 5.27), (HEIGHT * 0.66) + (OFFSET * 11.3)), (slider_width, slider_height)), start_value=0, value_range=[0, 100], manager=self.manager)
        

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
        
        self.settingsWidgets['Left_text_line'] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 5))), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.settingsWidgets['Right_text_line'] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 6) + label_settings_height)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.settingsWidgets['Jump_platformer_text_line'] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 7) + label_settings_height * 2)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.settingsWidgets['Sit_down_platformer_text_line'] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 8) + label_settings_height * 3)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.settingsWidgets['Fight_platformer_text_line'] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 9) + label_settings_height * 4)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.settingsWidgets['Fire_platformer_text_line'] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 10) + label_settings_height * 5)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.settingsWidgets['Weapon_change_text_line'] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 11) + label_settings_height * 6)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.settingsWidgets['Fire_text_line'] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 12) + label_settings_height * 7)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.settingsWidgets['Front_text_line'] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 13) + label_settings_height * 8)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)
        self.settingsWidgets['Back_text_line'] = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((((WIDTH * 0.66) + (OFFSET * 7), (HEIGHT / 3) + (OFFSET * 14) + label_settings_height * 9)), (textEntryLine_width, textEntryLine_height)), manager=self.manager)

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
                print('Button play was pressed!')
                config.state = config.UIEnum.Game.value
            if event.ui_element == self.mainMenuWidgets['settings_button']:
                config.state = config.UIEnum.Settings.value
                print('Button settings was pressed!')
            if event.ui_element == self.mainMenuWidgets['exit_button']:
                print('Button exit was pressed!')
            if event.ui_element == self.mainMenuWidgets['left_arrow_button']:
                print('Button left arrow was pressed!')
            if event.ui_element == self.mainMenuWidgets['right_arrow_button']:
                print('Button right arrow was pressed!')
            
            # Settings
            if event.ui_element == self.settingsWidgets['info_settings_button']:
                print('Button info was pressed!')
            if event.ui_element == self.settingsWidgets['Back_button']:
                config.state = config.UIEnum.Main_menu.value
                print('Button Back was pressed!')
            if event.ui_element == self.settingsWidgets['OK_button']:
                config.state = config.UIEnum.Main_menu.value
                print('Button OK was pressed, changes saved!')
            
            # Pause
            if event.ui_element == self.pauseWidgets['continue_button']:
                config.state = config.UIEnum.Game.value
                print('Button continue was pressed!')
            if event.ui_element == self.pauseWidgets['settings_pause_button']:
                config.state = config.UIEnum.Settings.value
                print('Button settings was pressed!')  
            if event.ui_element == self.pauseWidgets['exit_pause_button']:
                config.state = config.UIEnum.Main_menu.value
                print('Button exit was pressed!')

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.settingsWidgets['Brightness_slider']:
                print('Brightness_slider:', event.value)
            
            if event.ui_element == self.settingsWidgets['Sound_slider']:
                print('Sound_slider:', event.value)

            if event.ui_element == self.settingsWidgets['Music_slider']:
                print('Music_slider:', event.value)

        if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
            if (event.ui_element == self.settingsWidgets['Resolution_DDM']):
                print("Resolution_DDM:", event.text)

            if (event.ui_element == self.settingsWidgets['Screen_DDM']):
                print("Screen_DDM:", event.text)

        if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
            if (event.ui_element == self.settingsWidgets['Left_text_line']):
                if(len(event.text) == 1):
                    print("Left_text_line:", event.text)

            if (event.ui_element == self.settingsWidgets['Right_text_line']):
                if(len(event.text) == 1):
                    print("Right_text_line:", event.text)
            
            if (event.ui_element == self.settingsWidgets['Jump_platformer_text_line']):
                if(len(event.text) == 1):
                    print("Jump_platformer_text_line:", event.text)
            
            if (event.ui_element == self.settingsWidgets['Sit_down_platformer_text_line']):
                if(len(event.text) == 1):
                    print("Sit_down_platformer_text_line:", event.text)
            
            if (event.ui_element == self.settingsWidgets['Fight_platformer_text_line']):
                if(len(event.text) == 1):
                    print("Fight_platformer_text_line:", event.text)
            
            if (event.ui_element == self.settingsWidgets['Fire_platformer_text_line']):
                if(len(event.text) == 1):
                    print("Fire_platformer_text_line:", event.text)

            if (event.ui_element == self.settingsWidgets['Weapon_change_text_line']):
                if(len(event.text) == 1):
                    print("Weapon_change_text_line:", event.text)
            
            if (event.ui_element == self.settingsWidgets['Fire_text_line']):
                if(len(event.text) == 1):
                    print("Fire_text_line:", event.text)
            
            if (event.ui_element == self.settingsWidgets['Front_text_line']):
                if(len(event.text) == 1):
                    print("Front_text_line:", event.text)

            if (event.ui_element == self.settingsWidgets['Back_text_line']):
                if(len(event.text) == 1):
                    print("Back_text_line:", event.text)
            

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
        
            self.UIEvents(event)

            self.manager.process_events(event)

        self.inputHandler.handleInput()

    def changeUIState(self):
        if (config.state == config.UIEnum.Main_menu.value):
            for widget in self.mainMenuWidgets:
                self.mainMenuWidgets[widget].show()

            for widget in self.settingsWidgets:
                self.settingsWidgets[widget].hide()

            for widget in self.pauseWidgets:
                self.pauseWidgets[widget].hide()

        if (config.state == config.UIEnum.Game.value):
            for widget in self.mainMenuWidgets:
                self.mainMenuWidgets[widget].hide()

            for widget in self.settingsWidgets:
                self.settingsWidgets[widget].hide()

            for widget in self.pauseWidgets:
                self.pauseWidgets[widget].hide()

        if (config.state == config.UIEnum.Pause.value):
            for widget in self.mainMenuWidgets:
                self.mainMenuWidgets[widget].hide()

            for widget in self.settingsWidgets:
                self.settingsWidgets[widget].hide()

            for widget in self.pauseWidgets:
                self.pauseWidgets[widget].show()

        if (config.state == config.UIEnum.Settings.value):
            self.screen.fill("black")

            for widget in self.mainMenuWidgets:
                self.mainMenuWidgets[widget].hide()

            for widget in self.settingsWidgets:
                self.settingsWidgets[widget].show()

            for widget in self.pauseWidgets:
                self.pauseWidgets[widget].hide()

    def update(self):
        self.manager.update(self.dt)
        self.level.update(self.dt)
        self.changeUIState()

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