import time

def new_server(conn):
    flag = True
    timeout = 0
    while flag:
        # Timout
        timeout += 1
        if timeout >= 50:
            flag = False
            continue
        
        # Check there is data to read
        if not conn.poll():
            time.sleep(0.1)
            continue
        
        # Data is there, lets go wild!
        timeout = 0
        data = conn.recv()
        
        cmd, kwargs = data
        
        if cmd == "quit":
            flag = False
            continue
            
        elif cmd == "keepalive":
            continue
            
        else:
            print("No handler for: {}, {}".format(cmd, str(kwargs)))
    

