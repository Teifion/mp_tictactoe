import time
import multiprocessing

from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

class TTT(LineReceiver):
    def __init__(self, users):
        self.users = users
        self.name = None
        self.state = "GETNAME"
    
    def connectionMade(self):
        self.sendLine("You are connected")
    
    def connectionLost(self, reason):
        if self.users.has_key(self.name):
            del self.users[self.name]
    
    def lineReceived(self, line):
        if line == "quit":
            reactor.stop()
            
        if self.state == "GETNAME":
            self.handle_GETNAME(line)
        else:
            self.handle_CHAT(line)
    
    def handle_GETNAME(self, name):
        if self.users.has_key(name):
            self.sendLine("Name taken, please choose another.")
            return
        self.sendLine("Welcome, %s!" % (name,))
        self.name = name
        self.users[name] = self
        self.state = "CHAT"
    
    def handle_CHAT(self, message):
        message = "<%s> %s" % (self.name, message)
        for name, protocol in self.users.iteritems():
            if protocol != self:
                protocol.sendLine(message)


class TTTFactory(Factory):
    def __init__(self):
        self.state = [0 for x in range(9)]
        self.turn = -1
        
        self.users = {} # maps user names to Chat instances
    
    def make_move(self, player, x, y):
        if player != self.turn:
            return "Not your turn"
        
        i = x + y * 3
        
        if self.state[i] != 0:
            return "Invalid move"
        
        self.state[i] = player
        
        # Horrizontal
        if self.state[0] == self.state[1] == self.state[2]: return "Win"
        if self.state[3] == self.state[4] == self.state[5]: return "Win"
        if self.state[6] == self.state[7] == self.state[8]: return "Win"
        
        # Vertical
        if self.state[0] == self.state[3] == self.state[6]: return "Win"
        if self.state[1] == self.state[4] == self.state[7]: return "Win"
        if self.state[2] == self.state[5] == self.state[8]: return "Win"
        
        # Diagonal
        if self.state[0] == self.state[4] == self.state[8]: return "Win"
        if self.state[6] == self.state[4] == self.state[2]: return "Win"
        
        # Swap turn
        self.turn = 0 - self.turn
        return "Next move"
    
    def buildProtocol(self, addr):
        return TTT(self.users)

# def reactor_runner():
def new_server(conn):
    port_num = 8007
    conn.send(port_num)
    
    reactor.listenTCP(port_num, TTTFactory())
    reactor.run()

