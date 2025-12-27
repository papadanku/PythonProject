
#version 330 core

/*
    Skybox vertex shader
    Transforms skybox vertices and outputs texture coordinates for cubemap sampling
*/

layout (location = 0) in vec3 in_position; // Vertex position (same as texture coordinates)

out vec3 texCubeCoords; // Output texture coordinates for cubemap

uniform mat4 m_proj; // Projection matrix
uniform mat4 m_view; // View matrix (rotation only, no translation)

void main()
{
    // Pass through position as texture coordinates
    texCubeCoords = in_position;

    // Transform vertex position
    vec4 pos = m_proj * m_view * vec4(in_position, 1.0);

    // Use w component for z to ensure skybox renders at far plane
    gl_Position = pos.xyww;

    // Apply small offset to prevent depth fighting
    gl_Position.z -= 0.0001;
}
