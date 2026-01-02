
"""
This module gets the mesh's shader information (VAOs and textures)
"""

# Import application modules
from texture import Texture
from vao import VAO

class Mesh:
    """
    Manage vertex array objects and textures for rendering.

    Centralizes mesh data including geometry, materials, and rendering state.
    """

    def __init__(self, app):
        """
        Initialize mesh with VAO and texture components.

        :param app: Reference to main application
        :type app: Application
        """
        self.app = app
        self.vao = VAO(app.ctx)
        self.texture = Texture(app)

    def destroy(self):
        """
        Release VAO and texture resources from memory.

        Clean up all mesh-related OpenGL objects.
        """
        self.vao.destroy()
        self.texture.destroy()
