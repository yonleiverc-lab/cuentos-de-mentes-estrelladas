import pygame
import os

loaded_animations = {}  # Cache global para animaciones

class Animator:
    def __init__(self, base_path, scale_factor=1.0):
        self.entity = None
        self.base_path = base_path
        self.scale_factor = scale_factor
        self.animations = self._load_animations()
        
        # Estado de animación
        self.current_animation = 'front_idle'
        self.frame_index = 0
        self.animation_speed = 0.3  # Velocidad de animación
        self.frame_timer = 0
        
        # Dirección del personaje
        self.facing_direction = 'front'  # front, back, left, right
        self.is_moving = False
    
    def _scale_image(self, image):
        """Escala una imagen según el scale_factor"""
        new_width = max(1, int(image.get_width() * self.scale_factor))
        new_height = max(1, int(image.get_height() * self.scale_factor))
        return pygame.transform.smoothscale(image, (new_width, new_height))
    
    def _load_walk_sequence(self, folder_name, count):
        """Carga una secuencia de frames de caminata"""
        frames = []
        folder_path = os.path.join(self.base_path, folder_name)
        
        print(f"Loading walk sequence from: {folder_path}")  # Debug
        
        for i in range(1, count + 1):
            file_path = os.path.join(folder_path, f'{i}.png')
            try:
                image = pygame.image.load(file_path).convert_alpha()
                image = self._scale_image(image)
                frames.append(image)
                print(f"  ✓ Loaded: {file_path}")  # Debug
            except Exception as e:
                print(f"  ✗ Failed to load {file_path}: {e}")  # Debug
                # Si falla, crear un placeholder
                placeholder = pygame.Surface((30, 60), pygame.SRCALPHA)
                placeholder.fill((255, 0, 255, 100))
                placeholder = self._scale_image(placeholder)
                frames.append(placeholder)
        
        return frames
    
    def _load_animations(self):
        """Carga todas las animaciones del personaje"""
        # Verificar si ya están cargadas en el cache
        cache_key = f"{self.base_path}_{self.scale_factor}"
        if cache_key in loaded_animations:
            print(f"Using cached animations for {cache_key}")
            return loaded_animations[cache_key]
        
        print(f"\n=== Loading animations from base path: {self.base_path} ===")
        
        animations = {}
        
        # Front idle - SOLO agregar la ruta relativa al base_path
        front_idle_path = os.path.join(self.base_path, 'Idle', 'Front.png')
        print(f"Loading front_idle from: {front_idle_path}")
        try:
            front_idle_image = pygame.image.load(front_idle_path).convert_alpha()
            front_idle_image = self._scale_image(front_idle_image)
            print("  ✓ Front idle loaded successfully")
        except Exception as e:
            print(f"  ✗ Failed to load front idle: {e}")
            front_idle_image = pygame.Surface((30, 60), pygame.SRCALPHA)
            front_idle_image.fill((0, 0, 255, 150))
            front_idle_image = self._scale_image(front_idle_image)
        
        animations['front_idle'] = [front_idle_image]
        
        # Back idle
        back_idle_path = os.path.join(self.base_path, 'Idle', 'Back.png')
        print(f"Loading back_idle from: {back_idle_path}")
        try:
            back_idle_image = pygame.image.load(back_idle_path).convert_alpha()
            back_idle_image = self._scale_image(back_idle_image)
            print("  ✓ Back idle loaded successfully")
        except Exception as e:
            print(f"  ✗ Failed to load back idle: {e}")
            back_idle_image = front_idle_image
        
        animations['back_idle'] = [back_idle_image]
        
        # Right/Left idle
        right_left_idle_path = os.path.join(self.base_path, 'Idle', 'Right_Left.png')
        print(f"Loading right/left idle from: {right_left_idle_path}")
        try:
            right_idle_image = pygame.image.load(right_left_idle_path).convert_alpha()
            right_idle_image = self._scale_image(right_idle_image)
            print("  ✓ Right/Left idle loaded successfully")
        except Exception as e:
            print(f"  ✗ Failed to load right/left idle: {e}")
            right_idle_image = front_idle_image
        
        animations['right_idle'] = [right_idle_image]
        animations['left_idle'] = [pygame.transform.flip(right_idle_image, True, False)]
        
        # Walk animations - SOLO la subcarpeta relativa
        walk_frames_right = self._load_walk_sequence('Right_Left_Walk', 16)
        animations['right_walk'] = walk_frames_right
        animations['left_walk'] = [pygame.transform.flip(f, True, False) for f in walk_frames_right]
        
        walk_frames_front = self._load_walk_sequence('Front_Walk', 12)
        animations['front_walk'] = walk_frames_front if walk_frames_front else [front_idle_image]
        
        # Back walk (placeholder por ahora)
        walk_frames_back = self._load_walk_sequence('Back_Walk', 10)
        animations['back_walk'] = walk_frames_back if walk_frames_back else [front_idle_image]
        
        # Attack animations - 11 frames
        print("Loading attack animations...")
        attack_frames = self._load_walk_sequence('Attack', 11)  # 11 frames de ataque

        # Usar los mismos frames para todas las direcciones (con flip para izquierda)
        animations['front_attack'] = attack_frames if attack_frames else [front_idle_image]
        animations['back_attack'] = attack_frames if attack_frames else [back_idle_image]
        animations['right_attack'] = attack_frames if attack_frames else [right_idle_image]
        animations['left_attack'] = [pygame.transform.flip(f, True, False) for f in attack_frames] if attack_frames else [front_idle_image]

        print(f"✓ Attack animations loaded (11 frames)")
        print(f"=== Animation loading complete ===\n")
        
        # Guardar en cache
        loaded_animations[cache_key] = animations
        
        return animations

                
    def update(self, dt=1.0):
        """Actualiza la animación actual"""
        # Avanzar el timer de frames
        self.frame_timer += self.animation_speed * dt
        
        # Si es momento de cambiar de frame
        if self.frame_timer >= 1.0:
            self.frame_timer = 0
            current_frames = self.animations.get(self.current_animation, self.animations['front_idle'])
            
            # IMPORTANTE: Avanzar el frame y hacer wrap con el tamaño actual de la animación
            if len(current_frames) > 0:
                self.frame_index = (self.frame_index + 1) % len(current_frames)
    
    def set_movement_state(self, is_moving, direction=None):
        """
        Actualiza el estado de movimiento y dirección
        
        Args:
            is_moving: Si el personaje se está moviendo
            direction: 'front', 'back', 'left', 'right' o None
        """
        old_animation = self.current_animation
        
        self.is_moving = is_moving
        
        if direction:
            self.facing_direction = direction
        
        # Determinar la animación correcta
        if is_moving:
            self.current_animation = f'{self.facing_direction}_walk'
        else:
            self.current_animation = f'{self.facing_direction}_idle'
        
        # Si la animación no existe, usar front_idle como fallback
        if self.current_animation not in self.animations:
            self.current_animation = 'front_idle'
        
        # CRÍTICO: Si cambiamos de animación, resetear el frame_index
        if old_animation != self.current_animation:
            self.frame_index = 0
            self.frame_timer = 0

    def set_attack_state(self, is_attacking, direction=None):
        """Actualiza el estado de ataque
        Args:
         is_attacking: Si el personaje está atacando
         direction: 'front', 'back', 'left', 'right' o None
        """
        old_animation = self.current_animation
    
        if direction:
            self.facing_direction = direction
    
        if is_attacking:
        # Cambiar a animación de ataque
            self.current_animation = f'{self.facing_direction}_attack'
            self.animation_speed = 0.4  # Velocidad del ataque (ajusta si es muy rápido/lento)
        else:
        # Volver a idle cuando termina el ataque
            self.current_animation = f'{self.facing_direction}_idle'
            self.animation_speed = 0.3  # Velocidad normal
    
    # Si la animación no existe, usar front_attack como fallback
        if self.current_animation not in self.animations:
           self.current_animation = 'front_attack' if is_attacking else 'front_idle'
    
    # Si cambiamos de animación, resetear el frame_index
        if old_animation != self.current_animation:
            self.frame_index = 0
            self.frame_timer = 0
    
    def get_current_frame(self):
        """Retorna el frame actual de la animación"""
        # Obtener los frames de la animación actual, con fallback a front_idle
        current_frames = self.animations.get(self.current_animation, self.animations.get('front_idle', []))
        
        # Si no hay frames (no debería pasar), crear un placeholder
        if not current_frames:
            placeholder = pygame.Surface((30, 60), pygame.SRCALPHA)
            placeholder.fill((255, 0, 0, 150))
            return placeholder
        
        # CRÍTICO: Asegurar que el frame_index esté dentro del rango válido
        # Esto protege contra el IndexError
        self.frame_index = max(0, min(self.frame_index, len(current_frames) - 1))
        
        return current_frames[self.frame_index]