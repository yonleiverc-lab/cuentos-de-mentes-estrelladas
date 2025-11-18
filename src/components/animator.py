import pygame
import os

loaded_animations = {}  # Cache global para animaciones


class Animator:
    def __init__(self, base_path, scale_factor=1.0):
        self.entity = None
        self.base_path = base_path
        self.scale_factor = scale_factor
        self.animations = self._load_animations()
        self.current_animation = 'front_idle'
        self.frame_index = 0
        self.animation_speed = 0.3  # Velocidad de animación
        self.frame_timer = 0
        self.facing_direction = 'front'  # front, back, left, right
        self.is_moving = False
    
    def _scale_image(self, image):
        new_width = max(1, int(image.get_width() * self.scale_factor))
        new_height = max(1, int(image.get_height() * self.scale_factor))
        return pygame.transform.smoothscale(image, (new_width, new_height))
    
    def _load_walk_sequence(self, folder_name, count):
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
        try:
            back_idle_image = pygame.image.load(back_idle_path).convert_alpha()
            back_idle_image = self._scale_image(back_idle_image)
        except:
            back_idle_image = front_idle_image
        animations['back_idle'] = [back_idle_image]
        
        # Right/Left idle
        right_left_idle_path = os.path.join(self.base_path, 'Idle', 'Right_Left.png')
        try:
            right_idle_image = pygame.image.load(right_left_idle_path).convert_alpha()
            right_idle_image = self._scale_image(right_idle_image)
        except:
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
        animations['front_attack'] = attack_frames if attack_frames else [front_idle_image]
        animations['back_attack'] = attack_frames if attack_frames else [back_idle_image]
        animations['right_attack'] = attack_frames if attack_frames else [right_idle_image]
        animations['left_attack'] = [pygame.transform.flip(f, True, False) for f in attack_frames] if attack_frames else [front_idle_image]
        print(f"✓ Attack animations loaded (11 frames)")

        print(f"=== Animation loading complete ===\n")
        loaded_animations[cache_key] = animations
        return animations

                
    def update(self, dt=1.0):

        self.frame_timer += self.animation_speed * dt

        if self.frame_timer >= 1.0:
            self.frame_timer = 0
            current_frames = self.animations.get(self.current_animation, self.animations['front_idle'])

            if len(current_frames) > 0:
                old_index = self.frame_index
                self.frame_index = (self.frame_index + 1) % len(current_frames)

                if 'attack' in self.current_animation and self.frame_index == 0:
                    print(f" Frame {old_index} -> {self.frame_index} de {len(current_frames)}")
                    # Si la animación de ataque terminó, volver a idle o walk
                    if self.is_moving:
                        self.set_movement_state(True)
                    else:
                        self.set_movement_state(False)
    
    def set_movement_state(self, is_moving, direction=None):
        old_animation = self.current_animation
        self.is_moving = is_moving
        if direction:
            self.facing_direction = direction
        if is_moving:
            self.current_animation = f'{self.facing_direction}_walk'
        else:
            self.current_animation = f'{self.facing_direction}_idle'
        if self.current_animation not in self.animations:
            self.current_animation = 'front_idle'
        if old_animation != self.current_animation:
            self.frame_index = 0
            self.frame_timer = 0

    def set_attack_state(self, is_attacking, direction=None):
        old_animation = self.current_animation

        if direction:
            self.facing_direction = direction

        if is_attacking:
            self.current_animation = f'{self.facing_direction}_attack'
            self.animation_speed = 1.5  # Velocidad del ataque (ajusta si es muy rápido/lento)
            print(f" cambiando a animación: {self.current_animation}")
        else:
            self.current_animation = f'{self.facing_direction}_idle'
            self.animation_speed = 0.3  # Velocidad normal
            print(f" volviendo a idle: {self.current_animation}")

        if self.current_animation not in self.animations:
            self.current_animation = 'front_attack' if is_attacking else 'front_idle'
            print(f" animacion no encontrada, usando fallback: {self.current_animation}")

        if old_animation != self.current_animation:
            self.frame_index = 0
            self.frame_timer = 0
            print(f" Reset: frame_index=0, frame_timer=0")
    
    def get_current_frame(self):
        current_frames = self.animations.get(self.current_animation, self.animations.get('front_idle', []))
        if not current_frames:
            placeholder = pygame.Surface((30, 60), pygame.SRCALPHA)
            placeholder.fill((255, 0, 0, 150))
            return placeholder
        self.frame_index = max(0, min(self.frame_index, len(current_frames) - 1))
        return current_frames[self.frame_index]