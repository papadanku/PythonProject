
"""
This module processes an application's textures
"""

# Import Python modules
if __name__ == '__main__':
    import moderngl as mgl
    import pygame as pg


class Texture:
    """
    Load and manage 2D and cubemap textures.
    Handles texture loading, processing, and OpenGL resource management.
    """

    def __init__(self, app):
        """
        Initialize texture manager and load all required textures.

        :param app: Reference to main application
        :type app: Application
        """
        self.app = app
        self.ctx = app.ctx
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/img.png')
        self.textures[1] = self.get_texture(path='textures/img_1.png')
        self.textures[2] = self.get_texture(path='textures/img_2.png')
        self.textures['cat'] = self.get_texture(path='objects/cat/20430_cat_diff_v1.jpg')
        self.textures['skybox'] = self.get_texture_cube(dir_path='textures/skybox1/', ext='png')
        self.textures['depth_texture'] = self.get_depth_texture()

    def get_depth_texture(self):
        """
        Create depth texture for shadow mapping.

        :return: Depth texture configured for shadow rendering
        :rtype: Texture
        """
        depth_texture = self.ctx.depth_texture(self.app.WIN_SIZE)
        depth_texture.repeat_x = False
        depth_texture.repeat_y = False
        return depth_texture

    def get_texture_cube(self, dir_path, ext='png'):
        """
        Load and process cubemap textures for skybox.

        :param dir_path: Directory containing cubemap face images
        :type dir_path: str
        :param ext: File extension for cubemap images (default: 'png')
        :type ext: str
        :return: Cubemap texture ready for skybox rendering
        :rtype: Texture
        """
        faces = ['right', 'left', 'top', 'bottom'] + ['front', 'back'][::-1]
        # textures = [pg.image.load(dir_path + f'{face}.{ext}').convert() for face in faces]
        textures = []
        for face in faces:
            texture = pg.image.load(dir_path + f'{face}.{ext}').convert()
            if face in ['right', 'left', 'front', 'back']:
                texture = pg.transform.flip(texture, flip_x=True, flip_y=False)
            else:
                texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            textures.append(texture)

        size = textures[0].get_size()
        texture_cube = self.ctx.texture_cube(size=size, components=3, data=None)

        for i in range(6):
            texture_data = pg.image.tostring(textures[i], 'RGB')
            texture_cube.write(face=i, data=texture_data)

        return texture_cube

    def get_texture(self, path):
        """
        Load 2D texture with mipmapping and anisotropic filtering.

        :param path: Path to texture image file
        :type path: str
        :return: Processed 2D texture ready for rendering
        :rtype: Texture
        """
        # NOTE: Flip the texture along the Y-axis because PyGame has a downward Y-axis
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        # Mipmapping
        texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
        texture.build_mipmaps()
        # Anisotropic filtering
        texture.anisotropy = 32.0
        return texture

    def destroy(self):
        """
        Release all texture resources from memory.
        Clean up loaded textures when texture manager is destroyed.
        """
        [tex.release() for tex in self.textures.values()]
