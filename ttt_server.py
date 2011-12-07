import time
import socket

import screen_lib

from PodSixNet.Channel import Channel
from PodSixNet.Server import Server

# class representing a sigle connection with a client
# this can also represent a player
class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        Channel.__init__(self, *args, **kwargs)
        
        # points of the player
        self.points = 0
        self.player_id = 0
    
    def Network_quit(self, data=None):
        self._server.running = False
    
    def Network_move(self, data):
        x, y = int(data['x']), int(data['y'])
        
        self._server.make_move(self.player_id, x, y)
    

class TTTServer(Server):
    channelClass = ClientChannel
    
    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        
        # Game state
        self.state = [-1 for x in range(9)]
        self.turn = 0
        
        self.users = {} # maps user names to Chat instances
        
        self.timeout = 0
        self.running = True
        
        self.players = []
        
        self._next_update = time.time()
        self._update_delay = screen_lib.set_fps(self, 30)
        
        self.address, self.port = kwargs['localaddr']
        print('Server started at {} at port {}'.format(self.address, str(self.port)))
    
    # function called on every connection
    def Connected(self, player, addr):
        print("Player connected at {}, using port {}".format(addr[0], addr[1]))
        
        # add player to the list
        player.player_id = len(self.players)
        self.players.append(player)
        
        # set the bar rect of the player
        # player.rect = self.rects[len(self.players)-1]
        
        # send to the player their number
        player.Send({'action': 'number', 'num': len(self.players)-1})
        
        # send the initial ball speed
        player.Send({'action': 'gamestate', 'state': self.state})
        
    # this send to all clients the same data
    def send_to_all(self, data):
        [p.Send(data) for p in self.players]
    
    def loop(self, conn):
        """conn is used to send the server information
        from the parent process"""
        
        conn.send("setup complete")
        conn.send(self.address)
        conn.send(self.port)
        
        while self.running:
            self.update(conn)
    
    def update(self, conn):
        if time.time() < self._next_update:
            return
        
        # Update server connection
        self.Pump()
        
        # Check parent process connection
        while conn.poll():
            data = conn.recv()
            cmd, kwargs = data
            
            if cmd == "quit":
                self.running = False
            
            else:
                print("No handler for {}:{}".format(cmd, str(kwargs)))
        
        # What is happening today?
        """SERVER LOGIC GOES HERE"""
        
        self._next_update = time.time() + self._update_delay
    
    def make_move(self, player, x, y):
        if player != self.turn:
            return "Not your turn"
        
        i = x + y * 3
        
        if self.state[i] != -1:
            return "Invalid move"
        
        self.state[i] = player
        
        self.send_to_all({"action":"gamestate", "state":self.state})
        
        # Horrizontal
        if self.state[0] == self.state[1] == self.state[2] and self.state[0] != -1: return "Win"
        if self.state[3] == self.state[4] == self.state[5] and self.state[3] != -1: return "Win"
        if self.state[6] == self.state[7] == self.state[8] and self.state[6] != -1: return "Win"
        
        # Vertical
        if self.state[0] == self.state[3] == self.state[6] and self.state[0] != -1: return "Win"
        if self.state[1] == self.state[4] == self.state[7] and self.state[1] != -1: return "Win"
        if self.state[2] == self.state[5] == self.state[8] and self.state[2] != -1: return "Win"
        
        # Diagonal
        if self.state[0] == self.state[4] == self.state[8] and self.state[0] != -1: return "Win"
        if self.state[6] == self.state[4] == self.state[2] and self.state[6] != -1: return "Win"
        
        # Swap turn
        self.turn = 1 - self.turn
        return "Next move"

# def reactor_runner():
def new_server(conn):
    address = socket.gethostbyname(socket.gethostname())
    
    myserver = TTTServer(localaddr=(address, 31500))
    myserver.loop(conn)

