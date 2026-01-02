
"""
This module processes an application's vertex buffer objects (VBOs). VBOs are buffer objects we use for vertex processing.

In reality, we can use buffer objects for means outside of vertex processing.
"""

# Import Python modules
if __name__ == '__main__':
    import numpy as np
    import pywavefront


class VBO:
    def __init__(self, ctx):
        self.vbos = {}
        self.vbos['cube'] = CubeVBO(ctx)
        self.vbos['cat'] = CatVBO(ctx)
        self.vbos['skybox'] = SkyBoxVBO(ctx)
        self.vbos['advanced_skybox'] = AdvancedSkyBoxVBO(ctx)

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]


class BaseVBO:
    """
    Base class for vertex buffer objects.

    Provides common VBO functionality that subclasses extend with specific geometry.
    """

    def __init__(self, ctx):
        """
        Initialize base VBO with context and create vertex buffer.

        :param ctx: ModernGL context for buffer creation
        :type ctx: ModernGL context
        """
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format: str = None
        self.attribs: list = None

    def get_vertex_data(self):
        """
        Get vertex data for specific geometry.

        Subclasses override this method with geometry-specific implementation.
        """
        ...

    def get_vbo(self):
        """
        Create vertex buffer object from vertex data.

        :return: Vertex buffer object containing geometry data
        :rtype: VBO
        """
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def destroy(self):
        """
        Release vertex buffer resources.

        Clean up VBO when no longer needed.
        """
        self.vbo.release()


class CubeVBO(BaseVBO):
    """
    Cube vertex buffer object with texture coordinates and normals.

    Generates vertex data for a unit cube centered at origin.
    """

    def __init__(self, ctx):
        """
        Initialize cube VBO with vertex format and attributes.

        :param ctx: ModernGL context for buffer creation
        :type ctx: ModernGL context
        """
        super().__init__(ctx)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    @staticmethod
    def get_data(vertices, indices):
        """
        Extract vertex data from vertices using indices.

        :param vertices: List of vertex positions
        :type vertices: list
        :param indices: List of triangle indices
        :type indices: list
        :return: NumPy array of vertex data in order specified by indices
        :rtype: numpy.ndarray
        """
        # NOTE: Uses list comprehension to Outputs large list of tuples!
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self):
        """
        Generate complete vertex data for cube including positions, normals, and texture coordinates.

        :return: NumPy array containing interleaved vertex data
        :rtype: numpy.ndarray
        """
        # Get vertex coordinates
        vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)

        # Get texture coordinates
        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1),]
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        # Get normals
        # NOTE: Multiply tuples by 6 because each face, which has 6 vertices, have the same normal
        normals = [( 0, 0, 1) * 6,
                   ( 1, 0, 0) * 6,
                   ( 0, 0,-1) * 6,
                   (-1, 0, 0) * 6,
                   ( 0, 1, 0) * 6,
                   ( 0,-1, 0) * 6,]
        normals = np.array(normals, dtype='f4').reshape(36, 3)

        # NOTE: We horizontally concat per-vertex data
        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        return vertex_data


class CatVBO(BaseVBO):
    """
    Cat model vertex buffer object loaded from OBJ file.

    Uses pywavefront to load complex mesh data with textures and normals.
    """

    def __init__(self, app):
        """
        Initialize cat VBO with vertex format and attributes.

        :param app: Reference to main application
        :type app: Application
        """
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    def get_vertex_data(self):
        """
        Load cat model vertex data from OBJ file.

        :return: NumPy array containing cat mesh vertex data
        :rtype: numpy.ndarray
        """
        objs = pywavefront.Wavefront('objects/cat/20430_Cat_v1_NEW.obj', cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        return vertex_data


class SkyBoxVBO(BaseVBO):
    """
    Skybox vertex buffer object for cubemap rendering.

    Generates inside-out cube geometry for skybox rendering.
    """

    def __init__(self, ctx):
        """
        Initialize skybox VBO with vertex format and attributes.

        :param ctx: ModernGL context for buffer creation
        :type ctx: ModernGL context
        """
        super().__init__(ctx)
        self.format = '3f'
        self.attribs = ['in_position']

    @staticmethod
    def get_data(vertices, indices):
        """
        Extract vertex data from vertices using indices.

        :param vertices: List of vertex positions
        :type vertices: list
        :param indices: List of triangle indices
        :type indices: list
        :return: NumPy array of vertex data in order specified by indices
        :rtype: numpy.ndarray
        """
        # NOTE: Uses list comprehension to Outputs large list of tuples!
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self):
        """
        Generate vertex data for inside-out skybox cube.

        :return: NumPy array containing skybox vertex data
        :rtype: numpy.ndarray
        """
        # Get vertex coordinates
        vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)
        vertex_data = np.flip(vertex_data, 1).copy(order='C')
        return vertex_data


class AdvancedSkyBoxVBO(BaseVBO):
    """
    Advanced skybox VBO using fullscreen triangle for efficient rendering.

    Generates a large triangle that covers the entire screen for skybox projection.
    """

    def __init__(self, ctx):
        """
        Initialize advanced skybox VBO with vertex format and attributes.

        :param ctx: ModernGL context for buffer creation
        :type ctx: ModernGL context
        """
        super().__init__(ctx)
        self.format = '3f'
        self.attribs = ['in_position']

    def get_vertex_data(self):
        """
        Generate vertex data for fullscreen triangle.

        :return: NumPy array containing three vertices that cover screen space
        :rtype: numpy.ndarray
        """
        # NOTE: Generates a fullscreen quad through a large triangle
        z = 0.9999
        vertices = [(-1, -1, z), (3, -1, z), (-1, 3, z)]
        vertex_data = np.array(vertices, dtype='f4')
        return vertex_data
