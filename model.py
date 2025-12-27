
"""
This module processes uniform attributes for the appropriate model
"""

# Import Python modules
if __name__ == '__main__':
    import glm


class BaseModel:
    """
    Base class for all 3D models with position, rotation, and scale.
    Provides fundamental model matrix calculations and rendering functionality.
    """

    def __init__(self, app, vao_name, tex_id, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        """
        Initialize base model with transformation properties and rendering data.

        :param app: Reference to main application
        :type app: Application
        :param vao_name: Name of vertex array object to use
        :type vao_name: str
        :param tex_id: Texture identifier
        :type tex_id: str
        :param pos: Position in world coordinates (x, y, z)
        :type pos: tuple
        :param rot: Rotation in degrees (x, y, z)
        :type rot: tuple
        :param scale: Scale factors (x, y, z)
        :type scale: tuple
        """
        self.app = app
        self.pos = pos
        self.vao_name = vao_name
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self):
        """
        Update model state before rendering.
        Subclasses override this method for custom behavior.
        """

        pass

    def get_model_matrix(self):
        """
        Calculate model matrix combining translation, rotation, and scale.

        :return: Model transformation matrix
        :rtype: mat4
        """
        # NOTE: This is just an identity matrix
        m_model = glm.mat4()
        # Translate
        m_model = glm.translate(m_model, self.pos)
        # Rotate
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        # Scale
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def render(self):
        """
        Update model state and render using associated VAO.
        """
        self.update()
        self.vao.render()


class ExtendedBaseModel(BaseModel):
    """
    Subclass for an application's main objects
    """

    def __init__(self, app, vao_name, tex_id, pos, rot, scale):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.on_init()

    def update(self):
        """
        Update dynamic uniform attributes
        """

        self.texture.use(location=0)
        self.program['camPos'].write(self.camera.position)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)

    def update_shadow(self):
        self.shadow_program['m_model'].write(self.m_model)

    def render_shadow(self):
        self.update_shadow()
        self.shadow_vao.render()

    def on_init(self):
        self.program['m_view_light'].write(self.app.light.m_view_light)
        # Viewport resolution
        self.program['u_resolution'].write(glm.vec2(self.app.WIN_SIZE))
        # Depth texture
        self.depth_texture = self.app.mesh.texture.textures['depth_texture']
        self.program['shadowMap'] = 1
        self.depth_texture.use(location=1)
        # Shadow
        self.shadow_vao = self.app.mesh.vao.vaos['shadow_' + self.vao_name]
        self.shadow_program = self.shadow_vao.program
        self.shadow_program['m_proj'].write(self.camera.m_proj)
        self.shadow_program['m_view_light'].write(self.app.light.m_view_light)
        self.shadow_program['m_model'].write(self.m_model)
        # Texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_0'] = 0
        self.texture.use(location=0)
        # Matrices
        # NOTE: .write(x) is a function that gives the shader program a specified attribute
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # Light uniform attributes
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)


class Cube(ExtendedBaseModel):
    """
    Basic cube model with texture and lighting support.
    """

    def __init__(self, app, vao_name='cube', tex_id=0, pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        """
        Initialize cube model with default parameters.

        :param app: Reference to main application
        :type app: Application
        :param vao_name: Name of vertex array object (default: 'cube')
        :type vao_name: str
        :param tex_id: Texture identifier (default: 0)
        :type tex_id: int
        :param pos: Position in world coordinates (default: origin)
        :type pos: tuple
        :param rot: Rotation in degrees (default: no rotation)
        :type rot: tuple
        :param scale: Scale factors (default: unit scale)
        :type scale: tuple
        """
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class MovingCube(Cube):
    """
    Animated cube that rotates continuously.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize moving cube with same parameters as base cube.
        """
        super().__init__(*args, **kwargs)

    def update(self):
        """
        Update cube rotation based on application time.
        Creates continuous spinning animation.
        """
        self.m_model = self.get_model_matrix()
        super().update()


class Cat(ExtendedBaseModel):
    """
    Cat model with specific orientation and texture.
    """

    def __init__(self, app, vao_name='cat', tex_id='cat',
                 pos=(0, 0, 0), rot=(-90, 0, 0), scale=(1, 1, 1)):
        """
        Initialize cat model with default orientation.

        :param app: Reference to main application
        :type app: Application
        :param vao_name: Name of vertex array object (default: 'cat')
        :type vao_name: str
        :param tex_id: Texture identifier (default: 'cat')
        :type tex_id: str
        :param pos: Position in world coordinates (default: origin)
        :type pos: tuple
        :param rot: Rotation in degrees (default: -90° X rotation)
        :type rot: tuple
        :param scale: Scale factors (default: unit scale)
        :type scale: tuple
        """
        super().__init__(app, vao_name, tex_id, pos, rot, scale)


class SkyBox(BaseModel):
    """
    Basic skybox that renders a cubemap texture.
    Uses simplified view matrix to prevent skybox rotation with camera.
    """

    def __init__(self, app, vao_name='skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        """
        Initialize skybox with cubemap texture.

        :param app: Reference to main application
        :type app: Application
        :param vao_name: Name of vertex array object (default: 'skybox')
        :type vao_name: str
        :param tex_id: Texture identifier (default: 'skybox')
        :type tex_id: str
        :param pos: Position in world coordinates (default: origin)
        :type pos: tuple
        :param rot: Rotation in degrees (default: no rotation)
        :type rot: tuple
        :param scale: Scale factors (default: unit scale)
        :type scale: tuple
        """
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        # NOTE: Initialize the model's attributes here
        self.on_init()

    def update(self):
        """
        Update skybox view matrix to remove camera rotation.
        Prevents skybox from rotating with camera movement.
        """
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))

    def on_init(self):
        """
        Initialize skybox textures and matrices.
        Sets up cubemap texture and projection/view matrices.
        """
        # Assign uniform textures to a shader program
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
        # Assign uniform matrices to a shader program
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['m_view'].write(glm.mat4(glm.mat3(self.camera.m_view)))


class AdvancedSkyBox(BaseModel):
    """
    Advanced skybox with proper perspective projection.
    Uses inverse projection-view matrix for accurate cubemap sampling.
    """

    def __init__(self, app, vao_name='advanced_skybox', tex_id='skybox',
                 pos=(0, 0, 0), rot=(0, 0, 0), scale=(1, 1, 1)):
        """
        Initialize advanced skybox with cubemap texture.

        :param app: Reference to main application
        :type app: Application
        :param vao_name: Name of vertex array object (default: 'advanced_skybox')
        :type vao_name: str
        :param tex_id: Texture identifier (default: 'skybox')
        :type tex_id: str
        :param pos: Position in world coordinates (default: origin)
        :type pos: tuple
        :param rot: Rotation in degrees (default: no rotation)
        :type rot: tuple
        :param scale: Scale factors (default: unit scale)
        :type scale: tuple
        """
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        # NOTE: Initialize the model's attributes here
        self.on_init()

    def update(self):
        """
        Update inverse projection-view matrix for proper cubemap sampling.
        Converts clip coordinates back to world space for accurate texture lookup.
        """
        m_view = glm.mat4(glm.mat3(self.camera.m_view))
        self.program['m_invProjView'].write(glm.inverse(self.camera.m_proj * m_view))

    def on_init(self):
        """
        Initialize skybox textures.
        Sets up cubemap texture for advanced rendering.
        """
        # Assign uniform textures to a shader program
        self.texture = self.app.mesh.texture.textures[self.tex_id]
        self.program['u_texture_skybox'] = 0
        self.texture.use(location=0)
