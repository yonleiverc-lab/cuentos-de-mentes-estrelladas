# scene_manager.py
import pygame
import sys
import os

# Scene imports
from tavern_scene import TavernScene
from village_scene import VillageScene

class SceneManager:
    def __init__(self):
        pygame.init()

        # Screen configuration
        self.WIDTH, self.HEIGHT = 1600, 900
        self.screen = pygame.display.set_mode(
            (self.WIDTH, self.HEIGHT),
            pygame.SCALED | pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        pygame.display.set_caption("Cuentos de Mentes Estrelladas - Demo 2.5D")

        self.clock = pygame.time.Clock()
        self.running = True

        # Create scene instances once and reuse them
        self.scenes = {
            "TavernScene": TavernScene(self),
            "VillageScene": VillageScene(self)
        }

        # Set the starting scene
        self.current_scene_name = "TavernScene"
        self.current_scene = self.scenes[self.current_scene_name]
        if hasattr(self.current_scene, "on_enter"):
            self.current_scene.on_enter()

    def change_scene(self, new_scene_name):
        # Ignore invalid names
        if new_scene_name not in self.scenes:
            print(f"[SceneManager] Ignoring unknown scene: {new_scene_name}")
            return

        # Call on_exit on the current scene if provided
        if hasattr(self.current_scene, "on_exit"):
            try:
                self.current_scene.on_exit()
            except Exception as e:
                print(f"[SceneManager] on_exit error: {e}")

        # Switch to the existing scene instance
        self.current_scene_name = new_scene_name
        self.current_scene = self.scenes[new_scene_name]

        # Call on_enter on the new scene if provided
        if hasattr(self.current_scene, "on_enter"):
            try:
                self.current_scene.on_enter()
            except Exception as e:
                print(f"[SceneManager] on_enter error: {e}")

    def _process_scene_command(self, cmd):
        """
        Accepts:
          - dict with key "change_to": {"change_to": "SceneName"}
          - plain string with scene name: "SceneName"
        Returns True if a valid change was processed.
        """
        if not cmd:
            return False

        # If scene returned a dict
        if isinstance(cmd, dict) and "change_to" in cmd:
            self.change_scene(cmd["change_to"])
            return True

        # If scene returned a plain string (legacy)
        if isinstance(cmd, str):
            self.change_scene(cmd)
            return True

        return False

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # seconds per frame, capped at 60 FPS

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                # Let the current scene handle the event and capture any command it returns
                if hasattr(self.current_scene, "handle_input"):
                    try:
                        result = self.current_scene.handle_input(event)
                    except Exception as e:
                        print(f"[SceneManager] handle_input error: {e}")
                        result = None
                    # If the scene returned a command (change scene), process it immediately
                    if self._process_scene_command(result):
                        # scene changed; skip remaining event handling for this frame
                        break

            if not self.running:
                break

            # Update current scene
            scene_command = None
            if hasattr(self.current_scene, "update"):
                try:
                    scene_command = self.current_scene.update(dt)
                except Exception as e:
                    print(f"[SceneManager] update error: {e}")
                    scene_command = None

            # Process any command returned by update (change scene)
            if self._process_scene_command(scene_command):
                # If the scene changed, continue to next loop (new scene will be drawn)
                pass

            # Draw current scene
            if hasattr(self.current_scene, "draw"):
                try:
                    self.current_scene.draw(self.screen)
                except Exception as e:
                    print(f"[SceneManager] draw error: {e}")

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    manager = SceneManager()
    manager.run()
