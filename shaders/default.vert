
#version 330 core

/*
    Default vertex shader for 3D object rendering
    Handles vertex transformation, normal calculation, and shadow mapping
*/

layout (location = 0) in vec2 in_texcoord_0; // Texture coordinates
layout (location = 1) in vec3 in_normal; // Vertex normal
layout (location = 2) in vec3 in_position; // Vertex position

out vec2 uv_0; // Output texture coordinates
out vec3 normal; // Output normal in world space
out vec3 fragPos; // Output fragment position in world space
out vec4 shadowCoord; // Output shadow coordinates

uniform mat4 m_proj; // Projection matrix
uniform mat4 m_view; // View matrix
uniform mat4 m_view_light; // Light view matrix for shadow mapping
uniform mat4 m_model; // Model matrix

/*
    Shadow bias matrix for converting from [-1,1] to [0,1] range
    Also applies small offset to prevent shadow acne
*/
mat4 m_shadow_bias = mat4(
    0.5, 0.0, 0.0, 0.0,
    0.0, 0.5, 0.0, 0.0,
    0.0, 0.0, 0.5, 0.0,
    0.5, 0.5, 0.5, 1.0
);

void main()
{
    // Pass through texture coordinates
    uv_0 = in_texcoord_0;

    // Calculate fragment position in world space
    fragPos = vec3(m_model * vec4(in_position, 1.0));

    // Transform normal to world space using normal matrix
    normal = mat3(transpose(inverse(m_model))) * normalize(in_normal);

    // Calculate final vertex position in clip space
    gl_Position = m_proj * m_view * m_model * vec4(in_position, 1.0);

    // Calculate shadow coordinates from light perspective
    mat4 shadowMVP = m_proj * m_view_light * m_model;
    shadowCoord = m_shadow_bias * shadowMVP * vec4(in_position, 1.0);

    // Apply small offset to prevent shadow acne artifacts
    shadowCoord.z -= 0.0005;
}
