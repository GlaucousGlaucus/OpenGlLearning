#version 330 core

out vec4 FragColor;

in vec3 vertexColor;

uniform vec4 factor;

void main()
{
//    FragColor = vec4(0.5f, 0.5f, 0.75f, 1.0f) * factor;
    FragColor = vec4(vertexColor, 1.0f) * factor;
}