
#version 330 core

/*
    Advanced skybox vertex shader
    Generates fullscreen triangle and outputs clip coordinates for proper projection
*/

layout (location = 0) in vec3 in_position; // Vertex position (screen space coordinates)

out vec4 clipCoords; // Output clip coordinates for fragment shader

void main()
{
    // Pass through position directly (already in clip space)
    gl_Position = vec4(in_position, 1.0);

    // Pass clip coordinates to fragment shader
    clipCoords = gl_Position;
}
