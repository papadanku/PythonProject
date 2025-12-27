
#version 330 core

/*
    Shadow map vertex shader
    Transforms vertices from light perspective for depth rendering
*/

layout (location = 2) in vec3 in_position;  // Vertex position

uniform mat4 m_proj; // Projection matrix
uniform mat4 m_view_light; // Light view matrix
uniform mat4 m_model; // Model matrix

void main()
{
    // Calculate model-view-projection matrix from light perspective
    mat4 mvp = m_proj * m_view_light * m_model;

    // Transform vertex position to light clip space
    gl_Position = mvp * vec4(in_position, 1.0);
}
