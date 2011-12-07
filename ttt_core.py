from __future__ import division

from PodSixNet.Connection import connection, ConnectionListener

import sys
import time
import math
import traceback
import re

import pygame
from pygame.locals import *

file_name = re.compile(r".*/(.*?)\.[a-zA-Z]*")

class EngineV4 (ConnectionListener):
    fps = 30
    
    facings = 360/4# The number of different angles we'll draw
    
    def __init__(self, host, port):
        super(EngineV4, self).__init__()
        
        self.Connect((host, port))
        
        self.screens = {}
        self.current_screen = None
        self.images = {}
    
    def startup(self):
        pass
    
    def Network_gamestate(self, data):
        self.current_screen.state = data['state']
    
    def Network_connected(self, data):
        print "connected to the server"
    
    def Network_error(self, data):
        print "error:", data['error'][1]
    
    def Network_disconnected(self, data):
        print "disconnected from the server"
    
    def Network_myaction(data):
        print "myaction:", data
    
    def quit(self, event=None):
        self.running = False
        connection.Send({'action': 'quit'})
    
    def set_screen(self, s, *args, **kwargs):
        # s can be a screen instance or the name of a screen in self.screens
        if s in self.screens:
            s = self.screens[s]
        elif type(s) == str:
            raise KeyError("Screen '%s' not found in screen dictionary" % s)
        
        # Is it an instance or a class? If the latter we make a new instance of it
        # if "__call__" in dir(s):
        if type(s) == type:
            try:
                s = s(self, *args, **kwargs)
            except Exception as e:
                print("Args: %s" % str(args))
                print("Kwargs: %s" % str(kwargs))
                raise
        
        s.engine = self
        s.activate()
        
        pygame.display.set_caption(s.name)
        self.current_screen = s
        self.current_screen.activate()
        self.current_screen.redraw()
    
    # Contains main execution loop
    def start(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.screen_size)
        
        self.running = True
        
        try:
            self.startup()
            
            while self.running:
                for event in pygame.event.get():
                    if event.type == ACTIVEEVENT:       self.current_screen._handle_active(event)
                    if event.type == KEYDOWN:           self.current_screen._handle_keydown(event)
                    if event.type == KEYUP:             self.current_screen._handle_keyup(event)
                    if event.type == MOUSEBUTTONUP:     self.current_screen._handle_mouseup(event)
                    if event.type == MOUSEBUTTONDOWN:   self.current_screen._handle_mousedown(event)
                    if event.type == MOUSEMOTION:       self.current_screen._handle_mousemotion(event)
                    if event.type == QUIT:              self.current_screen.quit(event)
                
                # Check to see if a key has been held down
                self.current_screen._handle_keyhold()
                
                connection.Pump()
                self.Pump()
                
                self.current_screen.update()
                self.current_screen.redraw()
            
        except Exception as e:
            print("")
            traceback.print_exc(file=sys.stdout)
            connection.Send({'action': 'quit'})
            
            if self.current_screen != None:
                self.current_screen.quit()
            raise
        
        self.quit()
        pygame.quit()
    
    def load_static_images(self, *images):
        pygame.image.load("media/red_shuttle.png")
        
        for i in images:
            if type(i) == list:
                self.load_static_images(i)
            else:
                name = file_name.search(i).groups()[0]
                self.images[name] = pygame.image.load(i)
    
    def load_animations(self, *images):
        pass
    
    def round_angle(self, angle):
        return int(math.floor(angle/(360/self.facings)) * (360/self.facings))
    
    def get_frame_name(self, image_name, frame, facing):
        """Wrapper for accessing both image and animation names"""
        facing = self.round_angle(facing)
        
        if type(self.images[image_name]) == pygame.Surface:
            return "%s_%s" % (image_name, facing)
        else:
            raise Exception("No handler for class type of %s" % type(self.images[image_name]))
    
    def get_image(self, image_name, frame=0):
        """Wrapper for accessing both images and animations"""
        if type(self.images[image_name]) == pygame.Surface:
            return self.images[image_name]
        else:
            raise Exception("No handler for type %s" % type(self.images[image_name]))

