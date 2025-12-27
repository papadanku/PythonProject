
#version 330 core

/*
    Advanced skybox fragment shader
    Uses inverse projection to sample cubemap with proper perspective
*/

out vec4 fragColor; // Final fragment color

in vec4 clipCoords; // Clip coordinates from vertex shader

uniform samplerCube u_texture_skybox; // Cubemap texture
uniform mat4 m_invProjView; // Inverse projection-view matrix

void main()
{
    // Inversely project from [clip-space] to [normalized world space]
    // This converts screen coordinates back to world direction vectors
    vec4 worldCoords = m_invProjView * clipCoords;

    // Normalize to get direction vector for cubemap sampling
    vec3 texCubeCoord = normalize(worldCoords.xyz / worldCoords.w);

    // Sample cubemap texture using calculated direction
    fragColor = texture(u_texture_skybox, texCubeCoord);
}
