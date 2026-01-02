
# Import Python modules
if __name__ == '__main__':
    import glm
    import pygame as pg

# Camera constants
FOV = 50 # Field of view in degrees
NEAR = 0.1 # Near clipping plane distance
FAR = 100 # Far clipping plane distance
SPEED = 0.01 # Camera movement speed
SENSITIVITY = 0.05 # Mouse look sensitivity

class Camera:
    """
    First-person camera that handles view projection, movement, and rotation.

    Provides matrix calculations for 3D scene rendering and user navigation.
    """

    def __init__(self, app, position=(0, 0, 4), yaw=-90, pitch=0):
        """
        Initialize camera with position, orientation, and projection matrices.

        :param app: Reference to main application
        :type app: Application
        :param position: Initial camera position (x, y, z)
        :type position: tuple
        :param yaw: Initial horizontal rotation in degrees
        :type yaw: int
        :param pitch: Initial vertical rotation in degrees
        :type pitch: int
        """
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        # Setup camera/eye position and up-vector
        self.position = glm.vec3(position)
        self.up = glm.vec3(0, 1, 0)
        # Setup orthonormal basis vectors
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)
        # Setup orientations
        self.yaw = yaw
        self.pitch = pitch
        # View matrix
        self.m_view = self.get_view_matrix()
        # Projection matrix
        self.m_proj = self.get_projection_matrix()

    def rotate(self):
        """
        Update camera yaw and pitch based on mouse movement.

        Applies sensitivity scaling and clamps pitch to prevent over-rotation.
        """
        rel_x, rel_y = pg.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        """
        Recalculate forward, right, and up vectors based on current orientation.

        Uses spherical coordinates to convert yaw/pitch angles to 3D direction vectors.
        """
        yaw = glm.radians(self.yaw)
        pitch = glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        """
        Update camera position and orientation each frame.

        Handles movement, rotation, and recalculates view matrix.
        """
        self.move()
        self.rotate()
        self.update_camera_vectors()
        # Re-calculate the view matrix
        self.m_view = self.get_view_matrix()

    def move(self):
        """
        Handle keyboard input for camera movement in 3D space.

        Uses WASD for horizontal movement and QE for vertical movement.
        """
        velocity = SPEED * self.app.delta_time
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.position += self.forward * velocity
        if keys[pg.K_s]:
            self.position -= self.forward * velocity
        if keys[pg.K_a]:
            self.position -= self.right * velocity
        if keys[pg.K_d]:
            self.position += self.right * velocity
        if keys[pg.K_q]:
            self.position += self.up * velocity
        if keys[pg.K_e]:
            self.position -= self.up * velocity

    def get_view_matrix(self):
        """
        Calculate view matrix using camera position and orientation.

        :return: View matrix for transforming world coordinates to camera space
        :rtype: mat4
        """
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        """
        Calculate perspective projection matrix.

        :return: Projection matrix for perspective transformation
        :rtype: mat4
        """
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)
