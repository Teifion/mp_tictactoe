from __future__ import division

import pygame

import math

def set_fps(screen, fps):
    return 1/fps

def make_rotated_image(image, angle):
    return pygame.transform.rotate(image, -angle)


def _transition_fade_to_black(the_screen, total_frames=60):
    surf = the_screen.engine.display
    
    def trans(frame):
        if frame > total_frames:
            return None
        
        v = 255 - ((frame/total_frames) * 255)
        
        the_screen.background = (v, v, v)
        
        return True
    
    return trans

def _transition_fade_all_to_black(the_screen, total_frames=60):
    surf = the_screen.engine.display
    
    def trans(frame):
        if frame > total_frames:
            return None
        
        v = 255 - ((frame/total_frames) * 255)
        
        colour = (v, v, v)
        surf.fill(colour)
        
        return True
    
    return trans

transitions = {
    "Fade to black": _transition_fade_to_black,
    "Fade to all black": _transition_fade_all_to_black,
}

