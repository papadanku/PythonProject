
"""
This module formats an application's Vertex Array Objects (VAOs)
"""

# Import application modules
from shader_program import ShaderProgram
from vbo import VBO


class VAO:
    """
    Create and manage Vertex Array Objects for different shader programs.
    Formats vertex buffer data into renderable objects with attribute bindings.
    """

    def __init__(self, ctx):
        """
        Initialize VAO manager and create VAOs for all geometry types.

        Args:
            ctx: ModernGL context for VAO creation
        """
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # Generate a Cube VAO for a specified shader program
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cube'])

        # Generate a Cube VAO shadow-map for a specified shader program
        self.vaos['shadow_cube'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['cube'])

        # Generate a Cat VAO for a specified shader program
        self.vaos['cat'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cat'])

        # Generate a Cat VAO shadow-map for a specified shader program
        self.vaos['shadow_cat'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['cat'])

        # Generate a SkyBox VAO for a specified shader program
        self.vaos['skybox'] = self.get_vao(
            program=self.program.programs['skybox'],
            vbo=self.vbo.vbos['skybox'])

        # Generate an advanced SkyBox VAO for a specified shader program
        self.vaos['advanced_skybox'] = self.get_vao(
            program=self.program.programs['advanced_skybox'],
            vbo=self.vbo.vbos['advanced_skybox'])

    def get_vao(self, program, vbo):
        """
        Format VBO data into renderable VAO for specific shader.

        Args:
            program: Shader program to use for rendering
            vbo: Vertex buffer object containing geometry data

        Returns:
            Vertex array object ready for rendering
        """
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)
        return vao

    def destroy(self):
        """
        Release VBO and shader program resources.
        Clean up all VAO-related resources when destroyed.
        """
        self.vbo.destroy()
        self.program.destroy()
