import sys
import ttt_server, ttt_screen, ttt_core
import multiprocessing

class Game (ttt_core.EngineV4):
    name = "Tic tac toe"
    
    fps = 30
    
    screen_size = [600, 600]
    fullscreen = False
    
    def __init__(self, address, port):
        ttt_core.EngineV4.__init__(self, address, port)
    
    def startup(self):
        ttt_core.EngineV4.startup(self)
        
        self.screens['Game'] = ttt_screen.Screen
        
        self.set_screen('Game')
        self.new_game()
    
    def new_game(self):
        pass


if __name__ == '__main__':
    # If we supply an IP address we connect
    if len(sys.argv) > 1:
        address = sys.argv[1]
        port = int(sys.argv[2])
        parent_conn = None
    
    # If no IP address then we start a server
    else:
        parent_conn, child_conn = multiprocessing.Pipe()
        
        server_proc = multiprocessing.Process(
            target=ttt_server.new_server,
            args=(child_conn, )
        )
        server_proc.start()
        
        d = parent_conn.recv()
        
        if d != "setup complete":
            parent_conn.send(["quit", {}])
            raise Exception("Unexpected value from parent_conn: {}".format(d))
        
        address = parent_conn.recv()
        port = parent_conn.recv()
    
    # Lets start our game
    g = Game(address, port)
    g.start()
    
    if len(sys.argv) <= 1:
        parent_conn.send(["quit", {}])
        server_proc.join()


