
class SceneRenderer:
    """
    Handle multi-pass rendering including shadow mapping and main scene rendering.
    Coordinates complete rendering pipeline with depth buffer and final output.
    """

    def __init__(self, app):
        """
        Initialize scene renderer with application context and resources.

        Args:
            app: Reference to main application
        """
        self.app = app
        self.ctx = app.ctx
        self.mesh = app.mesh
        self.scene = app.scene
        # Render depth buffer
        self.depth_texture = self.mesh.texture.textures['depth_texture']
        self.depth_fbo = self.ctx.framebuffer(depth_attachment=self.depth_texture)

    def render_shadow(self):
        """
        Render depth buffer for shadow mapping.
        Clears and uses depth framebuffer, then renders all objects for shadow calculation.
        """
        self.depth_fbo.clear()
        self.depth_fbo.use()
        for obj in self.scene.objects:
            obj.render_shadow()

    def main_render(self):
        """
        Render main scene with textures and lighting.
        Uses screen framebuffer and renders all objects plus skybox.
        """
        self.app.ctx.screen.use()
        for obj in self.scene.objects:
            obj.render()
        self.scene.skybox.render()

    def render(self):
        """
        Execute complete rendering pipeline.
        Updates scene, performs shadow pass, then renders main scene.
        """
        self.scene.update()
        # Pass 1
        self.render_shadow()
        # Pass 2
        self.main_render()

    def destroy(self):
        """
        Release framebuffer resources.
        Clean up depth framebuffer when renderer is destroyed.
        """
        self.depth_fbo.release()
