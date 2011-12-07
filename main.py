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

def run_server():
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
    
    return address, port, parent_conn, server_proc

def run_client(address, port):
    g = Game(address, port)
    g.start()

if __name__ == '__main__':
    # If we supply an IP address we connect
    if len(sys.argv) == 2:
        mode = sys.argv[1]
        
        if mode == "dual":
            address, port, conn, server_proc = run_server()
            
            c1 = multiprocessing.Process(
                target=run_client,
                args=(address, port)
            )
            
            c2 = multiprocessing.Process(
                target=run_client,
                args=(address, port)
            )
            
            c1.start()
            c2.start()
            
            c1.join()
            c2.join()
            
            conn.send(["quit", {}])
            server_proc.join()
    
    elif len(sys.argv) > 2:
        address = sys.argv[1]
        port = int(sys.argv[2])
        
        run_client(address, port)
    
    else:
        address, port, conn, server_proc = run_server()
        
        g = Game(address, port)
        g.start()

        conn.send(["quit", {}])
        server_proc.join()
    

