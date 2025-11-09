import pygame
from core.camera import camera

sprites = []
loaded = {}

class Sprite:
    def __init__(self, image=None, base_scale=1.0, depth_scale=True, anchor_y_ratio=1.0, draw_order_override=0):
        # Load and cache the original image
        self.original_image = None
        if image:
            if image in loaded:
                self.original_image = loaded[image]
            else:
                self.original_image = pygame.image.load(image)
                loaded[image] = self.original_image

        self.base_scale = base_scale
        self.depth_scale = depth_scale
        self.image = self.original_image if self.original_image else None
        self.entity = None

        self.anchor_y_ratio = anchor_y_ratio
        self.draw_order_override = draw_order_override
        
        sprites.append(self)

    def get_depth_scale_factor(self):
        """Calculate how much to scale based on Y position (depth)."""
        if not self.depth_scale or self.entity is None:
            return self.base_scale
        
        min_y = 500
        max_y = 1100
        min_scale = 0.9
        max_scale = 1.5
        
        clamped_y = max(min_y, min(max_y, self.entity.y))
        progress = (clamped_y - min_y) / (max_y - min_y)
        scale_factor = min_scale + (max_scale - min_scale) * progress
        
        return self.base_scale * scale_factor
   
    def delete(self):
        sprites.remove(self)

    def draw(self, screen):
        if self.entity is None:
            return
        
        from components.animator import Animator
        animator = self.entity.get(Animator)
        
        # Si hay animator, usar su frame actual en lugar de la imagen estática
        if animator:
            image_to_draw = animator.get_current_frame()
        elif self.original_image:
            image_to_draw = self.original_image
        else:
            return  # No hay nada que dibujar
        
        # Calcular la escala actual basada en la profundidad
        current_scale = self.get_depth_scale_factor()
        
        # CRÍTICO: Escalar la imagen correcta (image_to_draw, NO self.original_image)
        new_width = int(image_to_draw.get_width() * current_scale)
        new_height = int(image_to_draw.get_height() * current_scale)
        scaled_image = pygame.transform.scale(image_to_draw, (new_width, new_height))
        
        # Calcular la posición de dibujo basándose en el punto de anclaje
        draw_x = self.entity.x - (new_width / 2)
        draw_y = self.entity.y - (new_height * self.anchor_y_ratio)
        
        # Aplicar el offset de la cámara y dibujar
        screen.blit(scaled_image, (draw_x - camera.x, draw_y - camera.y))
    
    def get_draw_order(self):
        """Retorna la posición Y para ordenar por profundidad."""
        if self.entity is None:
            return 0
        
        if self.draw_order_override != 0:
            return self.draw_order_override
        
        return self.entity.y if self.entity else 0
