import pygame
import os

class AttackController:
    """Controla los ataques del jugador"""
    
    def __init__(self):
        self.entity = None
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_cooldown_max = 20  # frames (aproximadamente 0.5 segundos)
        self.attack_duration = 33  # frames que dura la animación de ataque
        self.attack_timer = 0
        self.attack_damage = 10
        self.attack_range = 80  # Alcance del ataque en píxeles
        
        # Hitbox del ataque (se ajusta según la dirección)
        self.attack_hitbox = None
    
    def can_attack(self):
        """Verifica si el jugador puede atacar"""
        return not self.is_attacking and self.attack_cooldown <= 0
    
    def start_attack(self, direction='front'):
        """Inicia un ataque en la dirección especificada"""
        if not self.can_attack():
            return False
        
        self.is_attacking = True
        self.attack_timer = self.attack_duration
        self.attack_cooldown = self.attack_cooldown_max
        
        # Crear hitbox de ataque según la dirección
        self._create_attack_hitbox(direction)
        
        # Aquí podrías reproducir un sonido de ataque
        print(f"¡Ataque {direction}!")
        
        return True
    
    def _create_attack_hitbox(self, direction):
        """Crea el hitbox del ataque según la dirección"""
        if self.entity is None:
            return
        
        x = self.entity.x
        y = self.entity.y
        
        # Ajustar hitbox según dirección
        if direction == 'front':
            self.attack_hitbox = pygame.Rect(
                x - self.attack_range // 2,
                y,
                self.attack_range,
                self.attack_range
            )
        elif direction == 'back':
            self.attack_hitbox = pygame.Rect(
                x - self.attack_range // 2,
                y - self.attack_range,
                self.attack_range,
                self.attack_range
            )
        elif direction == 'left':
            self.attack_hitbox = pygame.Rect(
                x - self.attack_range,
                y - self.attack_range // 2,
                self.attack_range,
                self.attack_range
            )
        elif direction == 'right':
            self.attack_hitbox = pygame.Rect(
                x,
                y - self.attack_range // 2,
                self.attack_range,
                self.attack_range
            )
    
    def update(self, animator=None):
        """Actualiza el estado del ataque"""
        # Reducir cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Actualizar timer de ataque
        if self.is_attacking:
            self.attack_timer -= 1
            
            if self.attack_timer <= 0:
                self.is_attacking = False
                self.attack_hitbox = None
                # Resetear animación a idle
            if animator:
                animator.set_attack_state(False)
    
    def check_hit(self, target_x, target_y, target_width=50, target_height=50):
        """
        Verifica si el ataque golpea a un objetivo
        
        Args:
            target_x, target_y: Posición del objetivo
            target_width, target_height: Tamaño del objetivo
        
        Returns:
            bool: True si el ataque golpea al objetivo
        """
        if not self.is_attacking or self.attack_hitbox is None:
            return False
        
        target_rect = pygame.Rect(
            target_x - target_width // 2,
            target_y - target_height // 2,
            target_width,
            target_height
        )
        
        return self.attack_hitbox.colliderect(target_rect)
    
    def draw_debug(self, screen):
        """Dibuja el hitbox del ataque (para debug)"""
        from core.camera import camera
        
        if self.attack_hitbox and self.is_attacking:
            debug_rect = pygame.Rect(
                self.attack_hitbox.x - camera.x,
                self.attack_hitbox.y - camera.y,
                self.attack_hitbox.width,
                self.attack_hitbox.height
            )
            pygame.draw.rect(screen, (255, 0, 0, 128), debug_rect, 3)


class AttackAnimation:
    """Maneja la animación visual del ataque"""
    
    def __init__(self):
        self.active = False
        self.particles = []
        self.slash_frames = []
        self.current_frame = 0
        self.frame_timer = 0
        self.position = (0, 0)
        self.direction = 'front'
    
    def start(self, x, y, direction):
        """Inicia la animación de ataque"""
        self.active = True
        self.position = (x, y)
        self.direction = direction
        self.current_frame = 0
        self.frame_timer = 0
        
        # Crear partículas de efecto
        self._create_particles(x, y, direction)
    
    def _create_particles(self, x, y, direction):
        """Crea partículas para el efecto de ataque"""
        import random
        
        self.particles = []
        num_particles = 8
        
        for i in range(num_particles):
            angle = 0
            if direction == 'front':
                angle = random.uniform(-30, 30) + 90
            elif direction == 'back':
                angle = random.uniform(-30, 30) - 90
            elif direction == 'left':
                angle = random.uniform(-30, 30) + 180
            elif direction == 'right':
                angle = random.uniform(-30, 30)
            
            speed = random.uniform(3, 8)
            dx = speed * pygame.math.Vector2(1, 0).rotate(angle).x
            dy = speed * pygame.math.Vector2(1, 0).rotate(angle).y
            
            self.particles.append({
                'x': x,
                'y': y,
                'dx': dx,
                'dy': dy,
                'life': 15,
                'size': random.randint(3, 6)
            })
    
    def update(self):
        """Actualiza la animación"""
        if not self.active:
            return
        
        # Actualizar partículas
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            particle['size'] = max(1, particle['size'] - 0.2)
            
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Si no hay más partículas, terminar animación
        if len(self.particles) == 0:
            self.active = False
    
    def draw(self, screen):
        """Dibuja la animación de ataque"""
        from core.camera import camera
        
        if not self.active:
            return
        
        # Dibujar partículas
        for particle in self.particles:
            screen_x = int(particle['x'] - camera.x)
            screen_y = int(particle['y'] - camera.y)
            size = int(particle['size'])
            
            # Color de la partícula (efecto de hacha/metal)
            alpha = int(255 * (particle['life'] / 15))
            color = (200, 200, 255, alpha)
            
            pygame.draw.circle(screen, color[:3], (screen_x, screen_y), size)


# Instancias globales
attack_animation = AttackAnimation()