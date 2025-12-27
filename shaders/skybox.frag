
#version 330 core

/*
    Skybox fragment shader
    Samples cubemap texture using interpolated texture coordinates
*/

out vec4 fragColor; // Final fragment color

in vec3 texCubeCoords; // Interpolated texture coordinates for cubemap

uniform samplerCube u_texture_skybox; // Cubemap texture

void main()
{
    // Sample cubemap texture using texture coordinates
    fragColor = texture(u_texture_skybox, texCubeCoords);
}
