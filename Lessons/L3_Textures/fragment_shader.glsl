#version 330 core

out vec4 FragColor;

in vec3 vertexColor;
in vec2 TexCoord;

uniform vec4 factor;
uniform float alpha;
uniform sampler2D ourTexture;

void main()
{
//    FragColor = vec4(0.5f, 0.5f, 0.75f, 1.0f) * factor;
//    FragColor = vec4(vertexColor, alpha) * factor;
    FragColor = texture(ourTexture, TexCoord) * factor.b; //* vec4(1.0, 1.0, 1.0, alpha);
}