import pygame
from components.physics import Body

class NPC:
    """Componente para personajes no jugadores"""
    
    def __init__(self, name, dialogues, interaction_distance=50):
        """
        Args:
            name: Nombre del NPC
            dialogues: Lista de tuplas (nombre, texto) para el diálogo
                      Ejemplo: [("Tabernero", "¡Bienvenido!"), ("Tabernero", "¿Qué deseas?")]
            interaction_distance: Distancia máxima para interactuar
        """
        self.entity = None
        self.name = name
        self.dialogues = dialogues
        self.interaction_distance = interaction_distance
        self.player_nearby = False
        self.has_talked = False  # Para diálogos únicos
        
        # Visual
        self.show_prompt = False
        self.prompt_alpha = 0
        self.prompt_font = None
    
    def _init_font(self):
        """Inicializa la fuente de forma perezosa"""
        if self.prompt_font is None:
            self.prompt_font = pygame.font.Font(None, 28)
    
    def update(self):
        """Actualiza el estado del NPC cada frame"""
        from core.input import is_key_pressed
        from components.dialogue import dialogue_box
        from components.player import Player
        from components.entity import active_objs
        
        if self.entity is None:
            return
        
        # Buscar al jugador
        player_entity = None
        for obj in active_objs:
            if isinstance(obj, Player):
                player_entity = obj.entity
                break
        
        if player_entity is None:
            return
        
        # Calcular distancia al jugador
        distance = self._calculate_distance(player_entity)
        
        # Verificar si el jugador está cerca
        self.player_nearby = distance <= self.interaction_distance
        self.show_prompt = self.player_nearby and not dialogue_box.active
        
        # Animar el prompt (efecto pulsante)
        if self.show_prompt:
            self.prompt_alpha = min(255, self.prompt_alpha + 15)
        else:
            self.prompt_alpha = max(0, self.prompt_alpha - 15)
        
        # Interacción con tecla E
        if self.player_nearby and is_key_pressed(pygame.K_e):
            if not dialogue_box.active:
                self._start_dialogue()
    
    def _calculate_distance(self, player_entity):
        """Calcula la distancia entre el NPC y el jugador"""
        dx = self.entity.x - player_entity.x
        dy = self.entity.y - player_entity.y
        return (dx**2 + dy**2)**0.5
    
    def _start_dialogue(self):
        """Inicia el diálogo con el jugador"""
        from components.dialogue import dialogue_box
        
        # Si ya habló y solo quieres que hable una vez, puedes descomentar esto:
        # if self.has_talked:
        #     return
        
        dialogue_box.start_dialogue(self.dialogues)
        self.has_talked = True
        print(f"💬 Iniciando diálogo con {self.name}")
    
    def draw_prompt(self, screen):
        """Dibuja el indicador de interacción sobre el NPC"""
        from core.camera import camera
        
        if not self.show_prompt or self.prompt_alpha <= 0:
            return
        
        self._init_font()
        
        # Posición en pantalla (sobre el NPC)
        screen_x = self.entity.x - camera.x
        screen_y = self.entity.y - camera.y - 80  # Elevado sobre el NPC
        
        # Texto
        text = "[E] Hablar"
        text_surface = self.prompt_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_x, screen_y))
        
        # Fondo semi-transparente
        padding = 10
        bg_width = text_rect.width + padding * 2
        bg_height = text_rect.height + padding * 2
        bg_x = text_rect.x - padding
        bg_y = text_rect.y - padding
        
        # Crear superficie con alpha
        bg_surface = pygame.Surface((bg_width, bg_height), pygame.SRCALPHA)
        alpha = int(self.prompt_alpha * 0.8)
        bg_surface.fill((20, 20, 40, alpha))
        screen.blit(bg_surface, (bg_x, bg_y))
        
        # Borde con animación pulsante
        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500
        border_alpha = int(150 + 105 * pulse)
        border_color = (255, 220, 100, min(border_alpha, self.prompt_alpha))
        
        # Dibujar borde (simulado con rectángulos)
        border_thickness = 2
        for i in range(border_thickness):
            border_rect = pygame.Rect(bg_x + i, bg_y + i, bg_width - i*2, bg_height - i*2)
            pygame.draw.rect(screen, border_color[:3], border_rect, 1, border_radius=8)
        
        # Dibujar texto con alpha
        text_with_alpha = text_surface.copy()
        text_with_alpha.set_alpha(self.prompt_alpha)
        screen.blit(text_with_alpha, text_rect)


class NPCBehavior:
    """Comportamientos adicionales para NPCs (patrullar, mirar al jugador, etc.)"""
    
    def __init__(self, behavior_type="idle"):
        """
        Args:
            behavior_type: Tipo de comportamiento
                - "idle": Quedarse quieto
                - "wander": Caminar aleatoriamente
                - "patrol": Patrullar entre puntos
                - "look_at_player": Mirar hacia el jugador cuando está cerca
        """
        self.entity = None
        self.behavior_type = behavior_type
        self.patrol_points = []
        self.current_patrol_index = 0
        self.wander_timer = 0
        self.wander_direction = None
    
    def set_patrol_points(self, points):
        """
        Define puntos de patrullaje
        Args:
            points: Lista de tuplas (x, y)
        """
        self.patrol_points = points
        self.current_patrol_index = 0
    
    def update(self):
        """Actualiza el comportamiento del NPC"""
        if self.entity is None:
            return
        
        from components.animator import Animator
        animator = self.entity.get(Animator)
        
        if self.behavior_type == "idle":
            self._idle_behavior(animator)
        
        elif self.behavior_type == "look_at_player":
            self._look_at_player_behavior(animator)
        
        elif self.behavior_type == "patrol":
            self._patrol_behavior(animator)
        
        elif self.behavior_type == "wander":
            self._wander_behavior(animator)
    
    def _idle_behavior(self, animator):
        """Comportamiento: quedarse quieto"""
        if animator:
            animator.set_movement_state(False)
    
    def _look_at_player_behavior(self, animator):
        """Comportamiento: mirar hacia el jugador cuando está cerca"""
        from components.player import Player
        from components.entity import active_objs
        from components.npc import NPC
        
        # Buscar al jugador
        player_entity = None
        for obj in active_objs:
            if isinstance(obj, Player):
                player_entity = obj.entity
                break
        
        if player_entity is None or animator is None:
            return
        
        # Obtener el componente NPC para verificar distancia
        npc_component = self.entity.get(NPC)
        if npc_component and npc_component.player_nearby:
            # Calcular dirección hacia el jugador
            dx = player_entity.x - self.entity.x
            dy = player_entity.y - self.entity.y
            
            # Determinar dirección
            if abs(dx) > abs(dy):
                direction = 'right' if dx > 0 else 'left'
            else:
                direction = 'front' if dy > 0 else 'back'
            
            animator.set_movement_state(False, direction)
        else:
            animator.set_movement_state(False)
    
    def _patrol_behavior(self, animator):
        """Comportamiento: patrullar entre puntos"""
        if not self.patrol_points or animator is None:
            return
        
        # Obtener punto de destino actual
        target = self.patrol_points[self.current_patrol_index]
        
        # Calcular distancia al punto
        dx = target[0] - self.entity.x
        dy = target[1] - self.entity.y
        distance = (dx**2 + dy**2)**0.5
        
        # Si llegó al punto, ir al siguiente
        if distance < 20:
            self.current_patrol_index = (self.current_patrol_index + 1) % len(self.patrol_points)
            return
        
        # Moverse hacia el punto
        speed = 1.5
        direction = None
        
        if abs(dx) > abs(dy):
            direction = 'right' if dx > 0 else 'left'
            self.entity.x += speed if dx > 0 else -speed
        else:
            direction = 'front' if dy > 0 else 'back'
            self.entity.y += speed if dy > 0 else -speed
        
        animator.set_movement_state(True, direction)
    
    def _wander_behavior(self, animator):
        """Comportamiento: caminar aleatoriamente"""
        import random
        
        if animator is None:
            return
        
        self.wander_timer -= 1
        
        # Cambiar dirección cada cierto tiempo
        if self.wander_timer <= 0:
            self.wander_timer = random.randint(60, 180)  # 1-3 segundos
            
            # 50% probabilidad de moverse o quedarse quieto
            if random.random() > 0.5:
                self.wander_direction = random.choice(['front', 'back', 'left', 'right'])
                animator.set_movement_state(True, self.wander_direction)
            else:
                self.wander_direction = None
                animator.set_movement_state(False)
        
        # Moverse en la dirección actual
        if self.wander_direction:
            speed = 0.5
            if self.wander_direction == 'front':
                self.entity.y += speed
            elif self.wander_direction == 'back':
                self.entity.y -= speed
            elif self.wander_direction == 'left':
                self.entity.x -= speed
            elif self.wander_direction == 'right':
                self.entity.x += speed