import sys
import ttt_server, ttt_client, ttt_screen, ttt_core
import multiprocessing

class Game (ttt_core.EngineV4):
    name = "Tic tac toe"
    
    fps = 30
    
    screen_size = [600, 600]
    fullscreen = False
    
    def __init__(self):
        super(Game, self).__init__()
    
    def startup(self):
        super(Game, self).startup()
        
        self.screens['Game'] = ttt_screen.Screen
        
        self.set_screen('Game')
        self.new_game()
    
    def new_game(self):
        pass


if __name__ == '__main__':
    # If we supply an IP address we connect
    if len(sys.argv) > 1:
        ip_addr = sys.argv[1]
    
    # If no IP address then we start a server
    else:
        parent_conn, child_conn = multiprocessing.Pipe()
        
        server_proc = multiprocessing.Process(
            target=ttt_server.new_server,
            args=(child_conn, )
        )
        server_proc.start()
        
        port_number = parent_conn.recv()
    
    g = Game()
    g.start()
    
    parent_conn.send(["quit", {}])
    server_proc.join()


