
#version 330 core

/*
    Default fragment shader for 3D object rendering
    Implements Phong lighting model with shadow mapping and gamma correction
*/

layout (location = 0) out vec4 fragColor; // Final fragment color

in vec2 uv_0; // Texture coordinates
in vec3 normal; // Normal vector in world space
in vec3 fragPos; // Fragment position in world space
in vec4 shadowCoord; // Shadow coordinates for shadow mapping

// Light structure containing position and intensity components
struct Light
{
    vec3 position; // Light position in world space
    vec3 Ia; // Ambient intensity
    vec3 Id; // Diffuse intensity
    vec3 Is; // Specular intensity
};

uniform Light light; // Light data
uniform sampler2D u_texture_0; // Diffuse texture
uniform vec3 camPos; // Camera position in world space
uniform sampler2DShadow shadowMap; // Shadow map texture
uniform vec2 u_resolution; // Viewport resolution for soft shadows

/*
    Sample shadow map with offset for soft shadows
    Handles perspective division and applies pixel offset
*/
float lookup(float ox, float oy)
{
    vec2 pixelOffset = 1.0 / u_resolution;
    // NOTE: Multiply by shadowCoord.w due to GPU's perspective division!
    return textureProj(shadowMap, shadowCoord + vec4(vec2(ox, oy) * pixelOffset * shadowCoord.ww, 0.0, 0.0));
}

/*
    Calculate soft shadows using 16-sample pattern
    Creates smoother shadow edges by sampling multiple points
*/
float getSoftShadowX16()
{
    float shadow;
    float swidth = 1.0;
    float endp = swidth * 1.5;
    for (float y = -endp; y <= endp; y += swidth)
    {
        for (float x = -endp; x <= endp; x += swidth)
        {
            shadow += lookup(x, y);
        }
    }
    return shadow / 16.0;
}

/*
    Calculate hard shadows from shadow map
    Uses single sample for crisp shadow edges
*/
float getShadow()
{
    float shadow = textureProj(shadowMap, shadowCoord);
    return shadow;
}

/*
    Compute Phong lighting with ambient, diffuse, and specular components
    Applies shadow factor to diffuse and specular lighting
*/
vec3 getLight(vec3 color)
{
    vec3 Normal = normalize(normal);

    // Ambient light (constant illumination)
    vec3 ambient = light.Ia;

    // Diffuse light (Lambertian reflection)
    vec3 lightDir = normalize(light.position - fragPos);
    float diff = max(0, dot(lightDir, Normal));
    vec3 diffuse = diff * light.Id;

    // Specular light (Blinn-Phong highlight)
    vec3 viewDir = normalize(camPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, Normal);
    float spec = pow(max(dot(viewDir, reflectDir), 0), 32);
    vec3 specular = spec * light.Is;

    // Use soft shadows for smoother edges
    // float shadow = getShadow();
    float shadow = getSoftShadowX16();

    // Combine lighting components with shadow factor
    return color * (ambient + (diffuse + specular) * shadow);
}

void main()
{
    // Apply gamma correction for linear color space
    float gamma = 2.2;
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color = pow(color, vec3(gamma));

    // Calculate lighting
    color = getLight(color);

    // Convert back from linear to sRGB color space
    color = pow(color, 1.0 / vec3(gamma));
    fragColor = vec4(color, 1.0);
}
