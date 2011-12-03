import sys
import ttt_server, ttt_client, ttt_screen, ttt_core

class Game (ttt_core.EngineV4):
    name = "Tic tac toe"
    
    fps = 30
    
    screen_size = [600, 600]
    fullscreen = False
    
    def __init__(self):
        super(Game, self).__init__()
        
        # self.load_static_images(
        #     "media/red_shuttle.png",
        #     "media/red_factory.png",
        #     "media/red_mine.png",
        #     "media/red_cruiser.png",
        # )
    
    def startup(self):
        super(Game, self).startup()
        
        self.screens['Game'] = ttt_screen.Screen
        
        self.set_screen('Game')
        self.new_game()
    
    def new_game(self):
        pass
        

if __name__ == '__main__':
    if len(sys.argv) > 1:
        ip_addr = sys.argv[1]
    
    g = Game()
    g.start()
    
