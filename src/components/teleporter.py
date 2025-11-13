from components.physics import Trigger
from components.player import Player

def teleport(area_file):
    from core.area import area
   
    import pygame

    # Obtener la pantalla actual
    screen = pygame.display.get_surface()
    
    # Cargar nueva área con barra de carga
    area.load_file(area_file, screen)

class Teleporter(Trigger):
    def __init__(self, area_file, x=0, y=0, width=0, height=0):
        super().__init__(lambda: teleport(area_file), x, y, width, height)
