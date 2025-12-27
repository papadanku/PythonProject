
# Import Python modules
if __name__ == '__main__':
    import glm

class Light:
    """
    Directional light source with ambient, diffuse, and specular components.
    Provides lighting calculations and shadow mapping view matrix.
    """

    def __init__(self, position=(50, 50, -10), color=(1, 1, 1)):
        """
        Initialize light with position, color, and intensity components.

        Args:
            position: Light position in world coordinates (x, y, z)
            color: Light color as RGB values (default: white)
        """
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)
        self.direction = glm.vec3(0, 0, 0)
        # Intensities
        self.Ia = 0.06 * self.color # Ambient
        self.Id = 0.8 * self.color # Diffuse
        self.Is = 1.0 * self.color # Specular
        # View matrix
        self.m_view_light = self.get_view_matrix()

    def get_view_matrix(self):
        """
        Calculate light view matrix for shadow mapping.

        Returns:
            mat4: View matrix from light's perspective
        """
        return glm.lookAt(self.position, self.direction, glm.vec3(0, 1, 0))
