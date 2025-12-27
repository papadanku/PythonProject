
"""
This module initializes the main graphics application
"""

# Import Python modules
if __name__ == '__main__':
    import moderngl as mgl
    import pygame as pg
    import sys

# Import application modules
from camera import Camera
from light import Light
from mesh import Mesh
from model import *
from scene import Scene
from scene_renderer import SceneRenderer

class GraphicsEngine():
    """
    Main graphics engine that initializes OpenGL context, manages game loop, and coordinates all rendering components.
    Handles window creation, input processing, and rendering pipeline execution.
    """

    def __init__(self, win_size=(1600, 900)):
        """
        Initialize graphics engine with specified window size, OpenGL context, and core components.

        Args:
            win_size: Tuple containing window width and height in pixels (default: 1600x900)
        """
        # Initialize PyGame modules
        pg.init()
        # Initialize window size
        self.WIN_SIZE = win_size
        # Set OpenGL attributes
        # NOTE: This application uses OpenGL 3.3 Core
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # Create OpenGL context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        # Mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        # Detect and use existing OpenGL context
        # NOTE: Contexts provides API functions such renderstates, buffers, etc.
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        # Create an object to help track time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        # Create light data (positions, transformation)
        self.light = Light()
        # Create camera data (positions, transformations)
        self.camera = Camera(self)
        # Create mesh data (VBOs, VAOs, shader programs, textures)
        self.mesh = Mesh(self)
        # Accumulate required objects into a Scene
        self.scene = Scene(self)
        # Render the accumulated objects from the Scene
        self.scene_renderer = SceneRenderer(self)

    def get_time(self):
        """
        Update current time in seconds since application start.
        Converts milliseconds to seconds for consistent time units.
        """
        self.time = pg.time.get_ticks() * 0.001

    def check_events(self):
        """
        Process PyGame events and handle window close/escape key.
        Cleans up resources and exits application when quit event occurs.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                # Release everything from memory
                self.mesh.destroy()
                self.scene_renderer.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        """
        Clear framebuffer, render scene, and swap buffers.
        Sets background color and executes complete rendering pipeline.
        """
        # Clear framebuffer
        self.ctx.clear(color=(0.08, 0.16, 0.18))
        # Render scene
        self.scene_renderer.render()
        # Swap buffers
        pg.display.flip()

    def run(self):
        """
        Main game loop that updates time, processes events, updates camera, and renders scene.
        Runs at 60 FPS and maintains consistent delta time for smooth animations.
        """
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()
